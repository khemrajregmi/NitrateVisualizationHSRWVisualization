import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="Data exploration", page_icon=":bar_chart:", layout="wide")


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
    main_template_file = "kleve_wesel_season.xlsx"
    main_df = pd.read_excel(io="kleve_wesel_season.xlsx",
                            engine="openpyxl",
                            sheet_name="Sheet1",
                            usecols="A:K")

    uploaded_df = pd.read_excel(uploaded_file)

    if not main_df.columns.equals(uploaded_df.columns):
        raise ValueError("Uploaded file has different headers than the main template file.")

    if not main_df.columns.equals(uploaded_df.columns):
        raise ValueError("Columns in the uploaded file are not in the correct order.")
    return uploaded_df


# df = get_data_from_excel()
# filter by district, cities, season

# ---- Header ----
# Add three links in the header


st.markdown("""
    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: #f0f0f0;">
        <a href="/" target="_blank">Home</a>
        <a href="/About_Us" target="_blank">About Us</a>
        <a href="/Resources" target="_blank">Resources</a>
        <a href="/Contact_Us" target="_blank">Contact Us</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div id="top"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Groundwater Nitrate Representation</h1>", unsafe_allow_html=True)

st.title(":bar_chart: Data representation in Kleve and Wesel")

st.markdown("<hr style='border: 1px solid #000;'>", unsafe_allow_html=True)
# File uploader widget
uploaded_file = st.file_uploader("Add Excel file to your dataset", type=["xlsx", "xls"])

try:
    if uploaded_file:
        with st.spinner('Uploading and processing the file...'):
            df = upload_new_excel(uploaded_file)
            year_col = pd.to_datetime(df['datum_pn'])
            df['year'] = year_col.dt.year

        st.success('File is successfully uploaded and processed!')
        # Display your dataframe or any other content here
    else:
        st.warning("Original dataset is used for exploration.")

except ValueError as e:
    st.error(str(e))
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

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
# Anchor links
st.markdown("### Jump to Graphs")

# Create a horizontal layout using columns
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

# Add buttons to each column
if col1.button("Line Chart"):
    st.markdown('<a href="#line-chart">Go to Line Chart</a>', unsafe_allow_html=True)
if col2.button("Bar Chart"):
    st.markdown('<a href="#bar-chart">Go to Bar Chart</a>', unsafe_allow_html=True)
if col3.button("Bubble Chart"):
    st.markdown('<a href="#bubble-chart">Go to Bubble Chart</a>', unsafe_allow_html=True)
if col4.button("2D Chart"):
    st.markdown('<a href="#2d-chart">Go to 2D Chart</a>', unsafe_allow_html=True)
if col5.button("3D Chart"):
    st.markdown('<a href="#3d-chart">Go to 3D Chart</a>', unsafe_allow_html=True)
if col6.button("Scatter Plot"):
    st.markdown('<a href="#scatter-plot">Go to Scatter Plot</a>', unsafe_allow_html=True)
if col7.button("Intensity graph"):
    st.markdown('<a href="#intensity-graph">Go to Intensity graph</a>', unsafe_allow_html=True)

# ---- Line Chart ----
st.markdown('<div id="line-chart"></div>', unsafe_allow_html=True)
st.header("Line Chart")

# Creating a collapsible section
with st.expander("Line chart detail"):
    st.write(
        "A line chart, also known as a line graph or curve chart, is a graphical representation used to display data "
        "points connected by straight lines."
        "This type of chart is particularly useful for visualizing trends, changes, and relationships in data over a "
        "continuous interval, often time.")
    # You can add more Streamlit widgets inside the expander to enrich your app
    st.write(
        "The x-axis shows the years from 1978 to 2022, and the y-axis shows the average measurement. The chart includes two districts, Wesel and Kleve.")

df2 = df_selection[['year', 'landkreis', 'messergebnis_c']].copy()
average_df = df2.groupby(['year', 'landkreis']).mean().reset_index()
fig_line = px.line(average_df, x='year', y='messergebnis_c', color='landkreis',
                   markers=True, title='Measurement by District')
fig_line.update_layout(yaxis_title='Average measurements', legend_title_text='District', xaxis_title="Year",
                       xaxis=dict(dtick=2),
                       width=1000,
                       height=500)
st.plotly_chart(fig_line)

# ---- Bar Chart ----
st.markdown('<div id="bar-chart"></div>', unsafe_allow_html=True)
st.header("Bar Chart")
with st.expander("Line chart detail"):
    st.write(
        "A line chart, also known as a line graph or curve chart, is a graphical representation used to display data "
        "points connected by straight lines."
        "This type of chart is particularly useful for visualizing trends, changes, and relationships in data over a "
        "continuous interval, often time.")
    # You can add more Streamlit widgets inside the expander to enrich your app
    st.write(
        "The x-axis shows the years from 1978 to 2022, and the y-axis shows the average measurement. The chart includes two districts, Wesel and Kleve.")

df3 = df_selection[['städte', 'messergebnis_c']].copy()
average_df = df3.groupby(['städte']).mean().reset_index()
fig_bar = px.bar(average_df, x='städte', y='messergebnis_c', title='Measurement by Cities')
fig_bar.update_layout(xaxis_title='City', yaxis_title='Average measurements',
                      width=1000,
                      height=500
                      )

st.plotly_chart(fig_bar)

# ---- Bubble Chart ---
st.header("Bubble Chart")
with st.expander("Bubble Chart detail"):
    st.write(
        "A line chart, also known as a line graph or curve chart, is a graphical representation used to display data "
        "points connected by straight lines."
        "This type of chart is particularly useful for visualizing trends, changes, and relationships in data over a "
        "continuous interval, often time.")
    # You can add more Streamlit widgets inside the expander to enrich your app
    st.write(
        "The x-axis shows the years from 1978 to 2022, and the y-axis shows the average measurement. The chart includes two districts, Wesel and Kleve.")

st.markdown('<div id="bubble-chart"></div>', unsafe_allow_html=True)
fig_bubble = px.scatter(average_df, x='städte', y='messergebnis_c',
                        size='messergebnis_c', hover_data=['messergebnis_c'],
                        title='Bubble Chart - Measurement by District')
fig_bubble.update_layout(xaxis_title='City', yaxis_title='Average measurements',
                         width=1000,  # Set the width of the plot
                         height=500)
st.plotly_chart(fig_bubble)

# ---- Pie Chart ----
st.markdown('<div id="2d-chart"></div>', unsafe_allow_html=True)
st.header("2D Pie Chart")
with st.expander("Line chart detail"):
    st.write(
        "A line chart, also known as a line graph or curve chart, is a graphical representation used to display data "
        "points connected by straight lines."
        "This type of chart is particularly useful for visualizing trends, changes, and relationships in data over a "
        "continuous interval, often time.")
    # You can add more Streamlit widgets inside the expander to enrich your app
    st.write(
        "The x-axis shows the years from 1978 to 2022, and the y-axis shows the average measurement. The chart includes two districts, Wesel and Kleve.")

fig_pie = px.pie(average_df, names='städte', values='messergebnis_c', title='Measurement by Cities')
fig_pie.update_layout(width=1000,  # Set the width of the plot
                      height=500)
st.plotly_chart(fig_pie)

st.header("3D Pie Chart")
with st.expander("Line chart detail"):
    st.write(
        "A line chart, also known as a line graph or curve chart, is a graphical representation used to display data "
        "points connected by straight lines."
        "This type of chart is particularly useful for visualizing trends, changes, and relationships in data over a "
        "continuous interval, often time.")
    # You can add more Streamlit widgets inside the expander to enrich your app
    st.write(
        "The x-axis shows the years from 1978 to 2022, and the y-axis shows the average measurement. The chart includes two districts, Wesel and Kleve.")

st.markdown('<div id="3d-chart"></div>', unsafe_allow_html=True)
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
st.markdown('<div id="scatter-plot"></div>', unsafe_allow_html=True)
st.header("Scatter Plot")
with st.expander("Scatter Plot detail"):
    st.write(
        "A line chart, also known as a line graph or curve chart, is a graphical representation used to display data "
        "points connected by straight lines."
        "This type of chart is particularly useful for visualizing trends, changes, and relationships in data over a "
        "continuous interval, often time.")
    # You can add more Streamlit widgets inside the expander to enrich your app
    st.write(
        "The x-axis shows the years from 1978 to 2022, and the y-axis shows the average measurement. The chart includes two districts, Wesel and Kleve.")

# Create a scatter plot using the same data
# fig_scatter = px.scatter(df2, x='städte', y='messergebnis_c', title='Measurement by Cities (Scatter Plot)')
fig_scatter = px.scatter(df3, x='städte', y='messergebnis_c', color="städte",
                         title='Measurement by Cities (Scatter Plot)')
fig_scatter.update_layout(xaxis_title='City', yaxis_title='Measurement',
                          width=1000,  # Set the width of the plot
                          height=500)
st.plotly_chart(fig_scatter)

# ---- Intensity Graph (Heatmap) ----
st.markdown('<div id="intensity-graph"></div>', unsafe_allow_html=True)
st.header("Intensity Graph ")
with st.expander("Intensity Graph detail"):
    st.write(
        "An intensity graph is a type of data visualization that uses color or shading to "
        "represent variations in intensity or magnitude of a measured quantity. In the context following chart,"
        " the intensity likely refers to the average measurement value for each city.")

    st.write("Visualize the average measurement values for different cities.")
    st.write("Identify cities with higher or lower average measurements.")
    st.write("Compare the distribution of average measurements across different cities.")

fig_intensity = px.imshow([average_df['measurement']], x=average_df['city'], y=['Average Measurement'])
fig_intensity.update_layout(xaxis_title='City', width=1000,  # Set the width of the plot
                            height=500)
st.plotly_chart(fig_intensity)

if st.button('Go to top'):
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)

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
            .st-emotion-cache-79elbk{display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
