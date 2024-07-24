import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Trendyol hesap bilgileri
kullanici_bilgileri = [
{"email": "fredrick62305@7tqsgug.cashbenties.com", "sifre": "a123456"},
{"email": "kristi25744@seg2d1u.crankymonkey.info", "sifre": "a123456"},
]

def trendyol_giris(email, sifre):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.trendyol.com/giris?cb=%2F")
        time.sleep(2)

        email_input = driver.find_element(By.CSS_SELECTOR, ".q-input-wrapper.email-input input#login-email")
        email_input.send_keys(email)

        sifre_input = driver.find_element(By.ID, "login-password-input")
        sifre_input.send_keys(sifre)

        giris_yap_btn = driver.find_element(By.CSS_SELECTOR, "button.q-primary.q-fluid.q-button-medium.q-button.submit[type='submit'] span")
        giris_yap_btn.click()
        time.sleep(3)

        return driver

    except Exception as e:
        print("Giriş yapılırken hata oluştu:", e)
        return None

def urunu_begendir(kullanici_bilgileri):
    for kullanici in kullanici_bilgileri:
        email = kullanici["email"]
        sifre = kullanici["sifre"]
        driver = trendyol_giris(email, sifre)
        if driver:
            try:
                urun_url = "https://www.trendyol.com/pd/aron-atelier/kadin-vizon-taba-bambu-astarli-kilitli-model-omuz-cantasi-p-815934898?boutiqueId=61&merchantId=950418&filterOverPriceListings=false"
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
                for _ in range(10):
                    driver.get(urun_url)
                    sepete_ekle_butonu = driver.find_element(By.CSS_SELECTOR, "button.add-to-basket")
                    sepete_ekle_butonu.click()
                    time.sleep(2)


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

def main():
    chunk_size = 10  # Her bir iterasyonda kaç kullanıcı işlenecek
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(0, len(kullanici_bilgileri), chunk_size):
            chunk = kullanici_bilgileri[i:i+chunk_size]
            executor.submit(urunu_begendir, chunk)

if __name__ == "__main__":
    main()
