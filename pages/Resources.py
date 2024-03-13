import streamlit as st
import pandas as pd
import os


st.title("Resources/Ressourcen")

st.markdown('<p class="custom-header">Here you can download and preview the datasets / Hier können Sie die Datensätze herunterladen und in der Vorschau anzeigen</p>', unsafe_allow_html=True)

# Get the path to the current directory
current_dir = os.path.dirname(__file__)

# Define the image file name and Excel file name
image_filename = "sample.png"
excel_filename = "demo_data.xlsx"

# Concatenate the directory and filename to get the full path
image_path = os.path.join(current_dir, image_filename)
excel_path = os.path.join(current_dir, excel_filename)

# Display the image
st.image(image_path, caption='Figure: A sample image of excel dataset with relevant fields /Ein Beispielbild von Excel-Datensätzen mit relevanten Feldern', use_column_width=True)

# Display a download button for the image
if st.button("Download Image  / Bilder herunterladen "):
    st.download_button(
        label="Click here to confirm your download/Klicken Sie hier, um Ihren Download zu bestätigen",
        data=image_path,
        file_name=image_filename,
        mime="image/png",
    )

# Read the Excel file into memory
excel_data = open(excel_path, "rb").read()

# Custom HTML for the logo in the top right
logo_url = "https://www.hochschule-rhein-waal.de/sites/default/files/images/2022/04/12/300617022004d3sq.png"
st.markdown(f"""
<style>
.logo {{
    position: absolute;
    top: 0;
    right: 0;
    margin: 25px;
}}
.markdown-text-container {{
    padding-top: 100px;
}}

h1 {{
    color: green !important;
}}
h2 {{
    color: blue !important;
}}
</style>
<img class="logo" src="{logo_url}" alt="Logo" height="100">
""", unsafe_allow_html=True)

# Display a download button for the Excel sheet
if st.button("Download Excel Sheet"):
    st.download_button(
        label="Click here to confirm your download/Klicken Sie hier, um Ihren Download zu bestätigen",
        data=excel_data,
        file_name=excel_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )



