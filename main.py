import os
import requests
import json


whatsapp_token = os.getenv('FB_WHATSAPP_TOKEN')

print(whatsapp_token)
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
  #'Authorization': 'Bearer EAAQMT3uwSPIBO7TNoqHGT8xZBezX4IkFZCRlJC6Q9BeUBZB2wTg6ZASe0RrEdW5rd4kH1ZB67Ebq9GFZAykO0H6zH0zMKjVrLuDMDJnAkzVBqKs2Gaye8eDukmVakSHLOEKphGWEjeauIrJJBJTJN8eOatoLWZAcUepqMUD5ZCRlfxzXY83IlVB4l3bRPnSZBt7zB6z8GVLxRKo0bLSY5arIyrs9t7s9pRZCaxZAUI5ySqT'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

if __name__ == "__main__":
    if response.status_code == 200:
        print('FIN - C O R P I S')