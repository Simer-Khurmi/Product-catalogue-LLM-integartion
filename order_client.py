import json, requests
from settings import TMF_BASE_URL, MOCK_MODE, HTTP_TIMEOUT

def place_order(order_data):
    if MOCK_MODE or not TMF_BASE_URL:
        with open("api/MOCK_DATA.json","r+") as f:
            data = json.load(f)
            orders = data.get("orders", [])
            order_id = f"ord{1000+len(orders)+1}"
            entry = {"orderId": order_id, "order": order_data}
            orders.append(entry)
            data["orders"] = orders
            f.seek(0); json.dump(data, f, indent=2); f.truncate()
        return {"status": "success", "orderId": order_id}
    resp = requests.post(f"{TMF_BASE_URL}/productOrder", json=order_data, timeout=HTTP_TIMEOUT)
    return resp.json()
