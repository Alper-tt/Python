import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json

# Header bilgileri
headers = {
    "culture": "tr-TR",
    "storefront-id": "1",
    "application-id": "1",
    "Content-Type": "application/json"
}

# API endpoints
add_to_basket_url = "https://public-mdc.trendyol.com/discovery-web-checkout-service/api/basket/v2/add?culture=tr-TR&storefrontId=1"
product_detail_url_template = "https://public.trendyol.com/discovery-web-productgw-service/api/productDetail/{product_id}?sav=false&storefrontId=1&culture=tr-TR&linearVariants=true&isLegalRequirementConfirmed=false"

# Tokenların tutulduğu dosyanın adı
kullanıcı_dosyası = "/Users/alper/Desktop/users/1/aktif_kullanıcılar.json"
proxy_dosyasi = "/Users/alper/Desktop/APİ-trendyol/proxies.json"

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())

# Çerezler
cookies = {
    "__cflb": "02DiuFZUeLzKFPhAsPyKWhihyrZVnQpduXsCFL3ZrXZN4",
    "__cfruid": "beea2cbba89245c04fe3d666e516605734bfc1cd-1717263970",
    "_cfuvid": "h43fLBA9LefUZAFY6SRzCCgJKF0Zk7YRCgqZDOpNGC0-1717263970302-0.0.1.1-604800000"
}

# Gönderilecek veriler
def proxy_formatla(proxy):
    return f"http://{proxy}"

def api_istegi(token, proxy, data):
    # Headers'ı her istekte güncellemek
    updated_headers = headers.copy()
    updated_headers.update({"Authorization": f"Bearer {token}"})
    
    proxies = {
        "http": proxy,
        "https": proxy
    }
    session = requests.Session()
    session.headers.update(updated_headers)
    session.cookies.update(cookies)

    try:
        # POST isteği gönderme
        response = session.post(add_to_basket_url, json=data, proxies=proxies)

        # Cevabı kontrol etme
        if response.status_code == 200:
            # Başarılı istek
            print(f"{proxy} - Başarılı - {response.status_code} - {response.text} - {token}")
        elif response.status_code == 400:
            # Hatalı istek
            print(f"{proxy} - 400 Hatası - {response.text}")
        elif response.status_code == 401:
            # Yetkilendirme hatası
            print(f"{proxy} - 401 Hatası: Yetkilendirme hatası - {token}")
        else:
            # Diğer hata durumları
            print(f"{proxy} - Hata - {response.status_code} - {token} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{proxy} - İstek sırasında bir hata oluştu - {e}")

def fetch_product_details(product_id):
    url = product_detail_url_template.format(product_id=product_id)
    response = requests.get(url)
    if response.status_code == 200:
        product_details = response.json()
        result = product_details.get('result', {})
        return {
            "listingId": result.get("listingId"),
            "merchantId": result.get("merchant", {}).get("id", 0),
            "campaignId": result.get("campaign", {}).get("id", 0),
            "contentId": result.get("id"),
            "channelId": 1,
            "quantity": 1
        }
    else:
        print(f"Ürün ID {product_id} için detaylar getirilemedi: {response.status_code}")
        return None

# Tokenları dosyadan oku
with open(kullanıcı_dosyası, 'r') as dosya:
    kullanıcılar = json.load(dosya)

# Ürün ID'lerini içeren liste
urun_ID = [844924615, 844924588, 844924569, 844924544, 844924539]

# Ürün detaylarını al ve urun_data listesini oluştur
urun_data = []
for product_id in urun_ID:
    product_detail = fetch_product_details(product_id)
    if product_detail:
        urun_data.append(product_detail)

proxy_index = 0
kullanıcı_index = 0

with ThreadPoolExecutor(max_workers=5) as executor:  # Paralel iş parçacığı sayısını ayarlayın
    while kullanıcı_index < 13403:
        for data in urun_data:
            proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
            token = kullanıcılar[kullanıcı_index].get("token")
            executor.submit(api_istegi, token, proxy, data)
            proxy_index += 1
            print(kullanıcı_index)
            time.sleep(0.1)  # İsteğin gönderilme süresini kontrol etmek için bekleme süresi
        kullanıcı_index += 1
