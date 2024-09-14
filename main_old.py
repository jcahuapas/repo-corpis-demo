import os
import requests
import json


def connect_to_gdrive():
    return 

def generate_report():
    return 

def send_image_via_whatsapp():
    whatsapp_token = os.getenv('FB_WHATSAPP_TOKEN')
     ##JHONNATAN
    url = "https://graph.facebook.com/v20.0/279308521943312/messages"

    payload = json.dumps({
      "messaging_product": "whatsapp",
      "to": "51994375343",
      "type": "image",
      "image": {
        "link": "https://drive.google.com/uc?export=download&id=1V1s3ahJdyOj4lnyNDsyF9hB32uih3nIg"
      }
    })

    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {whatsapp_token}'  
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response

if __name__ == "__main__":
    if response.status_code == 200:
        print('FIN - C O R P I S')
