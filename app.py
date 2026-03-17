import streamlit as st
import io
import os
from google.cloud import vision
from openpyxl import Workbook, load_workbook

# 1. AUTHENTICATION
# Ensure your 'key.json' from Google Cloud is in the same folder
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your_key.json'

def detect_handwriting(image_content):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text

def create_excel(text_data):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Scanned Expenses"
    
    # Headers
    ws.append(["Raw AI Extraction", "Verified Date", "Item", "Amount"])
    
    # Split lines and add to Excel
    lines = text_data.split('\n')
    for line in lines:
        ws.append([line]) # We put raw text first so you can verify it
        
    wb.save(output)
    return output.getvalue()

# 3. STREAMLIT UI
st.title("🏗️ Construction Expense Scanner")
st.write("Upload a photo of your notebook to generate an Excel file.")

uploaded_file = st.file_uploader("Choose a notebook image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show the image
    st.image(uploaded_file, caption='Uploaded Notebook Page', use_column_width=True)
    
    if st.button('Convert to Excel'):
        with st.spinner('AI is reading your handwriting...'):
            # Run OCR
            img_bytes = uploaded_file.read()
            extracted_text = detect_handwriting(img_bytes)
            
            # Create Excel
            excel_data = create_excel(extracted_text)
            
            st.success("Extraction Complete!")
            st.text_area("AI Detected Content:", extracted_text, height=200)
            
            # Download Button
            st.download_button(
                label="📥 Download Excel File",
                data=excel_data,
                file_name="scanned_expenses.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
