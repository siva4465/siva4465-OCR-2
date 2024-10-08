import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Streamlit app title
st.title("OCR and Document Search Web Application")

# Function to extract text from the image using Tesseract
def extract_text_from_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray, lang='eng+hin')
    return extracted_text

# Function to search for keywords in the extracted text and highlight them
def highlight_keywords(extracted_text, keywords):
    for keyword in keywords:
        if keyword:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            extracted_text = pattern.sub(f'<span style="background-color: black; color: #39FF14;">{keyword}</span>', extracted_text)
    return extracted_text

# Upload image section
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Extract text from the image
    st.write("Extracting text from the image...")
    extracted_text = extract_text_from_image(image)
    
    # Display the extracted text
    st.subheader("Extracted Text:")
    st.write(extracted_text)

    # Search functionality
    keyword_input = st.text_input("Enter keywords to search in the extracted text (separate by commas):")
    search_button = st.button("Search")

    if search_button and keyword_input:
        # Split the input into keywords and remove extra spaces
        keywords = [keyword.strip() for keyword in keyword_input.split(',')]

        highlighted_text = highlight_keywords(extracted_text, keywords)

        # Check if any keywords are found in the extracted text
        found_keywords = [keyword for keyword in keywords if keyword.lower() in extracted_text.lower()]
        if found_keywords:
            st.success(f"Keywords '{', '.join(found_keywords)}' found in the extracted text!")
            st.markdown(highlighted_text, unsafe_allow_html=True)
        else:
            st.error("No keywords found in the extracted text.")
else:
    st.write("Please upload an image to start the OCR process.")
