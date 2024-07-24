import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

isimler = [
   "Fadime Betül", "Fahrettin", "Süleyman Emre", "Şerif", "Sinem", "Yasemin Seda",
    "Selahattin", "Hüseyin Selim", "Ömer Lütfü", "Muhammet Said", "Ali Osman",
    "Cemil", "Aykut Can", "Elif Aylin", "Gülcemal", "Gülçin", "Gülizar",
    "Hülya", "Ersin", "Büşra Cansu", "Şehriban", "Fatih Emre", "Selma Nur",
    "Ece", "Hikmet", "Meliha", "Eren", "Osman İlker", "Sümeyye", "Erkan",
    "Zekiye", "Burhan", "Nazlı", "Dilek Nur", "Murat Emre", "Taylan",
    "Hakkı", "Yunus Emre Can", "Buse Nur", "Tuğçe", "Ali Cengiz", "Büşra Kızılkaya",
    "Sultan", "Kubilay Kamil", "Meryem Nur", "Özgür Burak", "Şirin", "Recep Emre",
    "Süleyman Fatih", "Furkan Emre", "Hüseyin Kadir", "Fatma Nur", "Ayşe Kübra",
    "Merve Nur", "Selma", "Tuğçe Nur", "Yasin Emre", "Cemal", "Emine Nur",
    "Furkan Emre", "Meryem Gül", "Hüseyin Cemal", "Süleyman", "Şeyma", "Murat Can",
    "Nesrin", "Onur Emre", "Sefa Can", "Emine Betül", "Mehmet Berkay", "Nisa Nur",
    "Abdulkadir", "Emre Emir", "Sümeyye", "Aylin", "Halil İbrahim", "Kubilay Emre",
    "Yusuf Emre", "Zeliha", "Melike", "Nurcan", "Nurcan", "Şeyma", "Tuba",
    "Mehmet Efe", "Sümeyye", "Emine Nur", "Gökhan", "İlyas", "Sümeyye",
    "Furkan Emre", "Ali", "Tolga", "Furkan", "Süleyman", "Duygu", "Süleyman",
    "Fatih", "Halil İbrahim", "Mehmet", "İsmail", "Duygu", "Sümeyye", "Yunus Emre",
    "Ayşe Nur", "Yusuf Emre", "Yasin Emre", "Hüseyin", "Tuğçe", "Merve", "İbrahim",
    "Taha", "Emirhan", "Hüseyin", "Murat", "Rabia", "Ali", "Sümeyye",
    "Süleyman", "Emirhan", "Sebahattin", "Hüseyin", "Ayşe", "Ceren", "Fatih",
    "Nurcan", "Furkan", "Furkan", "Emine", "Hüseyin", "Sümeyye", "Tuba",
    "Ali", "Zeliha", "Süleyman", "Hüseyin", "Gizem", "Neslihan", "Melike",
    "Mustafa", "Nur", "Muhammet", "Murat", "Emine", "Sümeyye", "Emine",
    "Mustafa", "Cem", "Fatih", "Emine", "Sümeyye", "Melike", "Ali",
    "Halil", "Ceren", "Muhammet", "Fatih", "İbrahim", "Mehmet", "Fatih",
    "Tuba", "Murat", "Sümeyye", "Süleyman", "Emine", "Süleyman", "Hüseyin",
    "Cem", "Sümeyye", "Nur", "Emine", "Süleyman", "Ayşe", "Fatih",
    "Sümeyye", "Mustafa", "Sümeyye", "Cem", "Fatih", "Sümeyye", "Hüseyin",
    "Nur", "Emine", "Süleyman", "Emine", "Fatih", "Süleyman", "Fatih",
    "Emine", "Sümeyye", "Hüseyin", "Mehmet", "Sümeyye", "Fatih", "Sümeyye",
    "Emine", "Süleyman", "Fatih", "Emine", "Sümeyye", "Fatih", "Sümeyye",
    "Emine", "Fatih", "Sümeyye", "Emine", "Süleyman", "Fatih", "Emine",
    "Fatih", "Süleyman", "Emine", "Sümeyye", "Fatih", "Sümeyye", "Hüseyin",
    "Emine", "Fatih", "Sümeyye", "Emine"
]

soyisimler = [
    "Delal Abdullatif", "Fatma Özlem", "Özde", "Atahan", "Hacı Mehmet",
    "Mükerrem Zeynep", "Bestami", "Aykanat", "Şennur", "Tutkum",
    "Mügenur", "Sevinç", "Kayıhan Nedim", "Lemi", "Cihan", "Rafi",
    "Mehmetcan", "Nuhaydar", "Emine Münevver", "Servet", "Çilem",
    "Recep Ali Samet", "Emre Ayberk", "Kerime Hacer", "Ercüment", "Sarper",
    "Berker", "İclal", "Lemis", "Ahmet Polat", "Ata Kerem", "Ahmet Raşit",
    "Ecem Hatice", "Nüket", "Senem", "Ayşen", "Pekcan", "Bedirhan Lütfü",
    "Semina", "Eda Sena", "Müyesser", "Selinti", "Bahar Özlem", "İlma",
    "Kutlu", "Nesibe Nurefşan", "Ömer Buğra", "Hiba", "Mazlum", "Elif Tuğçe",
    "Ahmet Ruken", "Yaşar Utku Anıl", "Rana", "Fethullah", "Burak Tatkan",
    "Merve Ece", "Rima", "Elif Dilay", "Sırma Begüm", "Nefse", "Büşra Gül",
    "Erna", "Hikmet Nazlı", "İsmail Umut", "İlkay Ramazan", "Nebahat",
    "İlyas Umut", "Halim", "Yasin Şükrü", "Cansev", "Memet Ali", "Deniz Dilay",
    "İzlem", "Öget", "Şeyda Nur", "Zeki Yiğithan", "Nunazlı", "Ferdacan",
    "Şerife", "Mustafa Burhan", "Ilım", "Sevginur", "Hayrunnisa",
    "Hanife Duygu", "Sevtap", "Paksoy", "İlkim", "Rubabe Gökçen", "Saba",
    "Çisem", "Sabiha Elvan", "Edip", "Almina", "Saime", "Nehar", "Kaan Muharrem",
    "Murat Kaan", "Murat Sinan", "Ateş", "Zeynep Nihan", "Kerime", "Hami",
    "Thomas", "Güneş", "Elif Feyza", "Uğur Ali", "Osman Yasin", "Adem",
    "Sera Cansın", "Ali İsmail", "Ruhugül", "Alçiçek", "Memet", "Mercan",
    "Gökay", "Pırıltı", "Özgün", "Özgen", "Seung Hun", "Gülser", "Yüksel",
    "Ecren", "Muhammet Raşit", "Sakıp", "Kazım", "Abdullah Atakan", "Coşkun",
    "Serdar Kaan", "Ezel", "Ayşegül", "Sefa Kadir", "Elif Etga", "Balın",
    "Mahperi", "Erol Özgür", "Atak", "Safa", "Gökmen", "Fazıl Erem", "Bensu",
    "Nazım Orhun", "Safa Ahmet", "Demircan", "Burçin Kübra", "Derviş Haluk",
    "Taylan Remzi", "Abdulvahap", "Aygün", "Ayla", "Kubilay Barış",
    "Mustafa Samed", "Berfin Dilay", "İbrahim Onat", "Jutenya", "Hulki",
    "Mustafa Doğukan", "Hüner", "Buse Gizem", "Halime", "Didem", "Mihrinaz",
    "Lal", "Senay", "Remzi", "Armağan", "Çelik", "Kübra Tansu", "Uluç Emre",
    "Mehmet Burhan", "Ayça", "Akın", "Seçilay", "Selman", "Yasemin Pınar",
    "Umut Ateş", "Buse Çiğdem", "Büşra Betül", "Münevver", "Tuba Nur",
    "Özlem Duygu", "Muharrem", "Mert Kadir", "Dinçer", "Kıvılcım", "Havva",
    "Lütfü Berkay", "Gonca", "Nurhan", "Alper Kağan", "Suna Nur", "Yeliz",
    "Feyza Ayşe", "Ali Okan", "Adnan", "İsmet", "Serkan", "Mete", "Beyza",
    "İsmail Bilge", "Mehmet Sadık", "Halil Uğur", "Ediz", "Nurettin", "Meral",
    "Tansel", "Hacer Esra", "Gülseren", "Zeynep Gülşen", "Oğuz Kaan",
    "Aybüke Meryem", "Talha", "Hürriyet", "Melike", "Ebru", "Ahmet Hakan",
    "Aydın", "Esen", "Bünyamin", "Baha", "Ünzile", "Mukaddes", "Pınar Duygu",
    "Fatma Melek", "Rukiye", "Zübeyde", "Batuhan", "Nagehan", "Melihcan",
    "Sevinç", "Leyla", "Müge", "Funda", "Mehmet Hanifi", "Yalın", "Dursun",
    "Derviş", "Zarif", "Mehmet Çağrı", "Talat", "Dilşad", "Murtaza",
    "Burak Barış", "Leyla Tuğçe", "Selçuk", "Ethem", "Şeyda", "Arzu", "Şeymanur",
    "Yunus Emre", "Bekir", "Sebahat", "Adnan Can", "Bünyamin Burak", "Birkan",
    "Kaan Yasin", "Mahmut", "Şükran", "Hacı Mehmet", "Hakkı Utku", "Gizem",
    "Muratcan", "Rabia", "Kübra", "Mücahit", "Ömer Faruk", "Rana Nur",
    "Esma Nur", "Müberra", "Aslıhan", "Muhammet Fatih", "Mustafa Serdar",
    "Neşe", "Murat Alp", "Elif Ecem", "Mustafa Deniz", "Semra", "Berat",
    "Yavuz", "Kevser", "Meryem", "Meryem Zeynep", "Emre", "Doğukan", "Zeynep",
    "Hacer", "Alperen", "Abdullah Emre", "Hüseyin Can", "Rauf", "Zerrin",
    "Merve", "Mehmet Tayyip", "Sakine", "Aykut", "Erdal", "Yusuf Can",
    "Serkan Kaan", "Emre Barış", "Hasan Hüseyin", "Cenk", "Erdem", "Büşra",
    "Kemal", "Kadriye", "Berna", "Emin", "Gökçe", "Gürkan", "Berkay",
    "Mustafa Erkan", "Neslihan", "Çağdaş", "Hayrettin", "Beyza Nur",
    "Erdem Serhat", "Hilal", "Mehmet Murat", "Gürsel", "Ahmet", "Ela",
    "Osman", "Burcu", "Onur", "Ebru Ayşe", "Rıdvan", "Elif Gül", "Özgür",
    "Hüseyin", "Büşra Nur", "Hasan Basri", "Lütfiye", "Mehmet Reşit",
    "Hidayet", "Yavuz Selim", "Gülcan", "Uğur", "Nisa", "Arif", "Gülbahar",
    "Ebru Ümmü", "Furkan", "Mehmet Fatih", "Gülşen", "Canan", "Tuğba",
    "Erhan", "Fatma Hilal", "Ertan", "Esra", "Yusuf Sinan", "Özgün Akın",
    "Musa", "Sadiye", "Samed", "İbrahim", "Yusuf", "Burcu Nur", "Asuman",
    "Hilmi", "Meryem Nur", "Hüseyin Enes", "Mehmet Berkay", "Hakan",
    "Muharrem Uğur", "Sefa", "Gülten", "Pınar", "Şenay", "Nihat", "Arzuhan",
    "Umut", "Ayla Nur", "Soner", "Büşra Sema", "Canberk", "Şükrü",
    "Kemal Can", "Yağmur", "Mehmet Selim", "Hüseyin Kaan", "Ömer",
    "Abdülhamit", "Muhammed", "Zeynep Gamze", "Berna Nur", "Ertuğrul",
    "Özlem", "Türkan", "Fatma", "Türker", "Mehmet Özgür", "Süleyman",
    "Mehmet Emin", "Gülizar", "Asuman Ayşe", "Selma", "Serap", "Mehmet Emre",
    "Fatma Gül", "Feride", "Nesrin", "Oğuzhan", "Fulya", "Duygu", "Nurettin Enes",
    "Dilara", "Nursel", "Serkan Serdar", "Cem", "Ümran", "Recep",
    "Mustafa Kemal", "Özge", "Zeynep Betül", "Abdülkadir", "Betül", "Dilek",
    "Gözde", "Ali", "Fatih", "Merve Nur", "Mert", "Merve Gül", "Derya",
    "Halil İbrahim", "Bilgehan", "Cansu", "Yasemin", "Aslı", "Barış",
    "Abdullah", "Sibel", "Ezgi", "Muharrem Halit", "Sedat", "Cihan", "Gizemnur",
    "Yunus", "Fatma Nur", "Hatice", "Fatma Esra", "Sedat Cem", "Erdoğan",
    "Doğan", "Mehmet Salih", "Zeki", "Erdinç", "Halil", "Hüseyin Özgür",
    "Ayşe", "Nurullah", "Süleyman Samet", "Ahmet Gökhan", "Rabia Nur",
    "Mehmet Efe", "Hüseyin Cihan", "Ali Murat", "Ferhat", "Osman Zeki",
    "Emre Can", "Emine", "Nurettin Fatih", "Ayşe Gizem", "Efe", "Ahmet Çağrı",
    "Furkan Emre", "Muhammet Emir", "Yasin", "Murat", "Esra Nur", "Muhammet Furkan",
    "Can", "Gülay", "Havva Zehra", "Tuba", "Feyyaz", "Emin Barış", "Fatih Ferdi",
    "Ferhat Can", "Hüseyin Salih", "Hüseyin Yasin", "Kübra Nur", "Selma Gizem",
    "Emine Gül", "Recep Furkan", "Sadettin", "Cemre", "Sinan", "Deniz", "Özgür Can",
    "Emre Yasin", "Osman Kadir", "Hüseyin Yiğit", "Zümrüt", "Seda", "Onur Can",
    "Ali Rıza", "Beril", "Muharrem Salih", "Uğur Can", "Süleyman Kaan",
    "Hasan", "Taha", "Mehmet Emin Gökhan", "Esra Meltem", "Hüseyin Emre",
    "Tuna", "Ümit", "Fatih Can", "Emine Seda", "Fadime", "Muharrem Arif",
    "Canan Nur", "Yusuf Caner", "Güray", "Yasemin Nur", "Bora", "Adem",
    "Kamil", "Sezai", "Ömer Faruk Can", "Ahmet Yasin", "Özkan", "Saniye",
    "Sertaç", "Rabia Nur", "Meryem Sinem", "Serhat", "Kubilay", "Yasin Can",
    "Hüseyin Salih", "Yüksel", "Ömer Faruk", "Elif", "Mehmet Cemal",
    "Seda Nur", "Mehmet Fatih", "Süleyman Can", "Süleyman Hüseyin",
    "Fadime Betül", "Özlem Nur", "Hüseyin Sami", "Meltem", "Ufuk", "Ayşenur",
    "Ayşegül", "Sibel Tuğçe", "Ali Can", "Ümit Can", "Ümitkamil", "Rabia Betül",
]

