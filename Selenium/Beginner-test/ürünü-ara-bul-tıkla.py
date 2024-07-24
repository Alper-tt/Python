import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

while True:
    # Chrome WebDriver'ı başlat
    driver = webdriver.Chrome()

    try:
        # Trendyol web sitesine git
        driver.get("https://www.trendyol.com")

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='KADIN']"))
        ).click()

        time.sleep(1)

        # Arama kutusunu bul
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='suggestion']"))
        )
        time.sleep(1)

        # Arama kutusuna "cosser" yaz
        search_box.send_keys("cosser")

        # Arama sonuçlarını bekleyin
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='suggestions-container']"))
        )
        time.sleep(1)

        # İlgili mağaza öğesini bulun
        icon = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//img[contains(@alt, 'Cosser')]"))
        )

        # İkona tıkla
        icon.click()

        time.sleep(2)

        # Mağazada arama kutusunu bul
        search_box_in_store = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Mağazada Ara']"))
        )
        time.sleep(1)

        # Arama kutusuna "fötr şapka" yaz
        search_box_in_store.send_keys("cosser fötr şapka")
        time.sleep(1)

        # Enter tuşuna basarak aramayı gerçekleştir
        search_box_in_store.send_keys(Keys.ENTER)

        # Beklenmedik overlay öğesini ele almak için denetleme yapalım
        try:
            # Overlay öğesini belirli bir süre bekleyerek bul
            overlay_element = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".overlay"))
            )

            # Eğer overlay belirli bir süre içinde görünmez hale gelmezse, TimeoutException hatası alacağız
            # Bu durumda overlay öğesine tıklıyoruz
            overlay_element.click()

            time.sleep(2)

        except TimeoutException:
            # Overlay belirli bir süre içinde görünmez hale gelmezse, ürüne tıklıyoruz
            product = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href='https://www.trendyol.com/cosser/unisex-siyah-fotr-sapka-sert-kovboy-sapkasi-p-796489875?boutiqueId=61&merchantId=856570&filterOverPriceListings=false&sav=true']"))
            )

        # Ürüne tıkla
            product.click()

        time.sleep(5)

    finally:
        # Tarayıcıyı kapat
        driver.quit()



