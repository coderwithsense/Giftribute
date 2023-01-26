import requests
import json

url = "https://track.delhivery.com/api/cmu/create.json"

payload = {
    "shipments": {
        "phone": "+916358740371",
        "name": "Himanshu Poptani",
        "pin": 282005,
        "add": "77 Tulsi Vihar, dayal bagh agra",
        "payment_mode": "COD",
        "order": "Kite",
        "cosignee_gst_amount": "0",
        "integrated_gst_amount": "0",
        "ewbn": "0",
        "cosignee_gst_tin": "0",
        "hsn_code": "0",
        "gst_cess_amount": "0"
    },
    "pickup_location": {"name": "Giftribute"}
}

payload = f"format=json&data={payload}"

headers = {
    "accept": "application/json",
    "Authorization": "Token e027c40f92f800c02bcde556f4884f0208175248",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(payload)