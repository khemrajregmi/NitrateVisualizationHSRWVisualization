import streamlit as st

st.set_page_config(page_title="Contact Us", layout="wide")

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

st.title("Contact Us/Kontaktiere uns")

# Layout: Two Columns
col1, col2 = st.columns(2)

# Left Side: Supervised by Information
with col1:
    st.write("### Supervised by")
    st.write("Frau Prof. Dr. Daniela Lud")
    st.write(f"Email: [daniela.lud@hochschule-rhein-waal.de](mailto:daniela.lud@hochschule-rhein-waal.de)")

# Right Side: Design and Development Credits with LinkedIn Icon
with col2:
    st.write("### Design and Develop by")
    st.write("Khem Raj Regmi")
    st.write("Email: [khem-raj.regmi@hsrw.org](mailto:khem-raj.regmi@hsrw.org)/(khem.r.regmi@gmail.com)")

# Define the paths to your images
image_path_1 = 'resources/crops.JPG'
# image_path_2 = 'resources/crops2.JPG'

# Create two columns for the images to sit side-by-side
col1, col2 = st.columns(2)

# Display the first image in the first column
with col1:
    st.image(image_path_1, width=956, caption="Figure: Crops from green fab lab HSRW")

# Display the second image in the second column
# with col2:
    # st.image(image_path_2, width=500, caption="Figure: Crops from green fab lab HSRW")