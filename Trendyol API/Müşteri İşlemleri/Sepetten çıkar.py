import requests
import json
from concurrent.futures import ThreadPoolExecutor

# Headers bilgileri
headers = {
    "culture": "tr-TR",
    "storefront-id": "1",
    "application-id": "1",
    "Content-Type": "application/json"
}

# API endpointleri
basket_url = "https://public-mdc.trendyol.com/discovery-web-checkout-service/basket/fragment/sepet?culture=tr-TR&storefrontId=1&basketBuyAgainAndMyFavoritesAbTestEnabled=B&basketRecoCorporateTabAbTestEnabled=A&checkoutSavingAbTest=B&installmentsInBasketAbTest=A&azSelected=false&channelId=1"
remove_from_basket_url_template = "https://public-mdc.trendyol.com/discovery-web-websfxcheckoutbasket-santral/remove/{item_id}?channelId=1"

# Tokenların ve proxylerin tutulduğu dosyanın adı
kullanıcı_dosyası = "/kullanıcı/dosyası/yolu.json"
proxy_dosyasi = "/proxy/dosyası/yolu.json"

# Tokenları ve proxy listesini dosyadan oku
with open(kullanıcı_dosyası, 'r') as dosya:
    kullanıcılar = json.load(dosya)

with open(proxy_dosyasi, 'r') as dosya:
    proxy_listesi = eval(dosya.read())

# Kullanıcı tokenını güncelle
def update_headers(token):
    updated_headers = headers.copy()
    updated_headers.update({"Authorization": f"Bearer {token}"})
    return updated_headers

# Sepetteki ürünleri getir
def fetch_basket_content(token, proxy):
    session = requests.Session()
    updated_headers = update_headers(token)
    session.headers.update(updated_headers)

    proxies = {
        "http": proxy,
        "https": proxy
    }

    response = session.get(basket_url, proxies=proxies)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Sepet içeriği getirilemedi: {response.status_code} - {response.text}")
        return None

# Sepetten ürün çıkar
def remove_from_basket(token, item_id, proxy, mail):
    session = requests.Session()
    updated_headers = update_headers(token)
    session.headers.update(updated_headers)

    proxies = {
        "http": proxy,
        "https": proxy
    }

    remove_url = remove_from_basket_url_template.format(item_id=item_id)
    response = session.delete(remove_url, proxies=proxies)
    if response.status_code == 204:
        print(f"{proxy} - {mail} - Ürün başarıyla sepetten çıkarıldı: {item_id}")
    else:
        print(f"Ürün sepetten çıkarılamadı: {item_id} - {response.status_code} - {response.text}")

# Verilen merchant_ids listesi
merchant_ids = [946618, 804319, 413287, 681697, 975739]  # Örnek olarak verildi, sizin vereceğiniz listeye göre güncelleyin. Satıcı ID sepetten çıkarılmamasını istediğiniz satıcı idleri girmelisiniz

# İş parçacığı havuzu ile paralel işlem
def process_basket_for_user(token, proxy, mail):
    basket_content = fetch_basket_content(token, proxy)
    if basket_content:
        # Correctly access items in the basket content
        items = basket_content.get("result", {}).get("data", {}).get("items", [])
        for item in items:
            merchant_id = item.get("merchant", {}).get("id")
            item_id = item.get("id")
            if merchant_id not in merchant_ids:
                remove_from_basket(token, item_id, proxy, mail)

proxy_index = 0

# Kullanıcılar üzerinde paralel işlem
with ThreadPoolExecutor(max_workers=10) as executor:  # Paralel iş parçacığı sayısını ayarlayın
    for kullanıcı in kullanıcılar:
        token = kullanıcı.get("token")
        mail = kullanıcı.get("email")
        proxy = proxy_listesi[proxy_index % len(proxy_listesi)]
        executor.submit(process_basket_for_user, token, proxy, mail)
        proxy_index += 1
