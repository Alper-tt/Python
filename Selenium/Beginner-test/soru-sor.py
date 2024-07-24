import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random

soru_havuzu = [
    "Çantanın ölçüleri neler?",
    "Ürün ebatları nedir?",
    "Ürünün fermuarları bozulur mu?",
    "Arkadaşım aldı çantanın kalitesi güzeldi bende sipariş verdim.",
    "ürünün kaç bölmesi var?",
    "ürünün askısı sağlam mı?",
    "ben aldım çantanın aksesuarları çok güzel tavsiye ederim.",
    "Askı boyu ayarlanabilir mi?",
    "Çantanın içinde astar var mı?",

    # Diğer soruları ekleyin
]


def rastgele_soru_sec(soru_havuzu):
    return random.choice(soru_havuzu)


def trendyol_giris(driver, email, sifre):
    try:
        driver.get("https://www.trendyol.com/giris")  # Trendyol giriş sayfasına git
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

        return True  # Giriş başarılı

    except Exception as e:
        print("Giriş yapılırken hata oluştu:", e)
        return False  # Giriş başarısız


def soru_sor(driver):
    kullanici_bilgileri = [
            {"email": "cuxogady@clip.lat", "sifre": "a123456"},
    
        # Buraya diğer kullanıcı bilgilerini ekleyebilirsiniz
    ]

    for kullanici in kullanici_bilgileri:
        # Tarayıcı başlatma
        options = Options()
        options.headless = True  # Headless modu etkinleştir
        driver = webdriver.Chrome(options=options)

        # Trendyol'a giriş yap
        if trendyol_giris(driver, kullanici["email"], kullanici["sifre"]):
            try:
                # Soru sorma sayfasına git
                soru_sayfasi_url = "https://www.trendyol.com/pekmoda/kadin-krem-kaliteli-kapitone-desenli-baguette-canta-p-747217474/saticiya-sor?merchantId=681697&showSelectedSeller=true"
                driver.get(soru_sayfasi_url)
                time.sleep(2)

                # Satıcıya sor butonunu bul ve tıkla
                satıcıya_sor_butonu = driver.find_element(By.XPATH, "//button[contains(text(), 'Satıcıya Sor')]")
                satıcıya_sor_butonu.click()
                time.sleep(2)

                # Rastgele bir soru seç
                soru = rastgele_soru_sec(soru_havuzu)

                # Metin kutusunu bul ve içeriğini yaz
                metin_kutusu = driver.find_element(By.CSS_SELECTOR, ".create-question-form textarea")
                metin_kutusu.send_keys(soru)
                time.sleep(2)

                # Checkbox'u bul         

                # Gönder butonunu bul ve tıkla
                gonder_butonu = driver.find_element(By.XPATH, "//div[contains(text(), 'Gönder')]")
                gonder_butonu.click()
                time.sleep(2)

            except NoSuchElementException:
                print("Satıcıya sor butonu bulunamadı veya gönder butonuna tıklanamadı.")

            except Exception as e:
                print("Soru sorma işlemi sırasında bir hata oluştu:", e)

            finally:
                # Tarayıcıyı kapat
                driver.quit()


def main():
    # Tarayıcı başlatma
    options = Options()
    options.headless = True  # Headless modu etkinleştir
    driver = webdriver.Chrome(options=options)

    # Soru sorma fonksiyonunu çağır
    soru_sor(driver)

    # Tarayıcıyı kapat
    driver.quit()


if __name__ == "__main__":
    main()
