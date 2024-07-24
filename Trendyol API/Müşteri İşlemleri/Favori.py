import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json

# API endpoint
url = "https://public-mdc.trendyol.com/discovery-web-recogw-service/api/favorites?storefrontId=1&culture=tr-TR&channelId=1"

# Tokenların tutulduğu dosyanın adı
kullanıcı_dosyası = "/kullanıcı/bilgileri/dosyası/yolu.json"

proxy_dosyasi = "/proxy/dosyası/yolu.json"

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())

urun_ID = [844924615, 844924588, 844924569, 844924544, 844924539]

# Gönderilecek veriler

def proxy_formatla(proxy):
    return f"http://{proxy}"

def api_istegi(token, proxy, urun):
    proxies = {
        "http": proxy_formatla(proxy),
        "https": proxy_formatla(proxy)
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    body = {
    "contentId": urun
    }
    try:
        response = requests.post(url, headers=headers, json=body, proxies=proxies)
        # Cevabı kontrol etme
        if response.status_code == 200:
            print(f"{proxy} - Başarılı - {response.status_code} - {response.text} - {token}")
        elif response.status_code == 400:
            print(f"{proxy} - 400 Hatası - {response.text}")
        elif response.status_code == 401:
            print(f"{proxy} - 401 Hatası: Yetkilendirme hatası - {token}")
        else:
            print(f"{proxy} - Hata - {response.status_code} - {token} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{proxy} - İstek sırasında bir hata oluştu - {e}")

# Kullanıcıları dosyadan oku
with open(kullanıcı_dosyası, 'r') as dosya:
    kullanıcılar = json.load(dosya)

proxy_index = 0
kullanıcı_index = 0

with ThreadPoolExecutor(max_workers=5) as executor:  # Paralel iş parçacığı sayısını ayarlayın

    while kullanıcı_index < 15321:
    
        for urun in urun_ID:
            proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
            token = kullanıcılar[kullanıcı_index].get("token")
            executor.submit(api_istegi, token, proxy, urun)
            proxy_index += 1
            print(kullanıcı_index)
            time.sleep(0.1)  # İsteğin gönderilme süresini kontrol etmek için bekleme süresi
        kullanıcı_index += 1