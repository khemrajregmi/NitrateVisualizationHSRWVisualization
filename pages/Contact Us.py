import streamlit as st

# Page Configuration
st.set_page_config(page_title="Contact Us", layout="wide")
# Displaying the banner at the top of the page
banner_url = "https://www.hochschule-rhein-waal.de/sites/default/files/images/2022/04/12/seite.jpg"
st.image(banner_url, width=1340, caption="Hochschule Rhein-Waal")
st.title("Contact Us/Kontaktiere Uns")

# Layout: Two Columns
col1, col2 = st.columns(2)

# import streamlit as st


# def custom_popup(message):
    # Display the custom pop-up
    # st.markdown(
    #     f"""
    #     <style>
    #     /* Style for the custom pop-up */
    #     .custom-popup {{
    #         position: fixed;
    #         top: 50%;
    #         left: 50%;
    #         transform: translate(-50%, -50%);
    #         background-color: #f4f4f4;
    #         border: 2px solid #3498db;
    #         border-radius: 5px;
    #         padding: 20px;
    #         z-index: 9999;
    #     }}
    #     .custom-button {{
    #         background-color: #3498db;
    #         color: white;
    #         padding: 10px 20px;
    #         border: none;
    #         border-radius: 5px;
    #         cursor: pointer;
    #         margin-top: 10px;
    #     }}
    #     </style>
    #     <div class="custom-popup">
    #         <p>{message}</p>
    #         <button class="custom-button" onclick="closePopup()">Cancel</button>
    #     </div>
    #     <script>
    #     function closePopup() {{
    #         var popup = document.querySelector('.custom-popup');
    #         popup.style.display = 'none';
    #     }}
    #     </script>
    #     """,
    #     unsafe_allow_html=True
    # )


# def main():
    # Display the custom pop-up
    # custom_popup("This is a custom pop-up message.")
    #
    # # Check if the cancel button is clicked
    # if st.button("Cancel"):
    #     # Close the pop-up
    #     custom_popup("")


# if __name__ == "__main__":
#     main()

# Left Side: Supervised by Information
with col1:
    st.write("### Supervised by")
    st.write("Frau Prof. Dr. Daniela Lud")
    st.write(f"Email: [daniela.lud@hochschule-rhein-waal.de](mailto:daniela.lud@hochschule-rhein-waal.de)")

# Right Side: Design and Development Credits with LinkedIn Icon
with col2:
    st.write("### Design and Develop by")
    st.write("Khem Raj Regmi")
    st.write(f"Email: [khem-raj.regmi@hsrw.org](mailto:khem-raj.regmi@hsrw.org)/(khem.r.regmi@gmail.com)")


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