# Mail adresi havuzu
mail_adresleri = []

veriler_str = '''meuse57780@xbwsyw2.cashbenties.com
laurena87385@zuirtsw.crankymonkey.info
'''

ilk_veriler = veriler_str.split('\n')

def ilk_veri_formatina_cevir(ilk_veri_listesi):
    ilk_formatli_veriler = []
    for veri in ilk_veri_listesi:
        email, domain = veri.split("@")
        sifre = "a123456"
        ilk_formatli_veriler.append({"email": veri, "sifre": sifre})
    return ilk_formatli_veriler

ilk_formatli_veriler = ilk_veri_formatina_cevir(ilk_veriler)
mail_adresleri = ilk_formatli_veriler


def veri_formatina_cevir(veri_listesi):
    formatli_veriler = []
    for veri in veri_listesi:
        email, domain = veri.split("@")
        sifre = "a123456"
        formatli_veriler.append({"email": veri, "sifre": sifre})
    return formatli_veriler

def trendyol_giris(driver, email, sifre):
    try:
        driver.get("https://www.trendyol.com/giris")  # Trendyol giriş sayfasına git
        time.sleep(1)  # Sayfanın tam olarak yüklenmesini bekleyin

        # E-posta alanını doldur
        email_input = driver.find_element(By.CSS_SELECTOR, ".q-input-wrapper.email-input input#login-email")
        email_input.send_keys(email)

        # Şifre alanını doldur
        sifre_input = driver.find_element(By.ID, "login-password-input")
        sifre_input.send_keys(sifre)
        time.sleep(1)  # Sayfanın tam olarak yüklenmesini bekleyin

        # Giriş yap düğmesine tıkla
        giris_yap_btn = driver.find_element(By.CSS_SELECTOR, "button.q-primary.q-fluid.q-button-medium.q-button.submit[type='submit'] span")
        giris_yap_btn.click()
        time.sleep(1)  # Girişin tam olarak gerçekleşmesini bekleyin

        return True  # Giriş başarılı

    except Exception as e:
        print("Giriş yapılırken hata oluştu:", e)
        return False  # Giriş başarısız

