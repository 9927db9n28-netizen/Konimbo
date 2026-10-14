# דינמיקה (dynamica.co.il) — ניהול חנות קונימבו

מאגר זה משמש לניהול האתר www.dynamica.co.il, שבנוי על פלטפורמת **קונימבו** (Konimbo).
הוא מכיל ידע מסודר על המערכת, והוראות עבודה מול ה-API שלה.

## מפת המאגר
- `docs/konimbo-api-reference.md` — מדריך API מלא: נקודות קצה, שדות, התנהגויות מסוכנות (דריסה).
- `docs/integrations-and-webhooks.md` — מערכת האינטגרציות של קונימבו (Config / Initial Script / Actions / Trigger) ו-Webhooks.
- `docs/api-vs-ui.md` — מתי לבצע משימה דרך ה-API ומתי דרך ממשק הניהול.
- `docs/admin-guides-index.md` — אינדקס מדריכי הממשק (Freshdesk) וסטטוס הלמידה שלהם.
- `docs/course/` — קורס מלא (13 שיעורים) מסוכם מכל מדריכי Freshdesk; התחלה ב-`docs/course/README.md`.
- `scripts/konimbo.py` — לקוח API לשורת הפקודה (ללא תלויות חיצוניות).

## כללי עבודה
1. **טוקן**: נקרא רק ממשתנה הסביבה `KONIMBO_API_TOKEN`. אסור לכתוב טוקן בקוד, בקומיט או בהודעה.
2. **קריאה לפני כתיבה**: לפני כל עדכון — GET למצב הנוכחי ושמירת גיבוי ב-`backups/` (לא נכנס ל-git).
3. **אישור לפני שינוי**: כל פעולת כתיבה (POST/PUT/DELETE) על האתר החי — להציג למנהל מה ישתנה ולקבל אישור.
   ברירת המחדל של `scripts/konimbo.py` לכתיבה היא dry-run; ביצוע אמיתי רק עם `--apply`.
4. **שדות בדריסה מלאה** (מה שלא נשלח — נמחק): `images`, `related_items`, `spec`, `secondary_category_titles`,
   `related_tags` (ללא `add_to_item`). כשמעדכנים אותם — שולחים תמיד את הרשימה המלאה הרצויה.
5. **מגבלת קצב**: 100 קריאות ל-10 דקות לטוקן (ברירת מחדל). חסימה מחזירה 401 — לא לנסות שוב בלולאה.
6. **עימוד**: 20 רשומות לדף כברירת מחדל; לעבור דפים עם `page=N` ולבדוק את `X-Pagination-Total`.

## גישת רשת בסביבת הענן
הדומיינים `api.konimbo.co.il`, `konimbo.freshdesk.com` ו-`www.dynamica.co.il` מאושרים ב-Allowed domains.
לקריאות API צריך להגדיר את `KONIMBO_API_TOKEN` כמשתנה סביבה בהגדרות הסביבה. בלי טוקן, ה-API מחזיר 401.
