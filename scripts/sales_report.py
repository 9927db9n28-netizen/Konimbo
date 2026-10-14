#!/usr/bin/env python3
"""Sales summary by manufacturer (brand) and price range, read-only.

Pulls orders for a date range from the Konimbo API, looks up each sold
item's brand, and writes a Markdown report plus CSVs under reports/
(git-ignored: sales data must never land in the public repo).

Examples:
  sales_report.py                       # last 30 days
  sales_report.py --from 2026-09-01 --to 2026-10-01
  sales_report.py --include-cancelled

Revenue is line price x quantity, before order-level discounts and
shipping (those are shown separately in the totals).
"""
import argparse
import csv
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konimbo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
BRAND_CACHE = REPORTS_DIR / "brand-cache.json"
PRICE_BANDS = [0, 100, 250, 500, 1000, 2500, 5000]
CANCELLED_WORDS = ("בוטל", "מבוטל", "ביטול", "cancel")
NO_BRAND = "(ללא יצרן)"


def rate_limited_get(path, params):
    """GET that sleeps until the window resets instead of tripping the 401 block."""
    result, headers = konimbo.call("get", path, params)
    current = int(headers.get("X-Rate-Limit-Current", 0) or 0)
    maximum = int(headers.get("X-Rate-Limit-Maximum", 100) or 100)
    if current >= maximum - 3:
        reset = headers.get("X-Rate-Limit-Reset", "")
        wait = 600
        try:
            reset_at = datetime.fromisoformat(reset.replace("Z", "+00:00"))
            wait = max(5, (reset_at - datetime.now(timezone.utc)).total_seconds() + 5)
        except ValueError:
            pass
        print(f"# rate limit {current}/{maximum}, waiting {int(wait)}s", file=sys.stderr)
        time.sleep(wait)
    return result, headers


def fetch_orders(start, end):
    params = {
        "created_at_min": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at_max": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "attributes": "id,created_at,payment_status,status_option_title,total_price,items,discounts,shipping",
    }
    orders, page = [], 1
    while True:
        chunk, headers = rate_limited_get("orders", {**params, "page": page})
        chunk = chunk or []
        orders.extend(chunk)
        total = int(headers.get("X-Pagination-Total", len(orders)))
        print(f"# orders {len(orders)}/{total}", file=sys.stderr)
        if not chunk or len(orders) >= total:
            return orders
        page += 1


def load_brands(item_ids):
    cache = json.loads(BRAND_CACHE.read_text()) if BRAND_CACHE.exists() else {}
    missing = [i for i in item_ids if str(i) not in cache]
    for n, item_id in enumerate(missing, 1):
        try:
            item, _ = rate_limited_get(f"items/{item_id}", {"attributes": "id,brand"})
            cache[str(item_id)] = (item or {}).get("brand") or NO_BRAND
        except SystemExit as err:  # deleted item -> 404
            print(f"# item {item_id}: {err}", file=sys.stderr)
            cache[str(item_id)] = NO_BRAND
        if n % 20 == 0:
            BRAND_CACHE.write_text(json.dumps(cache, ensure_ascii=False))
            print(f"# brands {n}/{len(missing)}", file=sys.stderr)
    BRAND_CACHE.write_text(json.dumps(cache, ensure_ascii=False))
    return cache


def price_band(price):
    for low, high in zip(PRICE_BANDS, PRICE_BANDS[1:]):
        if price < high:
            return f"₪{low:,}–{high:,}"
    return f"₪{PRICE_BANDS[-1]:,}+"


def is_cancelled(order):
    text = f"{order.get('payment_status') or ''} {order.get('status_option_title') or ''}".lower()
    return any(word in text for word in CANCELLED_WORDS)