def hesap_bilgilerini_guncelle(driver):
    try:
        # Hesap bilgileri sayfasına git
        driver.get("https://www.trendyol.com/Hesabim/KullaniciBilgileri")
        time.sleep(2)

        # İsim ve soyisim alanlarını bul ve doldur
        isim_input = driver.find_element(By.NAME, "firstname")
        soyisim_input = driver.find_element(By.NAME, "lastname")

        # Rastgele bir isim ve soyisim seç
        rastgele_isim = random.choice(isimler)
        rastgele_soyisim = random.choice(soyisimler)

        isim_input.clear()
        isim_input.send_keys(rastgele_isim)
        soyisim_input.clear()
        soyisim_input.send_keys(rastgele_soyisim)

        time.sleep(1)

        # Bilgileri güncelle düğmesine tıkla
        guncelle_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'GÜNCELLE')]")
        guncelle_btn.click()
        time.sleep(1)
        driver.quit()


    except NoSuchElementException:
        print("Hesap bilgileri güncelleme işlemi başarısız.")

    except Exception as e:
        print("Hesap bilgileri güncelleme sırasında bir hata oluştu:", e)

def kontrol_et(driver, email):
    try:
        # Kullanıcı bilgisi sayfasına git
        driver.get("https://www.trendyol.com/Hesabim/KullaniciBilgileri")
        time.sleep(2)

        # İsim ve soyisim alanlarını bul ve değerlerini al
        isim_input = driver.find_element(By.NAME, "firstname")
        soyisim_input = driver.find_element(By.NAME, "lastname")

        isim_degeri = isim_input.get_attribute("value")
        soyisim_degeri = soyisim_input.get_attribute("value")

        # İsim ve soyisim alanlarının dolu olup olmadığını kontrol et
        if isim_degeri and soyisim_degeri:
            return email
        else:
            return None

    except NoSuchElementException:
        print("Kullanıcı bilgileri bulunamadı.")

    except Exception as e:
        print("Kullanıcı bilgilerini kontrol ederken bir hata oluştu:", e)

