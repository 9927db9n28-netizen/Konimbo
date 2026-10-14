# תהליכים, הקמה, מעבר אתר, מובייל, פונטים (24 מאמרים)

## 🎯 ספציפי לדינמיקה
- במאמר "הטמעת פונט עם קבצים" מוזכר האתר **dynamica**: הוטמעו פונטים מותאמים —
  `Roboto` רק לתו ₪ (`unicode-range: U+20AA`), `Poppins` רק לאותיות באנגלית (`U+0041-005A, U+0061-007A`), ו-`SimplerPro_V3` לשאר האתר:
  `body { font-family: 'Roboto','Poppins','SimplerPro_V3','Open Sans Hebrew',Arial,FontAwesome !important; }`
  הפונטים יושבים ב-S3 (`konimbo-stores/<store>/fonts/<font>`) ומוטמעים בהייבריד. **לא לשנות בלי לבדוק השפעה על העיצוב.**

## גרסת מובייל (אתרים קלאסיים בלבד)
- דגל "Mobile lazy" + בעריכת החנות `gauges_code` = `mobilenew` (או `mobilenew_speed` בשיפור ציון).
- אלמנטים מ-`mobilenewelements`: loading page, `main_nav_bg_mobilenew`, וייז (`waze://?ll=..&navigate=yes`), infinitescroll (חובה), color theme (צבע ראשי), `mobile_order_page`, עגלה צפה, הדר שחור (לוגו לבן), `mobile_css` (CSS ב-HEAD, JS ב-FOOT).
- אלמנטי דף הבית למובייל ב**קבוצה 11** (`homepage_layout_x`): סליידר bootstrap, `element_general_images` (קטגוריות מעוצבות 350×350), גריד מוצרים.
- דינמיקה — אם האתר רספונסיבי/Layout X, זה לא רלוונטי (לבדוק).

## קאש ועיצוב
- שינוי `main.css` לא נראה: CloudFront TTL של כמה שעות → הייבריד זמני; או להעביר CSS להייבריד ולשנות שם הקובץ; או query string עם תאריך ב-layout.
- תקלות "סקצ'" (מרכז דף הבית) — מסלול טיפול פנימי.

## הייברידים/פיתוחים שימושיים
- **רימרקטינג דינמי פייסבוק/גוגל** (תוסף בתשלום, הייבריד "Facebook Catalog Setup" מ-`paidplugins`): תג מוצרים → Feed URL דינמי (מתעדכן ~שעתיים); `category_dictionary` לקטגוריות גוגל; שגיאת GTIN/MPN → יצרן עם כותרת באנגלית; קידוד XML → `item.title` בתיאור.
- viplus (דיוור), BUYME (iframe בדף), כמות שדרוגים=כמות מוצר (דגל + הייבריד 14346).
- **מחיר ל-100 גרם/מ"ל** (חובה בחוק למזון/נוזלים): שדות נוספים "כמות" + "יחידת מידה"; CSV: `data_record_quantity`, `data_record_unit`.
- קישור חוות דעת זאפ בתבנית מייל: `http://www.zap.co.il/ratestoreForm.aspx?siteid=<id>&model={{order.all_item_titles}}&invoice={{order.invoice_code}}`.
- **קהילת מפתחים חיצונית**: קונימבו כבר לא מפתחים פיתוחים פרטניים — מפנים למפתחי Hybrid/API חיצוניים (ענת ציוני, גיא רביב, שחר סרגטה, טל/datalogics, איתמר שלח, RcBuilder). כל שינוי בהייבריד נשמר כגרסה (עד 30 אחורה), יש סביבת טסטים (subdomain). תוספים חינמיים: konimbo-plugins.co.il.

## הפניות 301 במעבר אתר (תהליך)
איסוף לינקים: ידני + GA (Landing pages 90 יום) + `site:domain` → מיפוי (VLOOKUP לפי כותרת) → לא נמצא = דף הבית ("לא קיים") → אישור לקוח → טעינה (בלי `s` ב-https, דומיין במקום subdomain). מגבלה **250 תווים** להפניה (לפענח עברית מקודדת), אין הפניה כפולה מאותו דף, הפניות מוצרים דרך `prev_url`.
- מעבר אתר מקודם: עם מקדם; לא לשנות שמות קטגוריות; לא למחוק תוכן חודשיים לפני/אחרי; שדרוגים וסינונים לא מועברים.
- מכירת עסק/החלפת דומיין: לנקות zone ישן ב-AWS, Search Console חדש וסריקה מחדש.

## Google Analytics (ישן UA) והקמה
- Referral exclusions (כמו ב-GA4), view settings: מטבע ₪, Site search parameter **`q`**, Ecommerce settings מופעלים. הרשאות: Admin > User Management.
- דשבורד לייב: service account של קונימבו מקבל Read & Analyze + view id.
- העלאת תמונות מרובות: לתיקיית החנות ב-S3 `konimbo-stores/<subdomain>/` (ציבורי) ואז CSV עם `imageN_path` (יש גם skill של Claude פנימי `konimbo-images-to-s3`).
