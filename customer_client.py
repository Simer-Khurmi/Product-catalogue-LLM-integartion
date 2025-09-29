import json, requests
from settings import TMF_BASE_URL, MOCK_MODE, HTTP_TIMEOUT

def get_customer_info(customer_id):
    if MOCK_MODE or not TMF_BASE_URL:
        with open("api/MOCK_DATA.json","r") as f:
            for c in json.load(f)["customers"]:
                if c["id"] == customer_id:
                    return c
        return {"error": "customer not found"}
    resp = requests.get(f"{TMF_BASE_URL}/customer/{customer_id}", timeout=HTTP_TIMEOUT)
    return resp.json()
