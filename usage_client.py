from settings import MOCK_MODE, TMF_BASE_URL, HTTP_TIMEOUT
import requests

def get_usage(customer_id):
    if MOCK_MODE or not TMF_BASE_URL:
        return {"customerId": customer_id, "dataUsedMB": 4320, "callsMin": 120}
    resp = requests.get(f"{TMF_BASE_URL}/usage", params={"customer.id": customer_id}, timeout=HTTP_TIMEOUT)
    return resp.json()
