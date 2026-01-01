import streamlit as st
import tempfile
from PIL import Image
import requests

from barcode_utils import (
    decode_barcode_image,
    lookup_item_rapidapi,
    lookup_item_upcitemdb
    # lookup_item
)

st.set_page_config(page_title="Barcode Product Scanner", layout="centered")

st.title("🧾 Barcode Product Scanner")

mode = st.radio(
    "Choose input method",
    ["📷 Camera", "🖼 Upload Image", "⌨ Manual Barcode"]
)

barcode_value = None

# ---------------- CAMERA ----------------
if mode == "📷 Camera":
    img = st.camera_input("Scan barcode")

    if img:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            f.write(img.getbuffer())
            barcode = decode_barcode_image(f.name)

        if barcode:
            st.success(f"Detected: {barcode['value']}")
            barcode_value = barcode["value"]
        else:
            st.error("No barcode detected")

# ---------------- IMAGE UPLOAD ----------------
elif mode == "🖼 Upload Image":
    file = st.file_uploader("Upload barcode image", type=["jpg", "png"])

    if file:
        image = Image.open(file)
        st.image(image, caption="Uploaded Image")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            image.save(f.name)
            barcode = decode_barcode_image(f.name)

        if barcode:
            st.success(f"Detected: {barcode['value']}")
            barcode_value = barcode["value"]
        else:
            st.error("No barcode detected")

# ---------------- MANUAL ----------------
elif mode == "⌨ Manual Barcode":
    barcode_value = st.text_input("Enter barcode")

# ---------------- LOOKUP ----------------
if barcode_value and st.button("🔍 Lookup Product"):
    st.info("Searching product databases...")

    item = lookup_item_upcitemdb(barcode_value)

    if not item:
        item = lookup_item_rapidapi(barcode_value)

    if item:
        st.subheader("🛒 Product Details")
        st.write("**Title:**", item.get("title"))
        st.write("**Brand:**", item.get("brand"))
        st.write("**Category:**", item.get("category"))
        st.write("**Manufacturer:**", item.get("manufacturer"))

        images = item.get("images", [])
        if images:
            st.subheader("🖼 Product Images")
            for url in images[:3]:
                st.image(url)
        else:
            st.warning("No images available")

    else:
        st.error("Product not found")