def main():
    isim_güncellenen_kullanici_sayısı=0
    isim_kontrol_edilen_kullanici_sayısı=0
    # Her bir mail adresi için işlemleri gerçekleştir
    for mail_adresi in mail_adresleri:
        # Tarayıcı başlatma
        options = Options()
        options.headless = False  # Headless modunu devre dışı bırak
        driver = webdriver.Chrome(options=options)

        # Trendyol'a giriş yap
        if trendyol_giris(driver, mail_adresi["email"], mail_adresi["sifre"]):
            # Hesap bilgilerini güncelle
            hesap_bilgilerini_guncelle(driver)
            isim_güncellenen_kullanici_sayısı+=1
        # Tarayıcıyı kapat
        print("isimler güncelleniyor --> (", isim_güncellenen_kullanici_sayısı, "/", len(mail_adresleri), ") --> %", (isim_güncellenen_kullanici_sayısı * 100) / len(mail_adresleri))
        driver.quit()

    isim_soyisim_bulunanlar = []
    isim_soyisim_bulunmayanlar = []

    # Her bir mail adresi için işlemleri gerçekleştir
    for mail_adresi in mail_adresleri:
        # Tarayıcı başlatma
        options = Options()
        options.headless = True  # Headless modunu etkinleştir
        driver = webdriver.Chrome(options=options)

        # Trendyol'a giriş yap
        if trendyol_giris(driver, mail_adresi["email"], mail_adresi["sifre"]):
            # Kullanıcı bilgilerini kontrol et
            mail_adresi_sonuc = kontrol_et(driver, mail_adresi["email"])
            if mail_adresi_sonuc:
                isim_soyisim_bulunanlar.append(mail_adresi["email"])
            else:
                isim_soyisim_bulunmayanlar.append(mail_adresi["email"])
                
            isim_kontrol_edilen_kullanici_sayısı+=1
                
        print("isimler kontrol ediliyor -->", isim_kontrol_edilen_kullanici_sayısı, "/", len(mail_adresleri), "/ --> %", (isim_kontrol_edilen_kullanici_sayısı * 100) / len(mail_adresleri))


        # Tarayıcıyı kapat
        driver.quit()

        isimli_formatli_veriler = veri_formatina_cevir(isim_soyisim_bulunanlar)
        isimsiz_formatli_veriler = veri_formatina_cevir(isim_soyisim_bulunmayanlar)

    # Bulunanları JSON dosyasına yaz
    with open("/Users/alper/Desktop/isim_soyisim_bulunanlar.json", "x") as f:
        json.dump(isimli_formatli_veriler, f, indent=4)

    # Bulunmayanları JSON dosyasına yaz
    with open("/Users/alper/Desktop/isim_soyisim_bulunmayanlar.json", "x") as f:
        json.dump(isimsiz_formatli_veriler, f, indent=4)



    driver.quit()

if __name__ == "__main__":
    main()