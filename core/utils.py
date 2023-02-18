import requests
import json
import uuid
from instamojo_wrapper import Instamojo

instamojo_private_api_key = "4cebf802f2b59fd703839ba470e07edd"
instamojo_private_auth_key = "666e517be92e43428bdc4c743e9dd11b"
delhivery_api_key = "e08d91719905b21264bd030ea76b09e383b44915"
shiprocket_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjI0ODUxMTEsImlzcyI6Imh0dHBzOi8vYXBpdjIuc2hpcHJvY2tldC5pbi92MS9leHRlcm5hbC9hdXRoL2xvZ2luIiwiaWF0IjoxNjc2NjQ5MjI1LCJleHAiOjE2Nzc1MTMyMjUsIm5iZiI6MTY3NjY0OTIyNSwianRpIjoid3JCQ0xjTXNXZnN3Y2xKWSJ9.IVgKWKAvJhF28ENZBf0l3M8nwNwfUQv2HHP1xBlB4ag"

def make_payment(amount, comment, name, email, phone, redirect_url):
    api = Instamojo(api_key=instamojo_private_api_key, auth_token=instamojo_private_auth_key, endpoint='https://www.instamojo.com/api/1.1/')
    response = api.payment_request_create(
        amount=amount,
        purpose=comment,
        buyer_name=name,
        email=email,
        phone=phone,
        redirect_url=redirect_url
    )
    return response

def get_payment(payment_id):
    headers = { 
        "Authorization": "Bearer y70kak2K0Rg7J4PAL8sdW0MutnGJEl"
    }
    response = requests.get(
    f"https://api.instamojo.com/v2/payments/{payment_id}/", 
    headers=headers
    )
    return response

# print(get_payment('MOJO3218105Q71586227'))

def shipping_order(order_id, order_date, name, surname, address1, address2, city, pincode, country, state, email_addr, phone_number, order_items, amount_total, length, breadth, height, weight, payment_method="COD", comment="Order", pickup_location="Primary"):
    url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

    payload = json.dumps({
        "order_id": order_id,
        "order_date": order_date,
        "pickup_location": pickup_location,
        "channel_id": "",
        "comment": comment,
        "billing_customer_name": name,
        "billing_last_name": surname,
        "billing_address": address1,
        "billing_address_2": address2,
        "billing_city": city,
        "billing_pincode": pincode,
        "billing_state": state,
        "billing_country": country,
        "billing_email": email_addr,
        "billing_phone": phone_number,
        "shipping_is_billing": True,
        "shipping_customer_name": "",
        "shipping_last_name": "",
        "shipping_address": "",
        "shipping_address_2": "",
        "shipping_city": "",
        "shipping_pincode": "",
        "shipping_country": "",
        "shipping_state": "",
        "shipping_email": "",
        "shipping_phone": "",
        "order_items": order_items,
        "payment_method": payment_method,
        "shipping_charges": 0,
        "giftwrap_charges": 0,
        "transaction_charges": 0,
        "total_discount": 0,
        "sub_total": amount_total,
        "length": length,
        "breadth": breadth,
        "height": height,
        "weight": weight
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {shiprocket_api_key}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

def update_order_payment(order_id):
    # Set up the API endpoint and payload
    url = "https://apiv2.shiprocket.in/v1/external/orders/update/adhoc"
    payload = {
        "order_id": order_id,
        "payment_method": "Prepaid",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {shiprocket_api_key}"
    }

    # Send the API request
    # response = requests.post(url, headers=headers, data=json.dumps(payload))
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    # Check the response status code
    if response.status_code == 200:
        print(f"Order payment for order {order_id} has been updated to Prepaid.")
    else:
        print(f"Failed to update order payment for order {order_id}. Status code: {response.status_code}")

# Define test data
order_id = str(uuid.uuid1())
order_date = "2022-12-13 12:00:00"
name = "John"
surname = "Doe"
address1 = "123 Main St"
address2 = ""
city = "Anytown"
pincode = "12345"
country = "IN"
state = "KA"
email_addr = "johndoe@example.com"
phone_number = "9876543210"
order_items = [
    {
        "name": "Product 1",
        "sku": "SKU-001",
        "units": 1,
        "selling_price": "10.00",
        "discount": "",
        "tax": "",
        "hsn": 1234
    },
    {
        "name": "Product 2",
        "sku": "SKU-002",
        "units": 2,
        "selling_price": "20.00",
        "discount": "",
        "tax": "",
        "hsn": 5678
    }
]
amount_total = "50.00"
length = 10
breadth = 20
height = 30
weight = 2.5

# Call the order function with test data
# order_response = order(order_id, order_date, name, surname, address1, address2, city, pincode, country, state, email_addr, phone_number, order_items, amount_total, length, breadth, height, weight)

# response = make_payment(9, "Payment", "Himanshu", "himanshupoptani12@gmail.com", 6358740371, "http://localhost:8000/thank-you")

# update_order_payment('f7aa4de2-af57-11ed-afe1-defb076d99ce')