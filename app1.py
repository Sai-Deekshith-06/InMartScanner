import streamlit as st
import tempfile, hashlib
from PIL import Image

from barcode_utils import (
    decode_barcode_image,
    lookup_item_upcitemdb,
    lookup_item_rapidapi
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="inMart - Barcode Scanner",
    layout="wide"
)
is_mobile = st.session_state.get("is_mobile", False)
with st.sidebar:
    is_mobile = st.checkbox("📱 Mobile view", value=is_mobile)
    st.session_state.is_mobile = is_mobile

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "last_image_id" not in st.session_state:
    st.session_state.last_image_id = None

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <h1 style="text-align:center;">🛒 inMart - Barcode Scanner</h1>
    <p style="text-align:center; color:gray;">
        Scan products to add them to your cart
    </p>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def add_to_cart(product):
    """Merge quantity if already in cart"""
    # for item in st.session_state.cart:
    #     if item["id"] == product["id"]:
    #         item["qty"] += 1
    #         return
    # st.session_state.cart.append(product)
    if product["id"] in st.session_state.cart:
        st.session_state.cart[product["id"]]["qty"] += 1
    else:
        st.session_state.cart[product["id"]] = product
    # st.write(st.session_state.cart)


def lookup_product(barcode):
    item = lookup_item_upcitemdb(barcode)
    if not item:
        item = lookup_item_rapidapi(barcode)
    return item

# --------------------------------------------------
# CART UI
# --------------------------------------------------
# def show_cart_ui_mobile():
#     st.subheader("🛒 Cart")

#     total_price = 0

#     for index, key in enumerate(st.session_state.cart):
#         item = st.session_state.cart[key]

#         # ROW 1: image | item info | remove
#         col_img, col_info, col_x = st.columns([1, 3, 0.6])

#         with col_img:
#             if item["image"]:
#                 st.image(item["image"], width=80)

#         with col_info:
#             st.markdown(f"**{item['name']}**")
#             st.caption(item["desc"])

#         with col_x:
#             if st.button("❌", key=f"remove_m_{index}"):
#                 st.session_state.cart.pop(key)
#                 st.rerun()

#         # ROW 2: quantity | subtotal
#         col_qty, col_total = st.columns([2, 1])

#         with col_qty:
#             c1, c2, c3 = st.columns([1, 1, 1])

#             with c1:
#                 if st.button("➖", key=f"minus_m_{index}"):
#                     item["qty"] -= 1
#                     if item["qty"] <= 0:
#                         st.session_state.cart.pop(key)
#                         st.rerun()

#             with c2:
#                 st.markdown(
#                     f"<h4 style='text-align:center'>{item['qty']}</h4>",
#                     unsafe_allow_html=True
#                 )

#             with c3:
#                 if st.button("➕", key=f"plus_m_{index}"):
#                     item["qty"] += 1

#         subtotal = item["price"] * item["qty"]
#         total_price += subtotal

#         with col_total:
#             st.markdown(f"### ₹{subtotal:.2f}")

#         st.markdown("---")

#     # TOTAL (fixed bottom style)
#     st.markdown(
#         f"""
#         <div style="
#             background:#6a5acd;
#             padding:14px;
#             border-radius:10px;
#             text-align:center;
#             color:white;
#             font-size:20px;
#             font-weight:bold;
#         ">
#             Total: ₹{total_price:.2f}
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# def cart_item_mobile(item, key):
#     if item["image"]:
#         st.image(item["image"], width=90)

#     st.markdown(f"**{item['name']}**")
#     st.caption(item["desc"])

#     st.markdown("<div class='qty-container'>", unsafe_allow_html=True)
#     qty_col1, qty_col2, qty_col3 = st.columns(3)
#     with qty_col1:
#         if st.button("➖", key=f"m_minus_{key}"):
#             item["qty"] -= 1
#     with qty_col2:
#         st.markdown(f"<h4 style='text-align:center'>{item['qty']}</h4>",
#                     unsafe_allow_html=True)
#     with qty_col3:
#         if st.button("➕", key=f"m_plus_{key}"):
#             item["qty"] += 1
#     st.markdown("</div>", unsafe_allow_html=True)

#     subtotal = item["price"] * item["qty"]
#     st.markdown(f"### ₹{subtotal:.2f}")

#     if st.button("❌ Remove", key=f"m_remove_{key}"):
#         st.session_state.cart.pop(key)
#         st.rerun()

#     st.markdown("---")

