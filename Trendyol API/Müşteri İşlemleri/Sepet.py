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


# API endpoint
url = "https://public-mdc.trendyol.com/discovery-web-checkout-service/api/basket/v2/add?culture=tr-TR&storefrontId=1"

# Tokenların tutulduğu dosyanın adı
kullanıcı_dosyası = "/kullanıcı/dosyası/yolu.json"
proxy_dosyasi = "/proxy/dosyası/yolu.json"

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())



# Çerezler
cookies = {
    "__cflb": "02DiuFZUeLzKFPhAsPyKWhihyrZVnQpduXsCFL3ZrXZN4",
    "__cfruid": "beea2cbba89245c04fe3d666e516605734bfc1cd-1717263970",
    "_cfuvid": "h43fLBA9LefUZAFY6SRzCCgJKF0Zk7YRCgqZDOpNGC0-1717263970302-0.0.1.1-604800000"
}


urun_data = [{
    "channelId": 1,
    "campaignId" : 61,
    "contentId" : 780622968,
    "listingId" : "cc9d954680eb2b307d9519449fbd1069",
    "merchantId" : 946618,
    "quantity" : 1},
    
    {
    "channelId": 1,
    "campaignId" : 61,
    "contentId" : 780622968,
    "listingId" : "cc9d954680eb2b307d9519449fbd1069",
    "merchantId" : 946618,
    "quantity" : 1}

    ]

# Gönderilecek veriler

def proxy_formatla(proxy):
    return f"http://{proxy}"

def api_istegi(token, proxy, data):
    # Headers'ı her istekte güncellemek
    updated_headers = headers.copy()
    updated_headers.update({"Authorization": f"Bearer {token}"})
    
    proxies = {
        "http": (proxy),
        "https": (proxy)
    }
    session = requests.Session()
    session.headers.update(updated_headers)
    session.cookies.update(cookies)

    try:
        # POST isteği gönderme
        response = session.post(url, json=data, proxies=proxies)

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

# Tokenları dosyadan oku
with open(kullanıcı_dosyası, 'r') as dosya:
    kullanıcılar = json.load(dosya)

proxy_index = 0
kullanıcı_index = 0

with ThreadPoolExecutor(max_workers=7) as executor:  # Paralel iş parçacığı sayısını ayarlayın

    while kullanıcı_index < 1224:
        for data in urun_data:
            proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
            token = kullanıcılar[kullanıcı_index].get("token")
            executor.submit(api_istegi, token, proxy, data)
            proxy_index += 1
            print(kullanıcı_index)
            time.sleep(0.1)  # İsteğin gönderilme süresini kontrol etmek için bekleme süresi
        kullanıcı_index+=1