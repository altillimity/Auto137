import base64
import requests
import json

# Upload an image to imgbb and return the URL
def upload_image(image_path):
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "api_key",
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
        data = json.loads(res.content)
        return data["data"]["url"]

# Post to discord
def post_to_webhook(satellite, images, date):

    images_url = list()

    for img in images:
        images_url.append(upload_image(img))

    url = "url"
    if satellite.downlink == "APT":
        payload = "{\"username\": \"Aang23 Station\", \"embeds\": [{ \"image\": {\"url\": \"" + images_url[0] + "\"}, \"author\": {\"name\":\"" + satellite.name + "\"}, \"title\": \"At " + date.strftime('%H:%M %d, %b %Y') + "\" }]}"
    elif satellite.downlink == "LRPT":
        payload = "{\"username\": \"Aang23 Station\", \"embeds\": [{ \"image\": {\"url\": \"" + images_url[0] + "\"}, \"author\": {\"name\":\"" + satellite.name + " - Visible\"}, \"title\": \"At " + date.strftime('%H:%M %d, %b %Y') + "\" }, { \"image\": {\"url\": \"" + images_url[1] + "\"}, \"author\": {\"name\":\"" + satellite.name + " - Infrared\"}, \"title\": \"At " + date.strftime('%H:%M %d, %b %Y') + "\" }]}"
        
    print(requests.post(url, payload, headers={'Content-type': 'application/json'}).content)
