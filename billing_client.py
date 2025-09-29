from settings import MOCK_MODE, TMF_BASE_URL, HTTP_TIMEOUT
import requests

def get_balance(customer_id):
    if MOCK_MODE or not TMF_BASE_URL:
        return {"customerId": customer_id, "balance": 249.50, "lastBill": {"amount": 499, "date": "2025-07-15"}}
    resp = requests.get(f"{TMF_BASE_URL}/bill", params={"customer.id": customer_id}, timeout=HTTP_TIMEOUT)
    return resp.json()
