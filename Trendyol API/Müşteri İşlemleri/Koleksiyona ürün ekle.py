import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json

# API endpoint
create_collection_url = "https://public-mdc.trendyol.com/discovery-web-recogw-service/api/collections/create"

# Tokenların tutulduğu dosyanın adı
token_dosyasi = "/token/dosyası/yolu.json"

proxy_dosyasi = "/proxy/dosyası/yolu.json"

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())

# Gönderilecek veriler
collection_body = {
    "collectionName": "Elbise Koleksiyonum"
}

content_ids = [
  {"contentId": 834970302},
    #Diğer ürün ID'lerini girebilirsiniz
]


def proxy_formatla(proxy):
    return f"http://{proxy}"

def koleksiyon_olustur(token, proxy):
    proxies = {
        "http": proxy_formatla(proxy),
        "https": proxy_formatla(proxy)
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(create_collection_url, headers=headers, json=collection_body, proxies=proxies)

        if response.status_code == 200 and response.json().get("isSuccess"):
            collection_id = response.json()["result"]["collectionId"]
            koleksiyona_urun_ekle(token, proxy, collection_id)
        else:
            print(f"{proxy} - Koleksiyon Oluşturma Hatası - {response.status_code} - {response.text} - {token}")
    except requests.exceptions.RequestException as e:
        print(f"{proxy} - İstek sırasında bir hata oluştu - {e}")

def koleksiyona_urun_ekle(token, proxy, collection_id):
    collection_url = f"https://public-mdc.trendyol.com/discovery-web-recogw-service/api/collection/{collection_id}"
    proxies = {
        "http": proxy_formatla(proxy),
        "https": proxy_formatla(proxy)
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(collection_url, headers=headers, json=content_ids, proxies=proxies)

        if response.status_code == 200:
            print(f"{proxy} - Ürünler Koleksiyona Eklendi - {collection_id} - {token}")
        else:
            print(f"{proxy} - Ürün Ekleme Hatası - {response.status_code} - {response.text} - {token}")
    except requests.exceptions.RequestException as e:
        print(f"{proxy} - İstek sırasında bir hata oluştu - {e}")

# Tokenları dosyadan oku
with open(token_dosyasi, 'r') as dosya:
    tokenlar = json.load(dosya)

proxy_index = 0
token_index = 0

with ThreadPoolExecutor(max_workers=5) as executor:  # Paralel iş parçacığı sayısını ayarlayın
    while token_index < len(tokenlar):
        proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
        token = tokenlar[token_index]
        executor.submit(koleksiyon_olustur, token, proxy)
        proxy_index += 1
        token_index += 1
