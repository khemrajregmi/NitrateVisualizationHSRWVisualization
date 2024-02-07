import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Kleve Wesel Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="kleve_wesel_season.xltx",
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="A:K",
        nrows=7597,
    )
    # Add 'hour' column to dataframe
    year_col = pd.to_datetime(df['datum_pn'])
    df['year'] = year_col.dt.year
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()
# filter by district, cities, season

# # ---- Header ----
# st.markdown("<h1 style='text-align: center;'>App name and logo</h1>", unsafe_allow_html=True)
# st.markdown("<hr style='border: 1px solid #ffffff;'>", unsafe_allow_html=True)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

season = st.sidebar.multiselect(
    "Select the Season:",
    options=df["season"].unique(),
    default=df["season"].unique()
)

year = st.sidebar.multiselect(
    "Select Year:",
    options=df["year"].unique(),
    default=df["year"].unique()
)

district = st.sidebar.multiselect(
    "Select the District:",
    options=df["landkreis"].unique(),
    default=df["landkreis"].unique()
)

# Filter cities based on selected district
filtered_cities = df[df["landkreis"].isin(district)]["städte"].unique()

# Multiselect for Cities
city = st.sidebar.multiselect(
    "Select the City:",
    options=filtered_cities,
    default=filtered_cities
)

df_selection = df.query(
    "städte == @city & landkreis ==@district  & season == @season & year == @year"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.


# ---- MAINPAGE ----
st.title(":bar_chart: Kleve Wesel Dashboard")
st.markdown("##")



# ---- Footer ----
st.markdown(
    """
    <hr style="border: 0.5px solid #d3d3d3;">
    <div style=" padding: 10px; text-align: center; margin-top: 20px;">
        Copyright © 2024
    </div>
    """,
    unsafe_allow_html=True
)
# st.footer("Footer with a divider", divider='dash')

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
