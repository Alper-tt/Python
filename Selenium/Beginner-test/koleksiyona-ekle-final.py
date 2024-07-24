import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Kullanıcı bilgileri
kullanici_bilgileri = [
    {"email": "leanor93940@uh39osxk.cse445.com", "sifre": "a123456"},
    # Diğer kullanıcılar...
]

koleksiyona_ekleyen_sayısı = 0
toplam_kullanici=len(kullanici_bilgileri)

# Ürün havuzu
urunler = [
    "https://www.trendyol.com/frondcase/samsung-s23-fe-lavanta-desenli-seffaf-telefon-kilifi-p-788724719?merchantId=268885",
    "https://www.trendyol.com/frondcase/samsung-s24-lavanta-desenli-seffaf-telefon-kilifi-p-800921109?merchantId=268885",
    "https://www.trendyol.com/frondcase/samsung-s23-kadin-cicek-seffaf-telefon-kilifi-p-726671102?merchantId=268885",
    "https://www.trendyol.com/frondcase/samsung-s24-plus-lavanta-desenli-seffaf-telefon-kilifi-p-800787777?merchantId=268885",
    "https://www.trendyol.com/frondcase/samsung-s23-fe-panda-telefon-kilifi-p-788724431?merchantId=268885",
    "https://www.trendyol.com/frondcase/samsung-s23-fe-kadin-cicek-siyah-telefon-kilifi-p-789270238?merchantId=268885",
    "https://www.trendyol.com/frondcase/samsung-s23-kelebek-seffaf-telefon-kilifi-p-782437221?merchantId=268885",
    "https://www.trendyol.com/frondcase/samsung-s23-fe-women-art-kirmizi-telefon-kilifi-p-789270030?merchantId=268885",


    # Diğer ürünler...
]

def koleksiyon_olustur(email, sifre):
    global koleksiyona_ekleyen_sayısı
    # Tarayıcı başlatma
    options = Options()
    options.headless = True  # Arka planda çalışacak şekilde ayarla
    driver = webdriver.Chrome(options=options)

    try:
        # Trendyol'a giriş yap
        driver.get("https://www.trendyol.com/giris?cb=%2F")
        # Giriş bilgilerini doldur
        time.sleep(1)
        email_input = driver.find_element(By.ID, "login-email")
        email_input.send_keys(email)
        password_input = driver.find_element(By.ID, "login-password-input")
        password_input.send_keys(sifre)
        login_button = driver.find_element(By.CSS_SELECTOR, ".q-primary.q-fluid.q-button-medium.q-button.submit[type='submit']")
        login_button.click()
        time.sleep(1)  # Giriş tamamlanana kadar bekle

        # Ürünleri ziyaret et ve koleksiyona ekle
        for urun_url in urunler:
            driver.get(urun_url)
            time.sleep(1)
            driver.get(urun_url)
            time.sleep(1)

            # Koleksiyon ekle butonuna tıkla
            # Koleksiyon ekle butonuna tıkla
            collection_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Koleksiyona Ekle')]")
            collection_button.click()
            time.sleep(1)


            # Popup'ın yüklenmesini bekle
            popup = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "collect-popup")))

            # Koleksiyon adını kontrol et
            koleksiyon_adi = "samsung kılıf"
            if not koleksiyon_mevcut(driver, koleksiyon_adi):
                # Yeni koleksiyon oluştur
                yeni_koleksiyon_olustur(driver, koleksiyon_adi)
            else:
                # Mevcut koleksiyonu seç
                mevcut_koleksiyon_sec(driver, koleksiyon_adi)

            # Koleksiyona eklenen sayısını artır
            koleksiyona_ekleyen_sayısı += 1

    except Exception as e:
        print(f"Hata oluştu: {e}")

    finally:
        # Tarayıcıyı kapat
        driver.quit()

def koleksiyon_mevcut(driver, koleksiyon_adi):
    try:
        # Koleksiyon adının olduğu elementi bul
        driver.find_element(By.XPATH, f"//p[@class='collection-name' and contains(text(), '{koleksiyon_adi}')]").click()
        return True
    except:
        return False

def yeni_koleksiyon_olustur(driver, koleksiyon_adi):
    # Yeni koleksiyon oluştur butonuna tıkla
    new_collection_button = driver.find_element(By.CSS_SELECTOR, ".create-new-collection .i-plus-bold")
    new_collection_button.click()
    time.sleep(1)

    # Koleksiyon adını gir
    collection_input = driver.find_element(By.CSS_SELECTOR, ".collection-input")
    collection_input.clear()  # Önce mevcut değeri temizle
    collection_input.send_keys(koleksiyon_adi)
    time.sleep(1)

    # Koleksiyon oluştur butonuna tıkla
    create_button = driver.find_element(By.CSS_SELECTOR, ".collection-submit-button")
    create_button.click()
    time.sleep(1)
    print(f"{koleksiyon_adi} adında yeni bir koleksiyon oluşturuldu.")

def mevcut_koleksiyon_sec(driver, koleksiyon_adi):
    # Koleksiyon adını içeren elementi tıkla
    driver.find_element(By.XPATH, f"//p[@class='collection-name' and contains(text(), '{koleksiyon_adi}')]").click()
    print(f"{koleksiyon_adi} adındaki mevcut koleksiyon seçildi.")
    time.sleep(2)

def plot_live_data():
    global koleksiyona_ekleyen_sayısı

    while True:
        plt.clf()
        # Verileri bar grafiği olarak göster
        plt.bar(["koleksiyone ekleyen", "İşlenen Kullanıcı(%)"], [koleksiyona_ekleyen_sayısı, ((koleksiyona_ekleyen_sayısı * 100) / toplam_kullanici)])

        plt.title("Trendyol İşlem Dağılımı")
        plt.xlabel("İşlem Türü")
        plt.ylabel("Kullanıcı Sayısı")
        plt.draw()
        plt.pause(5)

def main():

    with ThreadPoolExecutor(max_workers=10) as executor:
        for kullanici in kullanici_bilgileri:
            executor.submit(koleksiyon_olustur, kullanici["email"], kullanici["sifre"])
        plot_live_data()

if __name__ == "__main__":
    main()
