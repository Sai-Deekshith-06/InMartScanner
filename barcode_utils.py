from pyzbar.pyzbar import decode
from PIL import Image
import requests

import os
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

if not RAPID_API_KEY:
    raise RuntimeError("RAPID_API_KEY is not set")

def decode_barcode_image(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception:
        return None

    results = decode(img)
    if not results:
        return None

    barcode = results[0]
    return {
        "value": barcode.data.decode("utf-8", errors="replace"),
        "format": barcode.type
    }

def lookup_item_upcitemdb(barcode):
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        if data.get("items"):
            return data["items"][0]
    return None


def lookup_item_rapidapi(barcode):
    url = f"https://barcodes-lookup.p.rapidapi.com/?query={barcode}"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "barcodes-lookup.p.rapidapi.com"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data.get("product")
    return None
