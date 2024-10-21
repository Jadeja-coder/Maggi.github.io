import streamlit as st
import qrcode
import numpy as np
import cv2

# Function to generate a QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# Function to display the QR code
def display_qr_code(qr_image):
    st.image(qr_image, caption='Scan this QR code to book your food items!', use_column_width=True)

# Streamlit app layout
st.title("Food Item Booking System")

st.sidebar.header("Menu")
food_items = {
    "Pizza": 12.99,
    "Burger": 8.99,
    "Sushi": 15.99,
    "Salad": 6.99
}

selected_items = st.sidebar.multiselect("Select Food Items", list(food_items.keys()))

# Calculate total price
if selected_items:
    total_price = sum(food_items[item] for item in selected_items)
    st.sidebar.write(f"Total Price: ${total_price:.2f}")

    # Generate QR code with selected items
    qr_data = ', '.join(selected_items)
    qr_image = generate_qr_code(qr_data)
    display_qr_code(qr_image)

    st.sidebar.write("QR code generated! Scan to book your items.")
else:
    st.sidebar.write("Please select at least one food item.")

# Optionally, add a section to upload QR code image for scanning
st.header("Scan QR Code")
uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read the uploaded image using OpenCV
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Decode the QR code
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector(image)

    if data:
        st.success(f"Decoded data: {data}")
    else:
        st.error("No QR code found.")


