import logging
import os
import requests
import json


class WS_API:
    def send_img_via_whatsapp(self,id_file_in,whatsapp_token):        
        #Limitacion: se puede enviar imagen alojada en algun servidor NO LOCAL        

        ##JHONNATAN
        url = "https://graph.facebook.com/v20.0/279308521943312/messages"

        payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": "51994375343",
        "type": "image",
        "image": {
            "link": f"https://drive.google.com/uc?export=download&id={id_file_in}"
        }
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {whatsapp_token}'  
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        logging.info("Se envió msg hacia whatsapp")
        return response