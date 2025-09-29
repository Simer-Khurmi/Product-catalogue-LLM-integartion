import json, requests
from settings import TMF_BASE_URL, MOCK_MODE, HTTP_TIMEOUT

def list_offers(filters=None):
    if MOCK_MODE or not TMF_BASE_URL:
        with open("api/MOCK_DATA.json","r") as f:
            data = json.load(f)["productOffering"]
        results = data
        if filters:
            if "category" in filters:
                results = [o for o in results if o["category"] == filters["category"]]
            if "price_lte" in filters:
                results = [o for o in results if o["price"] <= int(filters["price_lte"])]
        return results
    resp = requests.get(f"{TMF_BASE_URL}/productOffering", params=filters, timeout=HTTP_TIMEOUT)
    return resp.json()

def get_offer_by_id(offer_id):
    if MOCK_MODE or not TMF_BASE_URL:
        with open("api/MOCK_DATA.json","r") as f:
            for o in json.load(f)["productOffering"]:
                if o["id"] == offer_id:
                    return o
        return {"error": "Offer not found"}
    resp = requests.get(f"{TMF_BASE_URL}/productOffering/{offer_id}", timeout=HTTP_TIMEOUT)
    return resp.json()
