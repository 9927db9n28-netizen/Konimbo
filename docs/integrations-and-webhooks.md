# מערכת האינטגרציות ו-Webhooks של קונימבו

מקור: `v1/integration.md` ו-`v1/webhooks.md` במאגר התיעוד של קונימבו,
ומדריך הממשק "מערכת אינטגרציות - מדריך שימוש" (Freshdesk, מאמר 4000141160).

## מה זה
מנוע JavaScript שרץ בשרתי קונימבו ומאפשר לחבר מערכות חיצוניות (ERP, משלוחים, דיוור) **בלי שרת משלך**.
מנוהל בממשק: קונימבו - אדמין → **אינטגרציות** / **טריגרים**.

## הפעלה
1. הגדרות מתקדמות לחנות → לסמן **Api** ו**אינטגרציות**.
2. ליצור משתמש API (ראו reference).
3. קונימבו - אדמין → אינטגרציות → אינטגרציה חדשה → **פעיל** → שמירה.

## מבנה אינטגרציה: Config → Initial Script → Actions

### Config
מערך JSON של משתנים שערכיהם נקבעים ב-Trigger ונגישים כ-`vars["key"]`:
```json
[{"type":"password","label":"Konimbo API Token","key":"konimbo_api_token","class":"ltr"}]
```
משתנים מיוחדים: `trigger_id` (ל-/amazons), `log_emails` (מיילים לקובץ לוג, מופרדים בפסיק), `log_file_format` (XML/JSON).

### Initial Script — 5 פונקציות שחובה להגדיר
| פונקציה | מחזירה | תפקיד |
|---|---|---|
| `data(request, vars)` | אובייקט | נתונים התחלתיים. מ-webhook: `request["params"]["order"]["id"]`. לעימוד: `{"_page": 1}` |
| `request(data, vars)` | `{url, method, body, headers, expectedContentType?}` | קריאת ה-HTTP הראשונית. גישה לנתונים: `data[0]["…"]` |
| `filter(data, vars)` | true/false | האם להמשיך |
| `array(response, vars)` | אובייקט/מערך | על מה ירוצו ה-Actions (`response["body"]…`) |
| `hasAnotherPage(response, vars)` | true/false | true = הרצה נוספת עם `_page` מוגדל |

### Actions — לכל Action שלוש פונקציות
- `data(response, vars, current_obj)` — מעבד את האובייקט הנוכחי; נגיש ב-`data[N]` (N = מספר ה-Action, מתחיל ב-1).
- `filter(data, vars)` — true/false.
- `request(data, vars)` — קריאת HTTP. אפשר `internal_data`: `log_type: "items"`, `authentication` (basic_auth), `content_type` (`"blank"` לביטול), `x-forwarded-proto: "https"` (לשגיאת "end of file reached").

### Trigger
קונימבו - אדמין → **טריגרים** → בחירת אינטגרציה → **פעיל**, "הגבלת פעילות" למקסימום בזמן בדיקות,
מילוי ערכי ה-Config. מקבלים URL ייחודי — GET אליו מפעיל את האינטגרציה.
- `Access-Control-Allow-Origin` ב-vars — לאפשר cross-domain.
- `execute_now = YES` — ריצה מיידית (למשל להזמנות).
- "שכבת אבטחה נוספת" — אפשר לבטל.

## Webhooks
אירועים זמינים: `order_created`, `order_created_future` (10 דק' אחרי), `order_after_payment`, `order_created_bulk`,
`order_after_payment_api`, `order_after_payment_paypal`, `order_status_created`, `credit_guard_xml_created`,
`item_inventory_updated`, `customer_created`, `customer_logged_in`, `ticket_created`.

```
POST /v1/webhooks      {"token":"…","webhook":{"callback_url":"https://…","event":"order_created"}}
PUT  /v1/webhooks/{id} {"token":"…","webhook":{…}}
GET  /v1/webhooks?token=…        GET /v1/webhooks/{id}?token=…
```
התבנית הנפוצה: `callback_url` = URL של Trigger → ההזמנה החדשה מגיעה לאינטגרציה →
`data()` שולף את `order.id` → `request()` מביא את ההזמנה המלאה מ-`/v1/orders/{id}` → Action שולח ל-ERP.

הפעלה ידנית מדף העגלה: טופס `POST /webhooks/trigger` עם `id`, `event`, `model` (cart/order), `trigger_data[…]`, `store_subdomain`.
