# ייצוא/ייבוא קבצים ודוחות (19 מאמרים)

## ייצוא מוצרים
- **כל המוצרים**: הגדרות > תגים > "כל המוצרים - CSV" (אחרון ברשימה) > מופיעים/לא מופיעים/פח זבל > "בחר פרמטרים לייצוא" (+ייצוא תמונות כן/לא) > "עדכן אקסל".
- **מוצרים מסוימים**: תג חדש > סימון מוצרים > "עדכן מוצרים" > CSV > פרמטרים > עדכן אקסל.
- הקובץ **נשלח במייל** ל"מיילים לעדכונים" (הגדרות > כללי סעיף 29). דורש הרשאת "הורדת קבצים". **תמיד לכלול `id`**.
- ג'יבריש בעברית: אקסל > נתונים > מטקסט (UTF-8), או אזור מערכת = עברית.
- קבצים שבורים/גדולים: פלואו N8N פנימי (V2→Excel).

## ייבוא מוצרים (CSV)
- הגדרות > תגים > תג חדש (שם עם תאריך) > כניסה לתג > CSV > בחירת קובץ > "עדכן מוצרים מהקובץ". לחיצה **אחת** וממתינים.
- **יצירה** (בלי עמודת `id`!) או **עדכון** (חובה `id`) — לא שניהם באותו קובץ. אין שחזור אוטומטי → לייצא גיבוי לפני.
- חובה ביצירה: `title` + `store_category_title_he` (קטגוריית **בן**, לא אבא).
- שמירה: Excel → CSV (comma delimited); Google Sheets → CSV. בעיות קידוד: לעבור דרך Google Sheets ולא לפתוח את הקובץ.
- לא מצליח? הגדרות החנות: "google spreadsheet key" = 0. ביטול יצירה: עדכון גורף > סינון לפי התג > מחיקה.
- **סיבות לשגיאות**: רווח בכותרות, שגיאת כתיב בכותרת, קטגוריית אבא, title/קטגוריה ריקים, מחיר עם סימנים ("₪", "החל מ"), עלות > מחיר או 0, `prev_url` כפול, `id` ביצירה, תאים ממוזגים, עמודות ריקות.
- **אי אפשר לעדכן באקסל**: תצוגה בחנות, שדרוגים, משלוחים, נלווים, תצוגה במנועי השוואה, מכירה אישית, קבוצת קופון/הנחה, אייקונים, css/קוד, פייפאל, קוד גישה → לתייג ולהשתמש בעדכון גורף.

### מילון עמודות CSV מוצרים
`id`, `title`*, `code`, `second_code`, `cost`, `price`, `warranty`, `position`, `desc`, `store_category_title_he`*, `store_category_position`, `store_category_parent_title`,
`store_category_group_title`, `content` (HTML), `features` (HTML), `visit_link` (לינק זאפ לרובוט), `dad_title`, `note`, `matching_models`, `restore_price`, `price_limit`,
`tag_titles` (מופרד ", "), `tag_category_titles` (קטגוריות משניות; דורש עמודת קטגוריה), `tag_position`, `origin_price`, `video`, `color_group`, `promotions`, `kit`, `quantity`,
`model_title`, `offer_code`, `zap_product_type` (מוצר חדש/מחודש/ממוחזר/עודפים/מתצוגה), `delivery_time`, `related_item_price`, `product_spec` (`blank` למחיקה), `product_brand`, `product_brand_he`,
`image1_path`..`image12_path` (URL ציבורי), `image1_alt`..`image12_alt`, `seo_title`, `seo_description`, `seo_keywords`, `slug`, `prev_url`, `filter_<שם סינון>` (ערכים מופרדים ב-";", דורש עמודת קטגוריה),
`css_class`, `only_contact` (ייצוא בלבד), `special_zap_shipping_price`, `data_record_<שדה>` (שדות נוספים). קישור למוצר = `domain/items/<id>`.
- המרה ל-WebP: דגלים "convert image to web" + "save images with lambda" (166) ואז טעינה חוזרת של התמונות.

## ייבוא מלאי
הגדרות > מלאי > טעינת מלאי מאקסל: `item_code`, `inventory_code` (חובה), `inventory_quantity`, `title1` (+ סוג מלאי "כמות").

## דוחות
- הגדרות > **דוחות**: דוח מכירות, דוח מוצרים ("הפקת הדוח" → נשלח למייל מנהל). **פרימיום** (דגל 136): טווח תאריכים + חיפוש (שם מוצר/קטגוריה) — למשל מיילים של קונים של מוצר מסוים (לבדוק `newsletter_msg`).
- "דוח מכירות כולל פח זבל" + Pivot ב-Sheets: מכירות לפי קופון של משפיען (`order id`, `order_summary_payment`, סינון `product_code`).
- מסך כל המוצרים → ייצוא XML. מסך הזמנות → "שמירת ההזמנות לקובץ/לאקסל/לטקסט" (כולל שדות נוספים).
- קטלוג פייסבוק/רימרקטינג: `id, title, price, desc, product_brand, image1_path` + link=`domain/items/<id>`.
- Enhanced Ecommerce (GA): הייבריד "אנליטיקס מורחב" — מטבע, מזהה מוצר (מק"ט/ID), אירועים (impressions, clicks, details, add/remove, promotions, checkout, purchase); דורש איחוד דומיינים.
- ייצוא חוות דעת/שאלות-תשובות ודפים: סקריפט קונסול בדפדפן (מאמרים פנימיים).
- השלמה אוטומטית עיר/רחוב: מבוססת קבצי data.gov.il (יישובים/רחובות).
