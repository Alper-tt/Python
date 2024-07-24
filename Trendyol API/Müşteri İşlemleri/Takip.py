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
url = "https://public-sdc.trendyol.com/discovery-sellerstore-webgw-service/v1/follow/"

# Tokenların tutulduğu dosyanın adı
kullanıcı_dosyası = "/Users/alper/Desktop/users/all_users.json"

proxy_dosyasi = "/Users/alper/Desktop/APİ-trendyol/proxies.json"

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())

# Çerezler
cookies = {
    "__cflb": "02DiuFZUeLzKFPhAsPyKWhihyrZVnQpduXsCFL3ZrXZN4",
    "__cfruid": "beea2cbba89245c04fe3d666e516605734bfc1cd-1717263970",
    "_cfuvid": "h43fLBA9LefUZAFY6SRzCCgJKF0Zk7YRCgqZDOpNGC0-1717263970302-0.0.1.1-604800000"
}

seller_ID = [946618]


def proxy_formatla(proxy):
    return f"http://{proxy}"

def api_istegi(token, proxy, seller_ID):
    # Headers'ı her istekte güncellemek
    updated_headers = headers.copy()
    updated_headers.update({"Authorization": f"Bearer {token}"})

    # Gönderilecek veriler
    params = {
        "channelId": 1,
        "sellerId" : seller_ID

    }
    
    proxies = {
        "http": (proxy),
        "https": (proxy)
    }
    session = requests.Session()
    session.headers.update(updated_headers)
    session.cookies.update(cookies)

    try:
        # POST isteği gönderme
        response = session.post(url, params=params, proxies=proxies)

        # Cevabı kontrol etme
        if response.status_code == 201:
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

# Kullanıcıları dosyadan oku
with open(kullanıcı_dosyası, 'r') as dosya:
    kullanıcılar = json.load(dosya)

proxy_index = 0
kullanıcı_index = 25000

with ThreadPoolExecutor(max_workers=10) as executor:  # Paralel iş parçacığı sayısını ayarlayın

    while kullanıcı_index < 31423:

        for magaza in seller_ID:
            proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
            token = kullanıcılar[kullanıcı_index].get("token")
            executor.submit(api_istegi, token, proxy, seller_ID)
            proxy_index += 1
            print(kullanıcı_index)
            time.sleep(0.1)
        kullanıcı_index += 1