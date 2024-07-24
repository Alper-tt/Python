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
    {
        "email": "fksmpnptvrqte@gmail.com",
        "sifre": "A123456789a",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdGFuZGFyZFVzZXIiOiIwIiwidW5pcXVlX25hbWUiOiJma3NtcG5wdHZycXRlQGdtYWlsLmNvbSIsInN1YiI6ImZrc21wbnB0dnJxdGVAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJhdHdydG1rIjoiNDYwZjIzNGQtMzJkZS0xMWVmLTljNDUtMjIyMzkxNzg3Nzg5IiwidXNlcklkIjoiNDc5NTE0ODAiLCJlbWFpbCI6ImZrc21wbnB0dnJxdGVAZ21haWwuY29tIiwiYXBwTmFtZSI6InR5IiwiYXVkIjoic2JBeXpZdFgramhlTDRpZlZXeTV0eU1PTFBKV0Jya2EiLCJleHAiOjE4NzcwOTk1NzEsImlzcyI6ImF1dGgudHJlbmR5b2wuY29tIiwibmJmIjoxNzE5MzExNTcxfQ._boex1Ie1lcK00Z2q7-4ACTyDXSr2qdfg3qDUUPb-Ew"
    },
    {
        "email": "ljo_wdjebjioe@gmail.com",
        "sifre": "A123456789a",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdGFuZGFyZFVzZXIiOiIwIiwidW5pcXVlX25hbWUiOiJsam9fd2RqZWJqaW9lQGdtYWlsLmNvbSIsInN1YiI6Imxqb193ZGplYmppb2VAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJhdHdydG1rIjoiNDYwY2RmZGUtMzJkZS0xMWVmLTk0NTItYWU5ZjhiMjExNjRiIiwidXNlcklkIjoiNjIxNTAwODgiLCJlbWFpbCI6Imxqb193ZGplYmppb2VAZ21haWwuY29tIiwiYXBwTmFtZSI6InR5IiwiYXVkIjoic2JBeXpZdFgramhlTDRpZlZXeTV0eU1PTFBKV0Jya2EiLCJleHAiOjE4NzcwOTk1NzEsImlzcyI6ImF1dGgudHJlbmR5b2wuY29tIiwibmJmIjoxNzE5MzExNTcxfQ.-4r1uF7gXUIgNsLLKgHCKsZeUjPRiFzdmb2zVLsswVc"
    },

]

urunler = ["https://www.trendyol.com/munora-butik/kalp-yaka-etegi-kruvaze-beyaz-mini-elbise-p-680443966?merchantId=413287&filterOverPriceListings=false",
           "https://www.trendyol.com/munora-butik/ince-askili-gogusu-drapeli-siyah-saten-elbise-p-311170436?merchantId=413287&filterOverPriceListings=false",
           "https://www.trendyol.com/munora-butik/kadin-siyah-sirt-detayli-etegi-sortlu-elbise-p-298741286?merchantId=413287&filterOverPriceListings=false",
           "https://www.trendyol.com/rabia-celik/kadin-beyaz-cep-detayli-alt-ust-takim-p-833274792?merchantId=413287",
           "https://www.trendyol.com/rabia-celik/kruvaze-yaka-drapeli-sifon-siyah-min-elbise-p-834968636?merchantId=413287&filterOverPriceListings=false",
           "https://www.trendyol.com/rabia-celik/kadin-kirmizi-sirt-dekolteli-yirtmacli-elbise-p-834441821?merchantId=413287&filterOverPriceListings=false",
           "https://www.trendyol.com/munora-butik/askili-korse-gorunumlu-onu-dugme-detayli-siyah-mini-elbise-p-705398026?merchantId=413287&filterOverPriceListings=false",
           "https://www.trendyol.com/munora-butik/sirt-detayli-balik-kesim-maxi-boy-mavi-elbise-p-685204340?merchantId=413287&filterOverPriceListings=false",
           "https://www.trendyol.com/rabia-celik/kadin-pembe-omuzlari-baglamali-sirt-dekolteli-midi-elbise-p-833276394?merchantId=413287&filterOverPriceListings=false"]

def trendyol_giris(email, sifre):
    options = Options()
    #options.add_argument('--headless') #Programı pencere açmadan çalıştırır
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280x720')
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
        time.sleep(1)

        return driver

    except Exception as e:
        print("Giriş yapılırken hata oluştu:", e)
        return None

def urun_islemleri(driver):
    try:
        for urun_url in urunler:
            driver.get(urun_url)
            time.sleep(1)
            driver.refresh()

            takip_et_butonu = driver.find_element(By.CSS_SELECTOR, ".follow-btn")
            takip_et_durum = takip_et_butonu.get_attribute("class")
            if "followed" not in takip_et_durum:
                takip_et_butonu.click()
                print("Mağaza takip edildi.")
            time.sleep(1)

            driver.get(urun_url)
            favori_butonu = driver.find_element(By.CSS_SELECTOR, ".favorite-button button.fv")
            favori_icon = favori_butonu.find_element(By.CSS_SELECTOR, "i")
            if "i-heart-orange" not in favori_icon.get_attribute("class"):
                favori_butonu.click() 
                print("Ürün favorilere eklendi.")
            time.sleep(1)


            #Ürün içinde fotoğrafları sırasıyla geçer
            
            #driver.refresh()
            #gallery_icon = driver.find_element(By.CSS_SELECTOR, ".gallery-icon-container.right")
            #gallery_icon.click()
            #time.sleep(9)
            #gallery_icon.click()
            #time.sleep(5)

            driver.refresh()
            sepete_ekle_butonu = driver.find_element(By.CSS_SELECTOR, "button.add-to-basket")
            sepete_ekle_butonu.click()
            print("Ürün sepete eklendi.")
            time.sleep(1)

    except Exception as e:
        print("Ürün işlenirken hata oluştu:", e)

def urunu_begendir(kullanici):
    email = kullanici["email"]
    sifre = kullanici["sifre"]
    driver = trendyol_giris(email, sifre)
    if driver:
        urun_islemleri(driver)
        driver.quit()

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(urunu_begendir, kullanici_bilgileri)

if __name__ == "__main__":
    main()
