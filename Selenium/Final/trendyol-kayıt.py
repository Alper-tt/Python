import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.action_chains import ActionChains
from lxml import html
import json
import concurrent.futures

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.87 Safari/537.36"
]

#kopeechka'dan aldığınız API Key'i aşağıya girmelisiniz
token = "123456"

# Chrome ayarları
def get_chrome_options():
    chrome_options = Options()
    chrome_options.add_extension('/Users/alper/Desktop/MPBJKEJCLGFGADIEMMEFGEBJFOOFLFHL_3_1_0_0.crx')
    user_agent = random.choice(user_agents)
    #chrome_options.add_argument(f"user-agent={user_agent}")
    #chrome_options.add_argument('--proxy-server=https://222.109.192.34:8080')
    return chrome_options

# API ile mail al ve id'yi al
def get_email():
    url = f'https://api.kopeechka.store/mailbox-get-email?site=www.trendyol.com&mail_type=OUTLOOK&token={token}&password=0&regex=&subject=&investor=&soft=&type=json&api=2.0'
    response = requests.get(url)
    json_data = response.json()
    print(json_data.get('mail'))
    print(json_data.get('id'))
    return json_data.get('mail'), json_data.get('id')

# Doğrulama kodunu almak için API'yi kullan
def get_verification_code(email_id):
    url = f'https://api.kopeechka.store/mailbox-get-message?id={email_id}&token={token}&full=0&type=json&api=2.0'
    response = requests.get(url)
    json_data = response.json()
    html_content = json_data.get('fullmessage', '')
    x=0
    while not html_content:
        print("tekrar deneniyor")
        time.sleep(5)
        response = requests.get(url)
        json_data = response.json()
        html_content = json_data.get('fullmessage', '')
        x+=5
        if(x>299):
            print("mail bulunamadı")
            break
    else:
        tree = html.fromstring(html_content)
        verification_code = tree.xpath("//table[@style='border-collapse: collapse; border: 1px dashed #f26928; background-color: #e3e3e3; height: 100% !important; font-family:Tahoma, Tahoma, Arial; font-size:19px; padding-left: 15px !important; text-align: center;']/tr[2]/td/strong/text()")
        verification_code_str = verification_code[0].strip()  # Metni al ve gereksiz boşlukları temizle
        verification_code_int = int(verification_code_str)    # Metni tamsayıya dönüştür
        if verification_code:
            print(verification_code_str)
            return verification_code_str
        else:
            print("Doğrulama kodu bulunamadı.")
        return verification_code[0] if verification_code else None


# Hesap oluşturma işlemi
def create_account(previous_email=None, previous_email_id=None):
    # Chrome tarayıcısını başlat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=get_chrome_options())

    try:
        # Trendyol üyelik sayfasına gidin
        driver.get('https://www.trendyol.com/uyelik?cb=%2F')

        # E-posta ve e-posta ID'sini alın
        if previous_email and previous_email_id:
            email, email_id = previous_email, previous_email_id
        else:
            email, email_id = get_email()

        time.sleep(15)  # Sayfanın tam yüklenmesi için bekle
        email_input = driver.find_element(By.ID, "register-email")
        email_input.send_keys(email)
        driver.delete_all_cookies()


        password_input = driver.find_element(By.ID, "register-password-input")
        password_input.send_keys('A123456789a')

        time.sleep(2)
        personal_checkbox = driver.find_element(By.CSS_SELECTOR, 'div[name="personal-data-error"]')
        driver.execute_script("arguments[0].click();", personal_checkbox)

        time.sleep(2)
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[src*="recaptcha"]')
        driver.switch_to.frame(iframe)

        recaptcha_checkbox = driver.find_element(By.ID, 'recaptcha-anchor')
        recaptcha_checkbox.click()

        time.sleep(10)

        actions = ActionChains(driver)
        actions.send_keys("\ue004")
        actions.send_keys("\ue004")
        actions.send_keys("\ue007")
        actions.perform()

        driver.switch_to.default_content()
        time.sleep(10)

        submit_button = driver.find_element(By.XPATH, "//button[@data-testid='submit-button']")
        submit_button.click()

        time.sleep(5)

        verification_code = get_verification_code(email_id=email_id)
        time.sleep(3)

        verification_input = driver.find_element(By.NAME, 'code')
        verification_input.click()
        actions = ActionChains(driver)
        actions.send_keys(verification_code)
        actions.perform()
        print(verification_code)

        time.sleep(3)
        submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ty-button') and contains(@class, 'ty-primary') and contains(text(), 'Onayla')]")
        submit_button.click()

        time.sleep(5)

        # Başarılı hesap oluşturma kaydı
        with open('acilan_hesaplar.json', 'a') as f:
            json.dump({"email": email, "sifre": "A123456789a"}, f, ensure_ascii=False, indent=4)
            f.write(',')
            f.write('\n')
        
        print("hesap oluşturuldu")
        return True, email, email_id

    except Exception as e:
        # Hatalı hesap oluşturma kaydı
        with open('hatali_hesaplar.json', 'a') as f:
            json.dump({"email": email, "id": email_id}, f, ensure_ascii=False, indent=4)
            f.write(',')
            f.write('\n')
        print(f'Hata oluştu: {e}\n bekleniyor (60 saniye)')
        for i in range(60):
            print(i)
            time.sleep(1)
        # Hata durumunda mail ve id'yi döndür
        return False, email, email_id

    finally:
        # Tarayıcıyı kapat
        driver.quit()

def main(number_of_accounts):
    def account_creation_task(previous_email=None, previous_email_id=None):
        while True:
            success, result_email, result_email_id = create_account(previous_email, previous_email_id)
            if success:
                # Hesap başarıyla oluşturulduğunda yeni bir mail alın
                return None, None
            else:
                # Hesap oluşturulamadığında aynı mail ile devam et
                previous_email, previous_email_id = result_email, result_email_id
                return previous_email, previous_email_id

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(account_creation_task) for _ in range(number_of_accounts)]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Hata oluştu: {e}')

if __name__ == "__main__":
    # Belirlediğiniz sayı kadar hesap oluştur
    number_of_accounts = 1000  # Örneğin 100 hesap oluştur
    main(number_of_accounts)