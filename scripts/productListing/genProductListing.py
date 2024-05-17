import requests

from getSpreadsheet import getSpreadsheet
from genHeader import genHeader
from genAuth import genAuth


def getFeeds():
    # params = {
    #     "feedTypes": ["POST_FLAT_FILE_LISTINGS_DATA"],
    # }
    # report_request_response = requests.get("https://sellingpartnerapi-na.amazon.com/feeds/2021-06-30/feeds",
    #     headers=headers,
    #     auth=auth,
    #     params=params
    # )
    # return report_request_response

    params = {
        "marketplaceIds": "ATVPDKIKX0DER"
    }

    report_request_response = requests.get("https://sellingpartnerapi-na.amazon.com/definitions/2020-09-01/productTypes/SQUEEZE_TOY",
        headers=headers,
        auth=auth,
        params=params
    )
    print(report_request_response)
    print(report_request_response.json())
    return report_request_response


def submitListing():
    params = {
        "marketplaceIds": "ATVPDKIKX0DER"
    }

    data = {
        "productType": "TOYS_AND_GAMES",
        "attributes": {
            "brand": [
                {
                    "value": "Random brand",
                    "marketplace_id": "ATVPDKIKX0DER"
                }
            ],
            "bullet_point": [
                {
                    "value": "This is an amazing toy!",
                    "marketplace_id": "ATVPDKIKX0DER"
                }
            ],
            "country_of_origin": [
                {
                    "value": "United States",
                    "marketplace_id": "ATVPDKIKX0DER"
                }
            ],
            "item_name": [
                {
                    "value": "Fun toy for kids and children",
                    "marketplace_id": "ATVPDKIKX0DER"
                }
            ],
            "item_type_keyword": [
                {
                    "value": "squeeze-toys",
                    "marketplace_id": "ATVPDKIKX0DER"
                }
            ],
            "product_description": [
                {
                    "value": "Kids can play with this super duper awesome toy!",
                    "marketplace_id": "ATVPDKIKX0DER"
                }
            ],
            "supplier_declared_dg_hz_regulation": [
                {
                    "value": "",
                    "marketplace_id": "ATVPDKIKX0DER"
                }
            ]
        }
    }

    # sellerId = "A1XDFAXUH4XVWD"
    # sku = "SBP-unreal987"
    # endpoint = "https://sellingpartnerapi-na.amazon.com//listings/2021-08-01/items/{sellerId}/{sku}"
    # report_request_response = requests.put("https://sellingpartnerapi-na.amazon.com//listings/2021-08-01/items/{sellerId}/{sku}",
    report_request_response = requests.put("https://sellingpartnerapi-na.amazon.com/listings/2021-08-01/items/A1XDFAXUH4XVWD/random-sku-123",
        headers=headers,
        auth=auth,
        params=params,
        json=data
    )
    print(report_request_response.json()['issues'])
    return report_request_response

if __name__ == '__main__':
    headers = genHeader()
    auth = genAuth()

    # print(headers)

    # getFeeds()
    submitListing()

# https://sellingpartnerapi-na.amazon.com/definitions/2020-09-01/productTypes/SQUEEZE_TOY?marketplaceIds=ATVPDKIKX0DER