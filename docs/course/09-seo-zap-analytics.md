# SEO, מנועי השוואה (זאפ/עזריאלי), Google Analytics (35 מאמרים)

## SEO
- שדות SEO: מוצר (לשונית "גוגל": title, description, keywords — גם לחיפוש פנימי, slug), קטגוריה (שדות גוגל), דפים, תגים מוצגים, יצרנים, סינונים רוחביים. **title ברירת מחדל = כותרת** (גוגל ימשוך לבד). לשנות בהתייעצות עם מקדם.
- **SEO מתקדם** (דגל 44 "מאופשר SEO"): תבניות liquid לכותרות, למשל H1 של מוצר `{{item.title}}` בלי יצרן.
- הייבריד SEO לשינוי תגיות/מבנה (selector, tag, class, title, alt, attr, location before/after/wrap) — משפיע על עיצוב.
- מעבר אתר: **301** לכל המוצרים (אוטומטית דרך `prev_url`) + עד 300 דפים; דפים בלי הפניה → 404; העברת תגיות מטא ברובוט (חינם); העברת מאמרים בתשלום. לא לשנות מבנה קטגוריות/למחוק מוצרים בזמן המעבר.
- טעינת SEO גורפת לדפים/קטגוריות/יצרנים: הייבריד `update_model_records` (duplicate=27936) + Google Sheet (`model_name`: pages/store_categories/brand/store, `model_id`, `seo_title`, `seo_description`, `seo_keywords`), מחזיר backups.
- **דף לא נסרק?** אתר < 4 חודשים / דף < חודש — להמתין; נשלח לסריקה ב-Search Console?; noindex/nofollow (Ctrl+U); תגיות מטא; פקודת `site:`; תאריך סריקה אחרון; sitemap (דגל 231, priority < 1).
- חיפוש בממשק: id, code, second_code, title, desc, matching_models, visit_link, color_group, inventory, seo_keywords. באתר: id, code, second_code, title, desc, matching_models, seo_keywords (אפשר לצמצם ל-title/code/keywords).
- קוד רימרקטינג: אלמנט `element_general_remarketing` (conversion_id) או ב-foot (הגדרות > כללי). **המרות רכישה** → הגדרות > כללי סעיף 28 "תוכן דף תודה". בדיקה: Tag Assistant.
- שת"פ SEO: Angora Media (AskPavel).

## זאפ ומנועי השוואה (הגדרות > מנועי השוואת מחירים, `admin/edit_price_comparison`)
- **אתר מראה** (XML): נשלח לזאפ. שדות: PRODUCT_NAME (כותרת/כותרת לאתר מראה), CATALOG_NUMBER (מק"ט), DETAILS (תיאור), PRODUCT_URL, CURRENCY, PRICE (מחיר/מחיר לאתר מראה), SHIPMENT_COST (המשלוח הזול שאינו איסוף עצמי, או "מחיר משלוח לזאפ" — חייב להתקיים באתר), DELIVERY_TIME, WARRANTY, PRODUCT_TYPE, MANUFACTURER, IMAGE. סינונים לא משודרים.
- זאפ דורש **מסוף סליקה פעיל**.
- הצגה בזאפ: "תצוגה במנועי השוואה" (מוצר חייב להיות מוצג ומחיר > 0), במסך כל המוצרים או עדכון גורף **סעיף 9**.
- מוצר לא בזאפ: מוצג? מסומן? מופיע באתר המראה (Ctrl+F)? → שם/קטגוריה כמו בזאפ, פנייה בממשק החנויות של זאפ (sa.zap.co.il). שינוי שם קטגוריה → לעדכן את זאפ.
- **רובוט זאפ** (`admin/zap_items`): שם החנות בזאפ, מיקום יעד, שינוי מחיר מקסימלי, סריקה אוטומטית. "הוספת נסרקים חדשים": כתובת זאפ (`zap.co.il/model.aspx?modelid=...`) + **מחיר מינימום** (חובה). "נסרקים": סוג סריקה (ידני/אוטומטי/הסרה), תוכנית פר מוצר, מחיר מומלץ, סריקה / סריקה ועדכון, "שנה למחיר זה בסריקה הבאה". זאפ מחשב מחיר **כולל משלוח**. מינימום גורף (רק לנסרקים חדשים) או CSV `price_limit`.
- מכירה אישית בזאפ: קטגוריה "מכירות אישיות" עם `OPEN_PRICE`; להוריד "תצוגה במנועי השוואה" כדי שלא יופיע כפול.
- **עזריאלי / Buy2**: דגלים 54 + 267 (מרקטפלייס); תג בשם בדיוק `buy2`; "עדכן שידור מוצרים לעזריאלי"; מלאי: פנימי / מטריצה (סכום) / גנרי (דגל 301 `orderlimit - azrieli`); איש קשר סער 052-605-9008.
- **מרקטפלייס זאפ**: התקנה `admin/apps/zap_marketplace_installation` + דגל 303 (פיד V2 `app.konimbo.co.il/api/v2?storeId=...&token=...&groupName=group1&modelName=item&itemIds=`). שדות נוספים: `ZAPISZAPPRODUCT` (1/0), `ZAPISMARKETPLACEPRODUCT` (1/0), WarrantyBy, ZAPMinQuantityAlert, ZAPMaxItemsInOrder, ZAPLeadTimeToShip, ZAPInstallationcost, ZAPIsPickup, **ZAPLogisticClass** (EX_S ≤2.5 ק"ג / S ≤5 ק"ג 30 ס"מ / M / L 5-20 ק"ג / Free / OV..OV5 / SPD), ZAPProductFreeParamInfo (תוכן עשיר מופרד ב-`###`), ZAPTermsAndConditions — דרך CSV `data_record_<field>`.
- **דילים** (דיל עם טיימר) — אתר מראה נפרד; **generalxml** — אתר מראה מותאם (תג `generalxml` + שדה `generalxml_price`, 250 ₪).
- חוות דעת זאפ: דפי החנות > "חוות דעת זאפ" (העתקה ידנית).

## Google Analytics 4
- יצירת נכס GA4 → Data Streams → הפעלת "Collect Universal Analytics events" → **List unwanted referrals**: הדומיין, paypal.com, cgmpi.creditguard.co.il, pps.creditguard.co.il, `<sub>.konimbo.co.il`, secure.konimbo.co.il, masterpass.com, mycheck.co.il → העתקת Measurement ID → התקנת תוסף GA4 בחנות (הייבריד "אנליטיקס 4") → שמירת נתונים 14 חודשים.
- רכישות פייפאל נספרות רק עם **חזרה אוטומטית לדף תודה** (אירוע הרכישה נשלח מדף התודה).
- מתן גישה: Admin > Account access management > +.
