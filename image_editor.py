import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import io

# Streamlit page configuration
st.set_page_config(page_title="AI Image Editor", layout="wide")

st.title("🖼️ AI Image Editing Tool")
st.write("Transform your images with filters, background removal, and more!")

# Initialize variables
uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
original_image = None
edited_image = None

if uploaded_image:
    # Load the image using PIL
    original_image = Image.open(uploaded_image)
    edited_image = original_image.copy()

    # Display the original image
    st.subheader("Original Image")
    st.image(original_image, use_column_width=True)

    # Filters and adjustments
    st.subheader("Adjust Image Filters")
    brightness = st.slider("Brightness", 0.1, 2.0, 1.0, 0.1)
    contrast = st.slider("Contrast", 0.1, 2.0, 1.0, 0.1)
    blur = st.slider("Blur", 0, 10, 0, 1)

    # Apply filters
    if st.button("Apply Filters"):
        enhancer = ImageEnhance.Brightness(edited_image)
        edited_image = enhancer.enhance(brightness)

        enhancer = ImageEnhance.Contrast(edited_image)
        edited_image = enhancer.enhance(contrast)

        if blur > 0:
            edited_image = edited_image.filter(ImageFilter.GaussianBlur(blur))

        st.subheader("Edited Image")
        st.image(edited_image, use_column_width=True)

    # Remove background
    if st.button("Remove Background"):
        try:
            img_byte_arr = io.BytesIO()
            edited_image.save(img_byte_arr, format='PNG')
            img_no_bg = remove(img_byte_arr.getvalue())
            edited_image = Image.open(io.BytesIO(img_no_bg))

            st.subheader("Image with Background Removed")
            st.image(edited_image, use_column_width=True)
        except Exception as e:
            st.error(f"Error removing background: {e}")

    # Crop the image to a square
    if st.button("Crop Image to Square"):
        width, height = edited_image.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        edited_image = edited_image.crop((left, top, left + min_dim, top + min_dim))
        st.subheader("Cropped Image")
        st.image(edited_image, use_column_width=True)

    # Reset the image
    if st.button("Reset Image"):
        edited_image = original_image.copy()
        st.image(edited_image, use_column_width=True)

    # Save the edited image
    if edited_image:
        img_byte_arr = io.BytesIO()
        edited_image.save(img_byte_arr, format='PNG')
        st.download_button(label="Download Edited Image", data=img_byte_arr.getvalue(), file_name="edited_image.png", mime="image/png")

# Feedback Section
st.subheader("⭐ Rate Us")
rating = st.radio("Rate the Tool", ("☆☆☆☆☆", "★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"))

# Comment Box
comment = st.text_area("Leave your feedback here", placeholder="Your feedback...")

if st.button("Submit Feedback"):
    st.success(f"Thank you for your feedback! Rating: {rating}")
    st.write("Your comment:", comment)
