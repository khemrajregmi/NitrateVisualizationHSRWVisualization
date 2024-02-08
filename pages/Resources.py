import streamlit as st
import pandas as pd
import os

# Get the path to the current directory
current_dir = os.path.dirname(__file__)

# Define the image file name and Excel file name
image_filename = "sample.png"
excel_filename = "demo_data.xlsx"

# Concatenate the directory and filename to get the full path
image_path = os.path.join(current_dir, image_filename)
excel_path = os.path.join(current_dir, excel_filename)

# Display the image
st.image(image_path, caption='Your Image', use_column_width=True)

# Display a download button for the image
if st.button("Download Image"):
    st.download_button(
        label="Download Image",
        data=image_path,
        file_name=image_filename,
        mime="image/png",
    )

# Read the Excel file into memory
excel_data = open(excel_path, "rb").read()

# Display a download button for the Excel sheet
if st.button("Download Excel Sheet"):
    st.download_button(
        label="Download Excel Sheet",
        data=excel_data,
        file_name=excel_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
