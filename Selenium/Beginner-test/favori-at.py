import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Trendyol hesap bilgileri
kullanici_bilgileri = [
 
    {"email": "cogiwa6748@aersm.com", "sifre": "a123456"},
    {"email": "herage6948@aersm.com", "sifre": "a123456"},
    # Buraya diğer kullanıcı bilgilerini ekleyebilirsiniz
]


def trendyol_giris(email, sifre):
    # Tarayıcı başlatma
    options = Options()
    options.headless = True  # Headless modu etkinleştir
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.trendyol.com/giris?cb=%2F")  # Trendyol giriş sayfasına git
        time.sleep(2)  # Sayfanın tam olarak yüklenmesini bekleyin

        # E-posta alanını doldur
        email_input = driver.find_element(By.CSS_SELECTOR, ".q-input-wrapper.email-input input#login-email")
        email_input.send_keys(email)
        time.sleep(2)  # Sayfanın tam olarak yüklenmesini bekleyin

        # Şifre alanını doldur
        sifre_input = driver.find_element(By.ID, "login-password-input")
        sifre_input.send_keys(sifre)
        time.sleep(2)  # Sayfanın tam olarak yüklenmesini bekleyin

        # Giriş yap düğmesine tıkla
        giris_yap_btn = driver.find_element(By.CSS_SELECTOR, "button.q-primary.q-fluid.q-button-medium.q-button.submit[type='submit'] span")
        giris_yap_btn.click()
        time.sleep(3)  # Girişin tam olarak gerçekleşmesini bekleyin

        return driver

    except Exception as e:
        print("Giriş yapılırken hata oluştu:", e)
        return None


def urunu_begendir(driver):
    try:
        # Ürüne gidin (örneğin, bir ürün sayfasının URL'sini kullanarak)
        urun_url = "https://www.trendyol.com/rosmod/kadin-siyah-organik-kanvas-kumas-capraz-canta-p-767638265?boutiqueId=61&merchantId=868857"
        driver.get(urun_url)

        time.sleep(2)

        driver.get(urun_url)

        time.sleep(1)

        # Favori butonunu bul
        favori_butonu = driver.find_element(By.CSS_SELECTOR, ".favorite-button button.fv")
        favori_butonu.click()
        time.sleep(2)

        # Sepete ekle butonunu bul
        for _ in range(10):
            driver.get(urun_url)
            sepete_ekle_butonu = driver.find_element(By.CSS_SELECTOR, "button.add-to-basket")
            sepete_ekle_butonu.click()
            time.sleep(2)


    except Exception as e:
        print("Ürün beğenirken veya sepete eklerken hata oluştu:", e)

##################################

    try:
        # Ürüne gidin (örneğin, bir ürün sayfasının URL'sini kullanarak)
        urun_url = "https://www.trendyol.com/cosser/unisex-siyah-fotr-sapka-sert-kovboy-sapkasi-p-796489875?boutiqueId=61&merchantId=663258"
        driver.get(urun_url)

        time.sleep(2)

        driver.get(urun_url)

        time.sleep(1)

        # Favori butonunu bul
        favori_butonu = driver.find_element(By.CSS_SELECTOR, ".favorite-button button.fv")
        favori_butonu.click()
        time.sleep(2)

        # Sepete ekle butonunu bul
        for _ in range(10):
            driver.get(urun_url)
            sepete_ekle_butonu = driver.find_element(By.CSS_SELECTOR, "button.add-to-basket")
            sepete_ekle_butonu.click()
            time.sleep(2)



    except Exception as e:
        print("Ürün beğenirken veya sepete eklerken hata oluştu:", e)

##################################


    try:
        # Ürüne gidin (örneğin, bir ürün sayfasının URL'sini kullanarak)
        urun_url = "https://www.trendyol.com/rosmod/kadin-bordo-rugan-capraz-askili-asimetrik-canta-p-810101014?boutiqueId=61&merchantId=868857"
        driver.get(urun_url)

        time.sleep(2)

        driver.get(urun_url)

        time.sleep(1)

        # Favori butonunu bul
        favori_butonu = driver.find_element(By.CSS_SELECTOR, ".favorite-button button.fv")
        favori_butonu.click()
        time.sleep(2)

        # Sepete ekle butonunu bul
        for _ in range(10):
            driver.get(urun_url)
            sepete_ekle_butonu = driver.find_element(By.CSS_SELECTOR, "button.add-to-basket")
            sepete_ekle_butonu.click()
            time.sleep(2)



    except Exception as e:
        print("Ürün beğenirken veya sepete eklerken hata oluştu:", e)

##################################
        

    try:
        # Ürüne gidin (örneğin, bir ürün sayfasının URL'sini kullanarak)
        urun_url = "https://www.trendyol.com/cosser/kadin-bordo-ozel-aski-detayli-kol-omuz-canta-p-801824054?boutiqueId=61&merchantId=856570&filterOverPriceListings=false&sav=true"
        driver.get(urun_url)

        time.sleep(2)

        driver.get(urun_url)

        time.sleep(1)

        # Favori butonunu bul
        favori_butonu = driver.find_element(By.CSS_SELECTOR, ".favorite-button button.fv")
        favori_butonu.click()
        time.sleep(2)

        # Sepete ekle butonunu bul
        for _ in range(10):
            driver.get(urun_url)
            sepete_ekle_butonu = driver.find_element(By.CSS_SELECTOR, "button.add-to-basket")
            sepete_ekle_butonu.click()
            time.sleep(2)

    except Exception as e:
        print("Ürün beğenirken veya sepete eklerken hata oluştu:", e)

##################################


def main():
    # Her bir kullanıcı için giriş yapın, ürünü beğendirin ve tarayıcıyı kapatın
    for kullanici in kullanici_bilgileri:
        driver = trendyol_giris(kullanici["email"], kullanici["sifre"])
        if driver:
            urunu_begendir(driver)
            driver.quit()  # Tarayıcıyı kapat
            print("Islem basarılı")


if __name__ == "__main__":
    main()
