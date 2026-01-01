import zxing
import requests

reader = zxing.BarCodeReader()
RAPID_API_KEY = "32d4e13869mshe58c8ba195ec19bp1992bcjsn25302358262e"

def decode_barcode_image(image_path):
    barcode = reader.decode(image_path)
    if barcode:
        return {
            "value": barcode.parsed,
            "format": barcode.format
        }
    return None


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
