import streamlit as st
import pandas as pd
from PIL import Image
import io
import os

# Get the path to the current directory
current_dir = os.path.dirname(__file__)

# Define the image file name and Excel file name
image_filename = "sample.png"
excel_filename = "demo_data.xlsx"

# Concatenate the directory and filename to get the full path
image_path = os.path.join(current_dir, image_filename)

# Load your image
image = Image.open(image_path)

# Display the image
st.image(image, caption='Your Image', use_column_width=True)

# Convert the image to bytes
image_bytes = io.BytesIO()
image.save(image_bytes, format='PNG')
image_bytes = image_bytes.getvalue()

# Display a download button for the image
if st.button("Download Image"):
    st.download_button(
        label="Download Image",
        data=image_bytes,
        file_name=image_filename,
        mime="image/png",
    )

# Load your DataFrame for the Excel sheet
# Here you should load your DataFrame from wherever it's stored
# For demonstration purposes, I'll create a simple DataFrame
df = pd.DataFrame({
    'Column1': [1, 2, 3],
    'Column2': ['A', 'B', 'C']
})

# Display a download button for the Excel sheet
if st.button("Download Excel Sheet"):
    excel_data = df.to_excel(index=False, encoding="utf-8-sig")
    st.download_button(
        label="Download Excel Sheet",
        data=excel_data,
        file_name=excel_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
