import requests
import json

# Bearer token ve API URL
bearer_token = '123456' #Mağaza tokenı
api_url = 'https://sellerpublic-sdc.trendyol.com/checkout-promotioncoupon-couponscbff-service/collectables/collect-to-win'

start_date = "2024-07-26T08:00:00.000"
end_date = "2024-07-26T23:00:00.000"

# Kupon oluşturma için gerekli veriler
coupon_data = {
    "sellerName": "Trendyol - Sana Özel Kupon", #Kupon ismi
    "budget": 1000,
    "discountType": "AMOUNT",  # İndirim türü: Tutar
    "discount": 10,  # İndirim tutarı
    "maxDiscountAmount": None,
    "lowerLimit": 300,  # Alt limit
    "couponStartDate": start_date,
    "couponEndDate": end_date,
    "collectStartDate": start_date,
    "couponCondition": {
        #"brandIds": [2044849],
        "categoryIds": None,
        "contentIds": None,
        "standaloneStorefrontIds": []
    },
    "averageProductsPrice": None,
    "createdBy": "Seller Center",
    "selectedRecommendations": ["COUPON_CATEGORY", "DISCOUNT", "LOWER_LIMIT"],
    "usageLimit": 100
}

# API isteği için gerekli başlıklar
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json',
    'X-Correlationid': '639ef65c-f8c1-4960-8541-1474c281cd1d',
    'X-Storefrontid': '1',
    'X-Applicationid': '1',
    'X-Agentname': 'coupon-seller-center'
}

# Kupon oluşturma isteği gönderme
response = requests.post(api_url, headers=headers, data=json.dumps(coupon_data))

if response.status_code == 201:
    print('Kupon başarıyla oluşturuldu:')
else:
    print('Kupon oluşturulamadı:', response.status_code, response.text)
