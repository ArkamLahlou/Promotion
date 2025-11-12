# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import yaml
import time
import random
import hashlib # لاستخدامه كمعرف فريد بدلاً من hash() المباشر

# =========================================================
# ⚠️ مهم جداً: قم بتحديث هذه القوائم بالروابط الصحيحة
# =========================================================

# 1. قائمة الروابط الطويلة (Landing URLs) التي سيتم سحب البيانات منها (يجب أن يكون ترتيبها مطابقاً للقائمة الثانية)
PRODUCT_URLS = [
    "الرابط_الطويل_النهائي_للمنتج_1_من_المتصفح", 
    "الرابط_الطويل_النهائي_للمنتج_2_من_المتصفح", 
    "الرابط_الطويل_النهائي_للمنتج_3_من_المتصفح",
    "الرابط_الطويل_النهائي_للمنتج_4_من_المتصفح"
]

# 2. قائمة روابط الإحالة القصيرة (Affiliate URLs) التي سيتم وضعها في زر الشراء (يجب أن يكون ترتيبها مطابقاً للأولى)
AFFILIATE_URLS = [
    "https://s.click.aliexpress.com/e/_c4mrsRWb", 
    "https://s.click.aliexpress.com/e/_c3j3Tkft", 
    "https://s.click.aliexpress.com/e/_c3CVW26n",
    "https://s.click.aliexpress.com/e/_c3wXwMHz"
]

# =========================================================

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'ar-EG,ar;q=0.9',
    'Referer': 'https://ar.aliexpress.com/'
}

scraped_deals = []

def scrape_product(url, affiliate_link):
    """دالة لجلب وتحليل بيانات منتج واحد، مع ربطها برابط الإحالة."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # ملاحظة: محددات CSS قد تتغير. يجب التحقق منها.
        title_element = soup.find('h1', class_='product-title-text')
        title = title_element.text.strip() if title_element else "لم يتم العثور على العنوان"

        price_element = soup.find('div', class_='price-current')
        price = price_element.text.strip() if price_element else "0.00"
        
        image_meta = soup.find('meta', property='og:image')
        image_url = image_meta['content'] if image_meta and 'content' in image_meta.attrs else "لا يوجد رابط صورة"
        
        # استخدام hashlib لتوليد معرف فريد وثابت
        unique_id = hashlib.sha1(url.encode()).hexdigest()

        deal_data = {
            'id': unique_id, 
            'title_raw': title,
            'price_scraped': price,
            'image_url': image_url,
            'aliexpress_url': url,
            'exclusive_link': affiliate_link # الآن نستخدم رابط الإحالة الصحيح
        }
        
        print(f"✅ تم سحب بيانات المنتج: {title}")
        return deal_data

    except requests.RequestException as e:
        print(f"❌ خطأ في جلب الرابط {url}: {e}")
        return None
    except Exception as e:
        print(f"❌ خطأ في تحليل بيانات {url}: {e}")
        return None

def main():
    """الدالة الرئيسية لتشغيل السحب وحفظ البيانات."""
    
    # يجب أن تكون القائمتان متساويتين في الطول
    if len(PRODUCT_URLS) != len(AFFILIATE_URLS):
        print("❌ خطأ: يجب أن يكون عدد روابط السحب مساوياً لعدد روابط الإحالة.")
        return

    # التكرار على القوائم باستخدام الفهرس
    for i, url in enumerate(PRODUCT_URLS):
        affiliate_link = AFFILIATE_URLS[i]
        
        deal = scrape_product(url, affiliate_link)
        if deal:
            scraped_deals.append(deal)

        # الانتظار ببطء بين كل طلب لتجنب الحظر
        sleep_time = random.uniform(5, 15)
        print(f"😴 انتظار لـ {sleep_time:.2f} ثانية...")
        time.sleep(sleep_time)

    # حفظ النتائج في ملف YAML (لـ Jekyll)
    output_file = '_data/deals.yml'
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(scraped_deals, f, allow_unicode=True, sort_keys=False)
        
    print(f"\n🎉 انتهت العملية. تم حفظ {len(scraped_deals)} منتج في {output_file}")


if __name__ == "__main__":
    main()
