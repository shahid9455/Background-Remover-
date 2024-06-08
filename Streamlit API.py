import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("Background Removal and Image Resizing")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    try:
        # Open the uploaded image
        img = Image.open(uploaded_file)
        
        # Remove the background
        img_no_bg = remove(img)
        
        # Resize the image to 10x10 pixels
        resized_img = img_no_bg.resize((1000, 1000))
        
        # Display the original and processed images
        st.image(img, caption="Original Image", use_column_width=True)
        st.image(resized_img, caption="Processed Image", use_column_width=True)
        
        # Provide an option to download the processed image
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        st.download_button(
            label="Download Processed Image",
            data=img_byte_arr,
            file_name="processed_image.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"Error processing image: {e}")
