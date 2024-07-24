import requests
import json

# Bearer token ve API URL
bearer_token = '123456' #Mağaza tokenı
api_url = 'https://sellerpublic-sdc.trendyol.com/checkout-promotioncoupon-promotionscbff-service/promotion-groups'

start_date = "2024-07-26T08:00:00.000"
end_date = "2024-07-26T08:00:00.000"

# İndirim oluşturma için gerekli veriler
promotion_data = {
    "awardCondition": {
        "contentIds": []
    },
    "discountType": "XTH_PRODUCT_Y_VALUE_DISCOUNTED",
    "awardType": "AMOUNT",
    "selectionConditionOver": "QUANTITY",
    "name": "İndirim ismi",
    "promotionGroupItems": [
        {
            "awardValue": 15,
            "awardQuantity": 1,
            "conditionOverValue": 2,
            "maxOrderCount": 100,
            "awardApplyLimit": 10
        }
    ],
    "requestBy": "Promotion Seller Center UI",
    "startDate": start_date,
    "endDate": end_date,
    "condition": {
        "brandIds": [],
        "categoryIds": [],
        "contentIds": [],
        "standaloneStorefrontIds": None
    },
    "storeFrontId": 1,
    "corporateSeller": True,
    "usableForAZChannel": False
}

# API isteği için gerekli başlıklar
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json',
    'X-Agentname': 'Promotion Seller Center Micro Frontend',
    'X-Applicationid': '1',
    'X-Banner-Version': '8001c544',
    'X-Child-Version': 'f0c6a876',
    'X-Correlationid': '65cddf10-712f-436d-87df-215214545133',
    'X-Header-Version': 'debb6d0e',
    'X-Storefrontid': '1'
}

# İndirim oluşturma isteği gönderme
response = requests.post(api_url, headers=headers, data=json.dumps(promotion_data))

if response.status_code == 201:
    print('İndirim başarıyla oluşturuldu:', response.text)
else:
    print('İndirim oluşturulamadı:', response.status_code, response.text)
