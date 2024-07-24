import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt


# Trendyol hesap bilgileri
kullanici_bilgileri = [
    {
        "email": "zidnbbimwadmh@gmail.com",
        "sifre": "A123456789a",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdGFuZGFyZFVzZXIiOiIwIiwidW5pcXVlX25hbWUiOiJ6aWRuYmJpbXdhZG1oQGdtYWlsLmNvbSIsInN1YiI6InppZG5iYmltd2FkbWhAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJhdHdydG1rIjoiNDYwZDFkMTQtMzJkZS0xMWVmLWFlODctN2ViMDRmZDc4NWM5IiwidXNlcklkIjoiNDgzMTUzNjgiLCJlbWFpbCI6InppZG5iYmltd2FkbWhAZ21haWwuY29tIiwiYXBwTmFtZSI6InR5IiwiYXVkIjoic2JBeXpZdFgramhlTDRpZlZXeTV0eU1PTFBKV0Jya2EiLCJleHAiOjE4NzcwOTk1NzEsImlzcyI6ImF1dGgudHJlbmR5b2wuY29tIiwibmJmIjoxNzE5MzExNTcxfQ.S76-mBdR_Bc1YFrlVa6pBYqVOUgtqqazIzJirjOfxx8"
    },
]

takip_edilen_mağaza_sayısı = 0
favoriye_eklenen_ürün_sayısı = 0
sepete_eklenen_ürün_sayısı = 0
islenen_kullanici=0
toplam_kullanici_sayisi = len(kullanici_bilgileri)

def trendyol_giris(email, sifre):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.trendyol.com/giris?cb=%2F")
        time.sleep(1)

        email_input = driver.find_element(By.CSS_SELECTOR, ".q-input-wrapper.email-input input#login-email")
        email_input.send_keys(email)

        sifre_input = driver.find_element(By.ID, "login-password-input")
        sifre_input.send_keys(sifre)

        giris_yap_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'q-primary') and contains(@class, 'q-fluid') and contains(@class, 'q-button-medium') and contains(@class, 'q-button') and contains(@class, 'submit')]/span")
        time.sleep(1)
        giris_yap_btn.click()
        time.sleep(2)


        return driver

    except Exception as e:
        print("Giriş yapılırken hata oluştu:", e)
        return None

def urunu_begendir(kullanici_bilgileri):
    global takip_edilen_mağaza_sayısı
    global favoriye_eklenen_ürün_sayısı
    global sepete_eklenen_ürün_sayısı
    global islenen_kullanici

    for kullanici in kullanici_bilgileri:
        email = kullanici["email"]
        sifre = kullanici["sifre"]
        driver = trendyol_giris(email, sifre)
        time.sleep(2)
        if driver:
            try:
                urun_url = "https://www.trendyol.com/rosmod/kadin-siyah-dugmeli-model-omuz-ve-kol-cantasi-p-789348427?boutiqueId=61&merchantId=868857"
                driver.get(urun_url)
                time.sleep(1)
                driver.get(urun_url)
                time.sleep(1)

                # Favori butonunu kontrol et
                favori_butonu = driver.find_element(By.CSS_SELECTOR, ".favorite-button button.fv")
                favori_icon = favori_butonu.find_element(By.CSS_SELECTOR, "i")

                # Eğer favori butonunda "i-heart-orange" sınıfı varsa zaten favoride, tekrar tıklamaya gerek yok
                if "i-heart-orange" in favori_icon.get_attribute("class"):
                    print("Ürün zaten favorilerde.")
                else:
                # Favoriye ekle butonuna tıkla
                    favori_butonu.click()

                time.sleep(2)

                # Sepete ekle butonunu bul
                for _ in range(1):
                    driver.get(urun_url)
                    sepete_ekle_butonu = driver.find_element(By.CSS_SELECTOR, "button.add-to-basket")
                    sepete_ekle_butonu.click()
                    time.sleep(2)

                driver.get(urun_url)
                takip_et_butonu = driver.find_element(By.CSS_SELECTOR, ".follow-btn")
                takip_et_durum = takip_et_butonu.get_attribute("class")
                if "followed" in takip_et_durum:
                    print("Mağaza zaten takip ediliyor.")
                else:
                    takip_et_butonu.click()        
                time.sleep(2)
      
            except Exception as e:
                print("Ürün beğenirken veya sepete eklerken hata oluştu:", e)
            finally:
                driver.quit()

def plot_live_data():
    global takip_edilen_mağaza_sayısı
    global favoriye_eklenen_ürün_sayısı
    global sepete_eklenen_ürün_sayısı
    global islenen_kullanici

    while True:
        plt.clf()
        # Verileri bar grafiği olarak göster
        plt.bar(["Takip Edilen Mağaza", "Favoriye Eklendi", "Sepete Eklendi", "İşlenen Kullanıcı"], [takip_edilen_mağaza_sayısı, favoriye_eklenen_ürün_sayısı, sepete_eklenen_ürün_sayısı,((islenen_kullanici*100)/(toplam_kullanici_sayisi))
])
        
        plt.title("Trendyol İşlem Dağılımı")
        plt.xlabel("İşlem Türü")
        plt.ylabel("Kullanıcı Sayısı")
        plt.draw()
        plt.pause(5)

def main():
    chunk_size = 10  # Her bir iterasyonda kaç kullanıcı işlenecek
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(0, len(kullanici_bilgileri), chunk_size):
            chunk = kullanici_bilgileri[i:i+chunk_size]
            executor.submit(urunu_begendir, chunk)

        plot_live_data()

if __name__ == "__main__":
    main()
