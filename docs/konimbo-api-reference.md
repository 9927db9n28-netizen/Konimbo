# מדריך API של קונימבו — סיכום מלא

מקור: https://github.com/konimbo/API-Documentation (v1). הסיכום נכתב אחרי קריאה מלאה של כל הקבצים.

## יסודות

| נושא | פירוט |
|---|---|
| Endpoint | `https://api.konimbo.co.il/v1` (HTTPS בלבד) |
| פורמט | JSON בגוף הבקשה ובתשובה (XML רק בתיאום עם התמיכה) |
| אימות | פרמטר `token` בכל קריאה — ב-query ל-GET/DELETE, בגוף ה-JSON ל-POST/PUT. בלי טוקן תקף: `401` |
| זמנים | ISO-8601: `YYYY-MM-DDTHH:MM:SSZ` |
| עימוד | 20 לדף. Headers: `X-Pagination-Per-Page`, `X-Pagination-Total`, `X-Pagination-Links`. דף: `page=N` |
| הגבלת קצב | 100 קריאות / 10 דקות לטוקן. Headers: `X-Rate-Limit-Current`, `X-Rate-Limit-Maximum`, `X-Rate-Limit-Reset`. חסימה = `401` |
| הגבלת רשומות | ההודעה `You have reached the maximum amount of items...` = יש להגדיל את "הגבלת רשומות" של משתמש ה-API |
| בחירת שדות | `attributes=id,title,price` בכל GET — מקטין תשובה ומזרז |

### יצירת משתמש API (בממשק)
1. הגדרות מתקדמות לחנות → לסמן **Api** (ולאינטגרציות גם **אינטגרציות**).
2. משתמשים - אדמין → **משתמשי API** → משתמש חדש, לסמן **פעיל**.
3. להגדיר "הגבלת קריאות" ו"הגבלת רשומות", ולתת הרשאות רק ל-endpoints הנדרשים (עיקרון ההרשאה המינימלית).
4. בהגדרת המשתמש נקבע גם אם חיפוש מוצר הוא לפי `id` / `code` / `second_code`, ולקוח לפי `id` / `email`.

---

## מוצרים — `/items`

| פעולה | קריאה |
|---|---|
| רשימה | `GET /v1/items?token=…` |
| מוצר בודד | `GET /v1/items/{id}` · לפי מק"ט: `GET /v1/items/0?code=…` · משני: `?second_code=…` |
| יצירה | `POST /v1/items` גוף: `{"token":…, "item":{…}}` |
| עדכון | `PUT /v1/items/{id}` או `PUT /v1/items/0?code=…` גוף: `{"token":…, "item":{…}}` |
| מחיקה (לפח, ניתן לשחזור) | `DELETE /v1/items/{id}?token=…` |

- חיפוש לפי `code`/`second_code` דורש הגדרה במשתמש ה-API (מול התמיכה). אם מק"ט מופיע פעמיים — רק מוצר אחד יתעדכן.
- **יצירה — שדות חובה**: `title`, `store_category_title`. אם נשלח `code` קיים — המוצר **יתעדכן** במקום להיווצר (upsert).

### סינון ומיון ברשימה
`created_at_min/max`, `updated_at_min/max`, `min_price`, `max_price`, `group_value_id` (ערך סינון),
`visible=true|false`, `tag_id`, `store_category_id`. מיון: `sort_by=price|updated_at|…` + `sort_order=asce|desc`.