def money(value):
    return f"₪{value:,.0f}"


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="start", help="YYYY-MM-DD (default: 30 days ago)")
    ap.add_argument("--to", dest="end", help="YYYY-MM-DD, exclusive (default: now)")
    ap.add_argument("--include-cancelled", action="store_true")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    end = datetime.fromisoformat(args.end).replace(tzinfo=timezone.utc) if args.end else now
    start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc) if args.start else end - timedelta(days=30)
    REPORTS_DIR.mkdir(exist_ok=True)

    orders = fetch_orders(start, end)
    by_status = defaultdict(lambda: [0, 0.0])
    for order in orders:
        key = f"{order.get('payment_status') or '-'} / {order.get('status_option_title') or '-'}"
        by_status[key][0] += 1
        by_status[key][1] += float(order.get("total_price") or 0)
    counted = [o for o in orders if args.include_cancelled or not is_cancelled(o)]

    item_ids = sorted({line["id"] for o in counted for line in o.get("items") or [] if line.get("id")})
    brands = load_brands(item_ids)

    brand_stats = defaultdict(lambda: {"units": 0, "revenue": 0.0, "orders": set(), "items": set()})
    band_stats = defaultdict(lambda: {"units": 0, "revenue": 0.0, "orders": set()})
    matrix = defaultdict(float)
    lines_out, discounts, shipping = [], 0.0, 0.0
    for order in counted:
        shipping += float((order.get("shipping") or {}).get("price") or 0)
        discounts += sum(abs(float(d.get("discount_value") or d.get("price") or 0)) for d in order.get("discounts") or [])
        for line in order.get("items") or []:
            qty = int(line.get("quantity") or 0)
            price = float(line.get("price") or 0)
            revenue = qty * price
            brand = brands.get(str(line.get("id")), NO_BRAND)
            band = price_band(price)
            b = brand_stats[brand]
            b["units"] += qty
            b["revenue"] += revenue
            b["orders"].add(order["id"])
            b["items"].add(line.get("id"))
            p = band_stats[band]
            p["units"] += qty
            p["revenue"] += revenue
            p["orders"].add(order["id"])
            matrix[(brand, band)] += revenue
            lines_out.append([order["id"], order.get("created_at"), brand, line.get("id"), line.get("code"),
                              line.get("title"), qty, price, revenue, band])

    total_rev = sum(b["revenue"] for b in brand_stats.values()) or 1
    total_units = sum(b["units"] for b in brand_stats.values())
    brand_rows = sorted(brand_stats.items(), key=lambda kv: -kv[1]["revenue"])
    band_order = [price_band(low) for low in PRICE_BANDS]
    stamp = f"{start:%Y-%m-%d}_{end:%Y-%m-%d}"

    with open(REPORTS_DIR / f"sales-lines-{stamp}.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["order_id", "created_at", "brand", "item_id", "code", "title", "quantity", "unit_price", "revenue", "price_band"])
        w.writerows(lines_out)
    with open(REPORTS_DIR / f"sales-by-brand-{stamp}.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["brand", "units", "revenue", "orders", "distinct_items", "avg_unit_price", "share"])
        for brand, s in brand_rows:
            w.writerow([brand, s["units"], round(s["revenue"], 2), len(s["orders"]), len(s["items"]),
                        round(s["revenue"] / s["units"], 2) if s["units"] else 0, round(s["revenue"] / total_rev, 4)])

    md = [f"# סיכום מכירות {start:%d/%m/%Y} – {end:%d/%m/%Y}", ""]
    md.append(f"- הזמנות שנספרו: **{len(counted)}** (מתוך {len(orders)} שנוצרו בתקופה)")
    md.append(f"- יחידות: **{total_units:,}** · מחזור שורות מוצר: **{money(sum(b['revenue'] for b in brand_stats.values()))}**")
    md.append(f"- משלוחים: {money(shipping)} · הנחות ברמת הזמנה: {money(discounts)} · "
              f"סה\"כ total_price: {money(sum(float(o.get('total_price') or 0) for o in counted))}")
    md += ["", "## לפי יצרן", ""]
    md.append(table(["יצרן", "יחידות", "מחזור", "% מהמחזור", "הזמנות", "מוצרים שונים", "מחיר יחידה ממוצע"],
                    [[brand, s["units"], money(s["revenue"]), f"{s['revenue'] / total_rev:.1%}", len(s["orders"]),
                      len(s["items"]), money(s["revenue"] / s["units"]) if s["units"] else "-"] for brand, s in brand_rows]))
    md += ["", "## לפי טווח מחיר (מחיר יחידה)", ""]
    md.append(table(["טווח", "יחידות", "מחזור", "% מהמחזור", "הזמנות"],
                    [[band, band_stats[band]["units"], money(band_stats[band]["revenue"]),
                      f"{band_stats[band]['revenue'] / total_rev:.1%}", len(band_stats[band]["orders"])]
                     for band in band_order if band in band_stats]))
    top = [brand for brand, _ in brand_rows[:15]]
    bands = [band for band in band_order if band in band_stats]
    md += ["", "## יצרן × טווח מחיר (מחזור, 15 היצרנים המובילים)", ""]
    md.append(table(["יצרן"] + bands, [[brand] + [money(matrix[(brand, band)]) if matrix[(brand, band)] else "" for band in bands]
                                       for brand in top]))
    md += ["", "## מצבי הזמנה בתקופה", ""]
    md.append(table(["מצב תשלום / מצב הזמנה", "הזמנות", "total_price"],
                    [[k, v[0], money(v[1])] for k, v in sorted(by_status.items(), key=lambda kv: -kv[1][0])]))
    md += ["", "_הזמנות שמצבן מכיל 'בוטל'/'ביטול' לא נספרו (אלא אם הורץ עם --include-cancelled)._"]
    out = REPORTS_DIR / f"sales-report-{stamp}.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
