import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Döngüyü başlat
for _ in range(10):
    # Selenium web sürücüsünü başlat
    driver = webdriver.Chrome()

    try:
        # www.trendyol.com adresine git
        driver.get("https://www.trendyol.com")

        # Kadın seçeneğini tıkla
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='KADIN']"))
        ).click()

        time.sleep(1)

        # Arama kutusunu bul
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Aradığınız ürün, kategori veya markayı yazınız']"))
        )

        # "rosmod kadın krem kanvas" metnini yazıp arama yap
        search_box.send_keys("rosmod kadın krem kanvas" + Keys.RETURN)

        time.sleep(2)

        # Sayfayı yenile
        driver.refresh()

        time.sleep(2)

        # Ürünü bul
        product = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href='/rosmod/kadin-krem-kanvas-capraz-askili-mini-the-tote-bag-el-omuz-canta-p-789461736?boutiqueId=61&merchantId=868857']"))
        )

        # Ürüne tıkla
        product.click()

        # Ürünün açıldığı sekmeyi sakla
        product_tab = driver.window_handles[-1]
        # Ana sekme ile ürünün açıldığı sekmeyi değiştir
        driver.switch_to.window(product_tab)

        time.sleep(2)

        # Sayfayı yenile
        driver.refresh()

        time.sleep(2)

        # Sepete ekle butonuna 10 kez tıkla
        for _ in range(10):
            add_to_cart_button = driver.find_element(By.XPATH, "//button[contains(., 'Sepete Ekle')]")
            add_to_cart_button.click()
            time.sleep(2)

    finally:
        # İşlem tamamlandığında tarayıcıyı kapat
        driver.quit()