def show_cart_ui():
    st.markdown(f"## Cart ({len(st.session_state.cart)} items)")

    total_price = 0

    for index, item in enumerate(st.session_state.cart):
        
        _, col1, col2 = st.columns([0.2, 0.8, 3]) 
            
        with col1:
            if st.session_state.cart[item]["image"]:
                st.image(st.session_state.cart[item]["image"], width=120)

        with col2:
            tc1, tc2 = st.columns([1, 0.18])

            with tc1:
                st.markdown(f"**{st.session_state.cart[item]['name']}**")
                st.caption(st.session_state.cart[item]["desc"])
                
            with tc2:
                if st.button("❌", key=f"remove_{index}") or st.session_state.cart[item]["qty"] <= 0:
                    st.session_state.cart.pop(item)
                    st.rerun()

            c1, _, c3 = st.columns([1, 0.1, 1])

            with c1:
                subtotal = st.session_state.cart[item]["price"] * st.session_state.cart[item]["qty"]
                total_price += subtotal
                st.markdown(f"### ₹{subtotal:.2f}")
                # st.markdown(f"**Subtotal:** ₹{subtotal:.2f}")

            with c3:
                cc1, cc2, cc3 = st.columns([1, 1, 1])
                with cc1:
                    if st.button('',icon="➖", key=f"minus_{index}"):
                        st.session_state.cart[item]["qty"] -= 1
                with cc2:
                    st.markdown(
                        f"<h4 style='text-align:center;'>{st.session_state.cart[item]['qty']}</h4>",
                        unsafe_allow_html=True
                    )
                with cc3:
                    if st.button("➕", key=f"plus_{index}"):
                        st.session_state.cart[item]["qty"] += 1

        st.markdown("---")

    # --------------------------------------------------
    # TOTAL
    # --------------------------------------------------
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(to right, #6a5acd, #7b68ee);
            padding: 16px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 22px;
            font-weight: bold;
        ">
            Total: ₹{total_price:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

left, _, right = st.columns([1.1,0.1, 3.8])

with left:
    # --------------------------------------------------
    # INPUT MODE
    # --------------------------------------------------
    st.markdown("### 🔍 Scan Mode")
    mode = st.radio(
        "",
        ["📷 Camera (Auto Scan)", "🖼 Upload Image", "⌨ Manual Barcode"]
    )
    barcode_value = None

    # --------------------------------------------------
    # CAMERA AUTO SCAN
    # --------------------------------------------------
    
    if mode == "📷 Camera (Auto Scan)":
        # Initialize state
        if "last_image_id" not in st.session_state:
            st.session_state.last_image_id = None

        # Camera widget (always rendered)
        with st.popover("Point your camera at a barcode and take a picture of it.", use_container_width=True):
            img = st.camera_input("")

        if img:
            # Generate a stable ID from image bytes
            image_bytes = img.getbuffer()
            current_image_id = hashlib.md5(image_bytes).hexdigest()

            # Scan only if new image
            if current_image_id != st.session_state.last_image_id:
                st.session_state.last_image_id = current_image_id

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
                    f.write(image_bytes)
                    result = decode_barcode_image(f.name)

                if result:
                    barcode_value = result["value"]
                    st.success(f"✅ Detected: {barcode_value}")
                else:
                    st.error("❌ No barcode detected")

    # --------------------------------------------------
    # IMAGE UPLOAD
    # --------------------------------------------------
    elif mode == "🖼 Upload Image":
        file = st.file_uploader("Upload barcode image", type=["jpg", "png"])

        if file:
            image = Image.open(file)
            st.image(image, width=300)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
                image.save(f.name)
                result = decode_barcode_image(f.name)

            if result:
                barcode_value = result["value"]
                st.success(f"✅ Detected: {barcode_value}")
            else:
                st.error("❌ No barcode detected")

    # --------------------------------------------------
    # MANUAL INPUT
    # --------------------------------------------------
    elif mode == "⌨ Manual Barcode":
        barcode_value = st.text_input("Enter barcode")

    # --------------------------------------------------
    # LOOKUP & ADD TO CART
    # --------------------------------------------------
    if barcode_value:
        with st.spinner("Looking up product…"):
            product = lookup_product(barcode_value)

        if product:
            cart_item = {
                "id": barcode_value,
                "name": product.get("title", "Unknown Product"),
                "desc": product.get("category", ""),
                "price": float(product.get("lowest_recorded_price", 100)),
                "qty": 1,
                "image": (product.get("images") or [""])[0]
            }

            add_to_cart(cart_item)
            st.success("🛒 Added to cart")

        else:
            st.error("Product not found")

with right:
    # if is_mobile:
    #     show_cart_ui_mobile()
    # else:
    show_cart_ui()
