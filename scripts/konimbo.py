#!/usr/bin/env python3
"""Minimal Konimbo API v1 client (stdlib only).

Token is read from the KONIMBO_API_TOKEN environment variable.
Write operations are dry-run unless --apply is given; before a PUT/DELETE
the current record is saved under backups/.

Examples:
  konimbo.py get items 1086782 --attributes id,title,price
  konimbo.py get items 0 --param code=SKU#345
  konimbo.py list items --param visible=true --attributes id,title,price --all
  konimbo.py list orders --param created_at_min=2026-10-01T00:00:00Z
  konimbo.py put items 1086782 --data '{"price": "1850"}'            # dry-run
  konimbo.py put items 1086782 --data '{"price": "1850"}' --apply
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://api.konimbo.co.il/v1"
BACKUP_DIR = Path(__file__).resolve().parent.parent / "backups"
# Singular body key per resource, as the API expects ({"item": {...}}, {"order": {...}}).
BODY_KEYS = {
    "items": "item",
    "orders": "order",
    "carts": "cart",
    "customers": "customer",
    "webhooks": "webhook",
}


def token():
    value = os.environ.get("KONIMBO_API_TOKEN")
    if not value:
        sys.exit("KONIMBO_API_TOKEN is not set")
    return value


def call(method, path, params=None, body=None):
    query = dict(params or {})
    if body is None:
        query["token"] = token()
    else:
        body = {"token": token(), **body}
    url = f"{BASE_URL}/{path}?{urllib.parse.urlencode(query)}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method.upper())
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = resp.read().decode() or "null"
            return json.loads(payload), dict(resp.headers)
    except urllib.error.HTTPError as err:
        detail = err.read().decode(errors="replace")
        sys.exit(f"HTTP {err.code} {method.upper()} {path}: {detail}")


def parse_params(pairs):
    params = {}
    for pair in pairs or []:
        key, _, value = pair.partition("=")
        params[key] = value
    return params


def backup(resource, ident, params):
    current, _ = call("get", f"{resource}/{ident}", params)
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = BACKUP_DIR / f"{resource}-{ident}-{stamp}.json"
    path.write_text(json.dumps(current, ensure_ascii=False, indent=2))
    return current, path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["get", "list", "post", "put", "delete"])
    ap.add_argument("resource", help="items, orders, carts, customers, webhooks, store_categories")
    ap.add_argument("id", nargs="?", help="record id (use 0 with --param code=... / email=...)")
    ap.add_argument("--param", action="append", help="query parameter key=value (repeatable)")
    ap.add_argument("--attributes", help="comma-separated fields to return")
    ap.add_argument("--data", help="JSON object for the record body (post/put)")
    ap.add_argument("--all", action="store_true", help="list: follow pagination to the last page")
    ap.add_argument("--apply", action="store_true", help="actually perform post/put/delete")
    args = ap.parse_args()

    params = parse_params(args.param)
    if args.attributes:
        params["attributes"] = args.attributes

    if args.action == "get":
        result, _ = call("get", f"{args.resource}/{args.id}", params)
    elif args.action == "list":
        result, page = [], int(params.pop("page", 1))
        while True:
            chunk, headers = call("get", args.resource, {**params, "page": page})
            chunk = chunk or []
            result.extend(chunk)
            total = int(headers.get("X-Pagination-Total", len(result)))
            if not args.all or not chunk or len(result) >= total:
                break
            page += 1
        print(f"# {len(result)} records", file=sys.stderr)
    else:
        path = args.resource if args.action == "post" else f"{args.resource}/{args.id}"
        body = None
        if args.action != "delete":
            body = {BODY_KEYS.get(args.resource, args.resource.rstrip("s")): json.loads(args.data or "{}")}
        if not args.apply:
            print(f"DRY-RUN {args.action.upper()} {path} params={params}")
            print(json.dumps(body, ensure_ascii=False, indent=2))
            return
        if args.action in ("put", "delete"):
            _, saved = backup(args.resource, args.id, params)
            print(f"# backup: {saved}", file=sys.stderr)
        result, _ = call(args.action, path, params, body)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
