import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="Kleve Wesel Dashboard", page_icon=":bar_chart:", layout="wide")


# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="kleve_wesel_season.xlsx",
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="A:K",
        nrows=7597,
    )
    year_col = pd.to_datetime(df['datum_pn'])
    df['year'] = year_col.dt.year
    return df


df = get_data_from_excel()


# Add 'hour' column to dataframe


def upload_new_excel(uploaded_file):
    # Load the main template file
    main_template_file = "kleve_wesel_season.xlsx"
    main_df = pd.read_excel(io="kleve_wesel_season.xlsx",
                            engine="openpyxl",
                            sheet_name="Sheet1",
                            usecols="A:K")

    # Load the uploaded file
    uploaded_df = pd.read_excel(uploaded_file)

    # print(main_df.columns)
    # print(uploaded_df.columns)
    # Check if the headers match
    if not main_df.columns.equals(uploaded_df.columns):
        raise ValueError("Uploaded file has different headers than the main template file.")

    # Check if the columns are in the correct order
    if not main_df.columns.equals(uploaded_df.columns):
        raise ValueError("Columns in the uploaded file are not in the correct order.")

    # Append the uploaded data to the main dataframe
    # main_df = pd.concat([main_df, uploaded_df], ignore_index=True)

    # # Save the updated dataframe back to the main file
    # main_df.to_excel(main_template_file, index=False)

    return uploaded_df


# df = get_data_from_excel()
# filter by district, cities, season

# ---- Header ----
st.markdown("<h1 style='text-align: center;'>App name and logo</h1>", unsafe_allow_html=True)

st.title(":bar_chart: Kleve Wesel Dashboard")

st.markdown("<hr style='border: 1px solid #ffffff;'>", unsafe_allow_html=True)
# File uploader widget
uploaded_file = st.file_uploader("Add Excel file to your dataset", type=["xlsx", "xls"])
try:
    if uploaded_file:
        df = upload_new_excel(uploaded_file)
        year_col = pd.to_datetime(df['datum_pn'])
        df['year'] = year_col.dt.year
except ValueError as e:
    st.error(str(e))

# testing whether the data changed
# print(df.shape)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

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

df_selection = df.query(
    "städte == @city & landkreis ==@district  & season == @season & year == @year"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()  # This will halt the app from further execution.

# ---- MAINPAGE ----

# ---- Line Chart ----
st.header("Line Chart")
df2 = df_selection[['year', 'landkreis', 'messergebnis_c']].copy()
average_df = df2.groupby(['year', 'landkreis']).mean().reset_index()
fig_line = px.line(average_df, x='year', y='messergebnis_c', color='landkreis',
                   markers=True, title='Measurement by District')
fig_line.update_layout(yaxis_title='Average measurements', legend_title_text='District',
                       xaxis=dict(dtick=2),
                       width=1000,  # Set the width of the plot
                       height=500)  # Set the height of the plot)
# Specify the order of categories on the x-axis (years)
# fig_line.update_xaxes(category_order='total ascending')
st.plotly_chart(fig_line)

# ---- Bar Chart ----
st.header("Bar Chart")
df3 = df_selection[['städte', 'messergebnis_c']].copy()
average_df = df3.groupby(['städte']).mean().reset_index()
fig_bar = px.bar(average_df, x='städte', y='messergebnis_c', title='Measurement by Cities')
fig_bar.update_layout(xaxis_title='City', yaxis_title='Average measurements',
                      width=1000,  # Set the width of the plot
                      height=500
                      )

st.plotly_chart(fig_bar)

# ---- Bubble Chart ---
# Creating a bubble chart using plotly express
fig_bubble = px.scatter(average_df, x='städte', y='messergebnis_c',
                        size='messergebnis_c', hover_data=['messergebnis_c'],
                        title='Bubble Chart - Measurement by District')
fig_bubble.update_layout(xaxis_title='City', yaxis_title='Average measurements',
                         width=1000,  # Set the width of the plot
                         height=500)
st.plotly_chart(fig_bubble)

# ---- Pie Chart ----
st.header("2D Pie Chart")
fig_pie = px.pie(average_df, names='städte', values='messergebnis_c', title='Measurement by Cities')
fig_pie.update_layout(width=1000,  # Set the width of the plot
                      height=500)
st.plotly_chart(fig_pie)

st.header("3D Pie Chart")
# Rename headers
new_headers = {'städte': 'city', 'messergebnis_c': 'measurement'}
average_df.rename(columns=new_headers, inplace=True)
# fig_pie = px.pie(average_df, names='städte', values='messergebnis_c', title='Measurement by Cities')
# st.plotly_chart(fig_pie)


pie_chart_data = average_df[['city', 'measurement']]
pie_chart_array = pie_chart_data.to_dict(orient='records')

components.html(f""" 
<!-- Styles -->
<style>
#chartdiv {{
  width: 100%;
  height: 1000px;
}}

</style>

<!-- Resources -->
<script src="https://cdn.amcharts.com/lib/4/core.js"></script>
<script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
<script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>

<!-- Chart code -->
<script>
am4core.ready(function() {{

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create("chartdiv", am4charts.PieChart3D);
chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

chart.legend = new am4charts.Legend();

chart.data = {pie_chart_array};

var series = chart.series.push(new am4charts.PieSeries3D());
series.dataFields.category = "city";
series.dataFields.value = "measurement";

}}); // end am4core.ready()
</script>

<!-- HTML -->
<div id="chartdiv"></div>

""", height=1000)

# ---- Scatter Plot ----
st.header("Scatter Plot")

# Create a scatter plot using the same data
# fig_scatter = px.scatter(df2, x='städte', y='messergebnis_c', title='Measurement by Cities (Scatter Plot)')
fig_scatter = px.scatter(df3, x='städte', y='messergebnis_c', color="städte",
                         title='Measurement by Cities (Scatter Plot)')
fig_scatter.update_layout(xaxis_title='City', yaxis_title='Measurement',
                          width=1000,  # Set the width of the plot
                          height=500)
st.plotly_chart(fig_scatter)

# ---- Intensity Graph (Heatmap) ----
st.header("Intensity Graph ")
fig_intensity = px.imshow([average_df['measurement']], x=average_df['city'], y=['Average Measurement'])
fig_intensity.update_layout(xaxis_title='City', width=1000,  # Set the width of the plot
                            height=500)
st.plotly_chart(fig_intensity)

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