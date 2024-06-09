import requests
import json

##JHONNATAN
url = "https://graph.facebook.com/v19.0/279308521943312/messages"

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
  'Authorization': 'Bearer EAAQMT3uwSPIBO71amuURGNL1JNRTEEZBC5LIFGhAIdZAnvp0yXGJU1VQZAd9QumQCYpG4OZB0RLUhLWpIvigpTmjDVLtlpN6039aAwJOtE0ZC0FNDvcDQ8xrrUeUFmeYR0cZAYMKtthRFW7vlRMZAn5coDOwxyLxNWzoSAKY0k5yh7WXZB3fRatlhhoyn6OnvywPeUdbAwVttMS9Y5zr6uePz6tHa3HE1KMg5ZC7SYx4ZD'
}

response = requests.request("POST", url, headers=headers, data=payload)

print('FIN - C O R P I S')
print(response.text)