### שדות פשוטים (כולם ניתנים לעדכון אלא אם צוין)
- **זיהוי**: `id` (קריאה בלבד), `code` (מק"ט), `second_code`, `slug`
- **תוכן**: `title`, `desc` (תיאור קצר), `content` (מידע נוסף), `spec_text`, `features`, `note`, `warranty`, `kit`, `promotions`, `matching_models`, `video` (קוד YouTube בלבד)
- **מחיר**: `price`, `origin_price` (מחיר לפני מבצע — מציג "מחיר מקורי"), `cost`, `related_item_price`, `restore_price` (מחיר ספק מומלץ), `eilat_price`, `discount_prices` (מחירי מועדון), `max_payment`, `free_payment` (תשלומים ללא ריבית)
- **מלאי**: `quantity` (מלאי פשוט), `quantity_step` (קפיצות במשקל), `delivery_time` (ימי אספקה)
- **תצוגה**: `visible`, `position`, `store_category_title`, `css_class`, `store_layout_title` (טמפלט), `head_html` / `foot_html` (liquid), `only_contact` (סוג מכירה: צור קשר בלבד), `offer_code` (קוד גישה), `visit_link`
- **ספק/יצרן**: `model_title` (ספק), `brand` (יצרן)
- **SEO**: `seo_title`, `seo_description`, `seo_keywords`, `slug`, `prev_url`
- **מוצר אבא/בן**: `is_dad`, `dad_id`, `color_group`
- **זאפ**: `zap_visable`, `zap_product_type`, `zap_item` (`url`, `price_limit` לרובוט זאפ)
- **משלוחים**: `default_shipping`, `shipping_option_ids` (מערך מזהי משלוח)
- **הנחות**: `discount_group_id`, `discount_group_title`, `coupon_group_name`
- **מכירה אישית**: `personal_sell`, `personal_sell_min_price`, `personal_sell_win_price`
- **שדות נוספים**: `data_record_var` (אובייקט, לשדות שהוגדרו בחנות)
- **קריאה בלבד**: `created_at`, `updated_at`, `destroy_at`, `store_category_group_title`

### שדות מיוחדים — ⚠️ שימו לב להתנהגות דריסה

| שדה | התנהגות | מחיקת הכל |
|---|---|---|
| `images` (עד 12 לקריאה; `url`, `alt`, `position`) | **דריסה**: מה שלא נשלח — נמחק. זיהוי לפי URL. עדכון מתבצע רק אם משהו השתנה | `[{"url":"","alt":"","position":"","delete":"true"}]` |
| `related_items` (`friend_item_id`/`friend_item_code`, `position`) | **דריסה** | `[{"friend_item_id":null,"position":null,"delete":"true"}]` |
| `spec` (`group`, `name`, `value`, `position`, `duplicate`) | **דריסה**. זיהוי שורה לפי group+name (לא ניתן לשנותם). `duplicate:"true"` ליצירת שורה כפולה | `[{"group":null,"name":null,"value":null,"position":null,"delete":"true"}]` |
| `secondary_category_titles` (`title_he`) | **דריסה**; קטגוריה לא קיימת נוצרת | `[{"remove_from_item":"true"}]` |
| `related_tags` (`title`, …) | **דריסה** כברירת מחדל; `add_to_item:"true"` מוסיף בלבד; `remove_from_item:"true"` מסיר תג ספציפי | `[{"remove_from_item":"true"}]` |
| `filters` (`group_title`, `group_value_title`, `group_position`, `group_value_position`, `broad`) | **הוספה**; סינון חסר נוצר אוטומטית. הסרה: `id` + `remove_from_item:"true"` | — |
| `set_icons` (`image_title` חובה, `title`, `url`, `visible`, `index-visible`) | משייך אייקונים **קיימים** בלבד. `remove:"all"` מסיר שיוכים קודמים | — |
| `discount_prices` | `{"field_<clubId>": "60.0"}` | — |
| `inventory` (מלאי מורכב, עד 30 לקריאה: `id`, `code`, `price`=תוספת מחיר, `free`=כמות) | עדכון לפי `code` (או `id`). יצירת סוג חדש: `upgrade_topic_title` + `upgrade_title` | — |

### קטגוריות
`GET /v1/store_categories?token=…` — כל הקטגוריות (`id`, `title_he`, `parent_id`, `position`, `slug`, SEO, `image_url`, …).

---

## הזמנות — `/orders`
- `GET /v1/orders` — סינון: `created_at_min/max`, `payment_status` (למשל `שולם`), `status_option_title` (למשל `הזמנה חדשה`); מיון `sort_by`/`sort_order`.
- `GET /v1/orders/{id}` — שדות: `id`, `payment_status`, `name`, `email`, `phone`, `address`, `note`, `total_price`, `status_option_title`, `created_at`, `items[]`, `upgrades[]` (כולל `inventory_code`), `discounts[]`, `shipping{}`, `payments{}`, `credit_card_details{}`, `statuses[]`, `newsletter`.
- `PUT /v1/orders/{id}` — **רק הוספת סטטוסים** (עד 5 לקריאה):
  ```json
  {"token":"…","order":{"statuses":[{"status_option_title":"חסר במלאי","username":"ERP","comment":"…"}]}}
  ```
  אם הכותרת קיימת ב"הזמנות > מצבי הזמנה" — גם מצב ההזמנה משתנה. אחרת — זו רק הערה בהיסטוריה.
- **משלוח כמוצר**: אם מוגדר מק"ט למשלוח בממשק, הוא יופיע בשורות ההזמנה.
- **חיוב ממערכת חיצונית** (דורש פתיחה ע"י קונימבו): `POST https://secure.konimbo.co.il/credit_guard_xmls/{subdomain}/{order_id}/debit?token=…`
- קודי חברות אשראי (`issued_company_number`): 1 ישראכרט, 2 ויזה, 3 דיינרס, 4 אמקס, 5 JCB, 6 לאומיקארד.
  `card_sub_type`: 0 רגיל, 1 זהב, 2 עסקים, 3 חו"ל, 4 חיוב מיידי, 5 דלק, 6 צעיר.

## עגלות — `/carts`
- `GET /v1/carts/{id}` — `items` (כולל `options` — שדרוגים ללא מחיר), `upgrades`, `shipping`, `payments`, `total_price`, `discounts`, `var_in_json`.
- `PUT /v1/carts/{id}` — הוספת הנחות לעגלה **פתוחה ולא נעולה**:
  `discounts[]`: `title`, `quantity`, `discount_value`, `discount_type` (`₪`/`%`), `unit_price`, `type_name`, `line_item_id`, `coupon_code`, `var_in_json` (מחרוזת JSON).
  מחיקה לפני הוספה: `"destroy_discounts": {"type_name": "all"}` (או type_name ספציפי).

## לקוחות — `/customers`
- `GET /v1/customers/0?email=…` (או `/{id}`) — `id`, `full_name`, `email`, `mobile_phone`, `full_address`, `newsletter`, `discount_title` (מועדון), `data_record_json`.
- `POST /v1/customers` — יצירה. `PUT /v1/customers/0` (לפי email) או `/{id}` (לפי ID — לפי הגדרת משתמש ה-API).
- `discount_title` = שם מדויק של מועדון לקוחות לשיוך.

## Webhooks — `/webhooks`
ראו `integrations-and-webhooks.md`.

## אמזון S3 — `/amazons`
- `POST /v1/amazons` — קריאת קובץ XML/JSON מ-S3 (עד 6MB). פרמטרים תחת `amazon`: `region`, `access_key_id`, `secret_access_key`, `bucket_name`, `file_name`, `file_format`.
- `POST /v1/amazons/write_file` — כתיבת קובץ; מחזיר לינק. `data`: `file_name`, `file_type` (json/xml/string/query), `store_unique_token`, `credentials{}`, `content`.

## קודי תשובה
200 הצלחה · 400 בקשה שגויה · 401 טוקן לא תקף / חריגה ממגבלת קצב · 404 לא נמצא · 422 נתונים לא תקינים · 500 שגיאת שרת.
