import requests
import json
from instamojo_wrapper import Instamojo
from dotenv import load_dotenv
import os 

instamojo_private_api_key = os.getenv('instamojo_private_api_key')
instamojo_private_auth_key = os.getenv('instamojo_private_auth_key')
delhivery_api_key = os.getenv('delhivery_api_key')
shiprocket_api_key = os.getenv('shiprocket_api_key')

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
    api = Instamojo(api_key=instamojo_private_api_key, auth_token=instamojo_private_auth_key)
    response = api.payment_request_status(payment_id)
    return response

def shipping_order(order_id, order_date, name, surname, address1, address2, city, pincode, country, state, email_addr, phone_number, order_items, amount_total, length, breadth, height, weight, payment_method="COD", comment="Order", pickup_location="Noida"):
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
        print(f"Failed to update order payment for order {order_id}. Status code: {response.status_code}, response")
