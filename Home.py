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
        <a href="/" target="_blank">Hauptseite</a>
        <a href="/About_Us" target="_blank">Über uns</a>
        <a href="/Resources" target="_blank">Ressourcen</a>
        <a href="/Contact_Us" target="_blank">Kontaktiere uns</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div id="top"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Darstellung Nitrat im Grundwasser</h1>", unsafe_allow_html=True)
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

st.title(":bar_chart: Darstellungen der Daten für Kleve und Wesel")

st.markdown("<hr style='border: 1px solid #000;'>", unsafe_allow_html=True)
# File uploader widget
uploaded_file = st.file_uploader("Lade deinen eigenen Datensatz als Excel-Tabelle hoch", type=["xlsx", "xls"])

try:
    if uploaded_file:
        with st.spinner('Die Datei wird hochgeladen und verarbeitet...'):
            df = upload_new_excel(uploaded_file)
            year_col = pd.to_datetime(df['datum_pn'])
            df['year'] = year_col.dt.year

        st.success('Datei wurde erfolgreich hochgeladen und verarbeitet!')
        # Display your dataframe or any other content here
    else:
        st.warning("Für die Exploration wird der Originaldatensatz verwendet.")

except ValueError as e:
    st.error(str(e))
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

# ---- SIDEBAR ----

st.sidebar.header("Bitte hier filtern:")

district = st.sidebar.multiselect(
    "Wähle den Landkreis aus:",
    options=df["landkreis"].unique(),
    default=df["landkreis"].unique()
)

# Filter cities based on selected district
filtered_cities = df[df["landkreis"].isin(district)]["städte"].unique()

# Multiselect for Cities
city = st.sidebar.multiselect(
    "Wähle die Stadt aus:",
    options=filtered_cities,
    default=filtered_cities
)

season = st.sidebar.multiselect(
    "Wähle die Jahreszeit aus:",
    options=df["season"].unique(),
    default=df["season"].unique()
)

year = st.sidebar.multiselect(
    "Wähle das Jahr aus:",
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
st.markdown("### Zu den Grafiken navigieren")

# Create a horizontal layout using columns
# Assuming you have already defined your columns layout
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

if col1.button("Liniendiagramm"):
    st.markdown('<a href="#line-chart">Gehe zum Liniendiagramm</a>', unsafe_allow_html=True)
if col2.button("Balkendiagramm"):
    st.markdown('<a href="#bar-chart">Gehe zum Balkendiagramm</a>', unsafe_allow_html=True)
if col3.button("Blasendiagramm"):
    st.markdown('<a href="#bubble-chart">Gehe zum Blasendiagramm</a>', unsafe_allow_html=True)
if col4.button("2D-Diagramm"):
    st.markdown('<a href="#2d-chart">Gehe zum 2D-Diagramm</a>', unsafe_allow_html=True)
if col5.button("3D-Diagramm"):
    st.markdown('<a href="#3d-chart">Gehe zum 3D-Diagramm</a>', unsafe_allow_html=True)
if col6.button("Streudiagramm"):
    st.markdown('<a href="#scatter-plot">Gehe zum Streudiagramm</a>', unsafe_allow_html=True)
if col7.button("Intensitätsdiagramm"):
    st.markdown('<a href="#intensity-graph">Gehe zum Intensitätsdiagramm</a>', unsafe_allow_html=True)

# ---- Line Chart ----
st.markdown('<div id="line-chart"></div>', unsafe_allow_html=True)
# Header in English and German
st.header("Line Chart / Liniendiagramm")

# Creating a collapsible section in English and German
with st.expander("Line chart detail / Details zum Liniendiagramm"):
    st.write(
        "A line chart, also known as a line graph or curve chart, is a graphical representation used to display data "
        "points connected by straight lines. "
        "This type of chart is particularly useful for visualizing trends, changes, and relationships in data over a "
        "continuous interval, often time. "
        "The x-axis shows the years from 1978 to 2022, and the y-axis shows the average measurement. The chart includes two districts, Wesel and Kleve."
    )

    st.write(
        "---"
    )

    st.write(
        "Ein Liniendiagramm, auch bekannt als Liniengrafik oder Kurvendiagramm, ist eine grafische Darstellung, die verwendet wird, um Datenpunkte anzuzeigen, "
        "die durch gerade Linien verbunden sind. "
        "Diese Art von Diagramm ist besonders nützlich, um Trends, Änderungen und Beziehungen in Daten über ein "
        "kontinuierliches Intervall, oft Zeit, zu visualisieren. "
        "Die x-Achse zeigt die Jahre von 1978 bis 2022, und die y-Achse zeigt das durchschnittliche Messergebnis. Das Diagramm umfasst zwei Bezirke, Wesel und Kleve."
    )

df2 = df_selection[['year', 'landkreis', 'messergebnis_c']].copy()
average_df = df2.groupby(['year', 'landkreis']).mean().reset_index()

# Creating the line chart
fig_line = px.line(average_df, x='year', y='messergebnis_c', color='landkreis',
                   markers=True, title='Messungen nach Landkreis')
fig_line.update_layout(yaxis_title='Durchschnittliche Messung', legend_title_text='District', xaxis_title="Year",
                       xaxis=dict(dtick=2),
                       width=1000,
                       height=500)

# Check if any average measurement is more than 40
if average_df['messergebnis_c'].max() > 50:
    # Add a dark horizontal line at y=50
    fig_line.add_hline(y=50, line_dash="dash", line_color="black",
                       annotation_text="Grenzwert für Trinkwasser", annotation_position="bottom right")

# Display the chart in Streamlit
st.plotly_chart(fig_line)

# ---- Bar Chart ----
st.markdown('<div id="bar-chart"></div>', unsafe_allow_html=True)
st.header("Bar Chart / Balkendiagramm")

# Creating a collapsible section in English and German
with st.expander("Bar Chart detail / Details zum Balkendiagramm"):
    st.write(
        "A bar chart, also known as a bar graph, is a graphical representation of categorical data with rectangular bars. "
        "The length of each bar is proportional to the value it represents, making it easy to compare different categories. "
        "This type of chart is particularly useful for visualizing comparisons between different groups or categories. "
        "The x-axis of this bar chart shows the cities, and the y-axis shows the average measurement. "
        "The chart represents the average measurements for different cities in the dataset."
    )

    st.write(
        "---"
    )

    st.write(
        "Ein Balkendiagramm, auch bekannt als Säulendiagramm, ist eine grafische Darstellung von kategorialen Daten mit rechteckigen Balken. "
        "Die Länge jedes Balkens ist proportional zum dargestellten Wert, was den Vergleich verschiedener Kategorien erleichtert. "
        "Diese Art von Diagramm ist besonders nützlich, um Vergleiche zwischen verschiedenen Gruppen oder Kategorien zu visualisieren. "
        "Die x-Achse dieses Balkendiagramms zeigt die Städte, und die y-Achse zeigt das durchschnittliche Messergebnis. "
        "Das Diagramm stellt die durchschnittlichen Messungen für verschiedene Städte im Datensatz dar."
    )

# Assuming df_selection is already defined
df3 = df_selection[['städte', 'messergebnis_c']].copy()
average_df = df3.groupby(['städte']).mean().reset_index()

# Assuming df_selection is defined elsewhere
df3 = df_selection[['städte', 'messergebnis_c']].copy()
average_df = df3.groupby(['städte']).mean().reset_index()

# Create the bar chart
fig_bar = px.bar(average_df, x='städte', y='messergebnis_c', title='Messungen nach Stadt')
fig_bar.update_layout(xaxis_title='Stadt', yaxis_title='Durchschnittliche Messung',
                      width=1000,
                      height=500
                      )

# Check if any average measurement is more than 50
if average_df['messergebnis_c'].max() > 50:
    # Add a dark horizontal line at y=50
    fig_bar.add_hline(y=50, line_dash="dash", line_color="black",
                       annotation_text="Grenzwert für Trinkwasser", annotation_position="bottom right")

# Render the chart in Streamlit
st.plotly_chart(fig_bar)

# ---- Bubble Chart ---
st.header("Bubble Chart / Blasendiagramm")

# Creating a collapsible section in English and German
with st.expander("Bubble Chart detail / Details zum Blasendiagramm"):
    st.write(
        "A bubble chart is a type of scatter plot where data points are displayed as bubbles. "
        "Similar to a scatter plot, it uses Cartesian coordinates to represent the values of two variables. "
        "In addition to the x and y coordinates, a bubble chart also uses the size of the bubbles to encode a third variable. "
        "The size of each bubble is proportional to the value of the third variable, providing a visual comparison between data points. "
        "This type of chart is particularly useful for visualizing relationships between three variables and identifying patterns within the data."
    )

    st.write(
        "---"
    )

    st.write(
        "Ein Blasendiagramm ist eine Art Streudiagramm, bei dem Datenpunkte als Blasen dargestellt werden. "
        "Ähnlich wie ein Streudiagramm verwendet es kartesische Koordinaten, um die Werte von zwei Variablen darzustellen. "
        "Zusätzlich zu den x- und y-Koordinaten verwendet ein Blasendiagramm auch die Größe der Blasen, um eine dritte Variable zu kodieren. "
        "Die Größe jeder Blase ist proportional zum Wert der dritten Variable, was einen visuellen Vergleich zwischen Datenpunkten ermöglicht. "
        "Diese Art von Diagramm ist besonders nützlich, um Beziehungen zwischen drei Variablen zu visualisieren und Muster in den Daten zu identifizieren."
    )
st.markdown('<div id="bubble-chart"></div>', unsafe_allow_html=True)
fig_bubble = px.scatter(average_df, x='städte', y='messergebnis_c',
                        size='messergebnis_c', hover_data=['messergebnis_c'],
                        title='Bubble Chart - Messungen nach Landkreis')
fig_bubble.update_layout(xaxis_title='Stad', yaxis_title='Durchschnittliche Messung',
                         width=1000,  # Set the width of the plot
                         height=500)

if average_df['messergebnis_c'].max() > 50:
    # Add a dark horizontal line at y=50
    fig_bubble.add_hline(y=50, line_dash="dash", line_color="black",
                       annotation_text="Grenzwert für Trinkwasser", annotation_position="bottom right")
st.plotly_chart(fig_bubble)


# ---- Pie Chart ----
st.markdown('<div id="2d-chart"></div>', unsafe_allow_html=True)
st.header("2D Pie Chart / 2D-Kreisdiagramm")

# Creating a collapsible section in English and German
with st.expander("2D Pie Chart detail / Details zum 2D-Kreisdiagramm"):
    st.write(
        "A 2D pie chart is a circular statistical graphic divided into slices to illustrate numerical proportions. "
        "Each slice of the pie represents a proportion of the whole, and the size of each slice is proportional to "
        "the quantity it represents. The chart is called '2D' because it is flat and does not include depth or perspective. "
        "Pie charts are commonly used to show percentages, proportions, or distributions of categorical data. "
        "Each slice of the pie typically represents a category, and the entire pie represents the total sum of the data. "
        "This type of chart is particularly useful for visualizing the composition of a whole and understanding "
        "the relative sizes of different parts within that whole."
    )


    st.write(
        "---"
    )

    st.write(
        "Ein 2D-Kreisdiagramm ist eine kreisförmige statistische Grafik, die in Segmente unterteilt ist, um numerische Verhältnisse zu veranschaulichen. "
        "Jedes Segment des Kreises stellt einen Anteil des Ganzen dar, und die Größe jedes Segments ist proportional zu "
        "der Menge, die es repräsentiert. Das Diagramm wird als '2D' bezeichnet, weil es flach ist und keine Tiefe oder Perspektive enthält. "
        "Kreisdiagramme werden häufig verwendet, um Prozentsätze, Anteile oder Verteilungen von kategorischen Daten zu zeigen. "
        "Jedes Segment des Kreises stellt typischerweise eine Kategorie dar, und der gesamte Kreis repräsentiert die Gesamtsumme der Daten. "
        "Diese Art von Diagramm ist besonders nützlich, um die Zusammensetzung eines Ganzen zu visualisieren und "
        "die relativen Größen verschiedener Teile innerhalb dieses Ganzen zu verstehen."
    )

fig_pie = px.pie(average_df, names='städte', values='messergebnis_c', title='Measurement by Cities')
fig_pie.update_layout(width=1000,  # Set the width of the plot
                      height=500)
st.plotly_chart(fig_pie)

st.header("3D Pie Chart / 3D-Kreisdiagramm")

# Creating a collapsible section in English and German
with st.expander("3D Pie Chart detail / Details zum 3D-Kreisdiagramm"):
    st.write(
        "A 3D pie chart is a variation of the traditional 2D pie chart, with an added dimension of depth. "
        "Similar to a 2D pie chart, it represents numerical proportions using slices of a circular graphic. "
        "However, the 3D pie chart adds depth to each slice, creating the illusion of a three-dimensional space. "
        "Each slice of the pie chart still represents a proportion of the whole, with the size of each slice "
        "proportional to the quantity it represents. The 3D effect is used to enhance visualization by adding depth "
        "and perspective, making it easier to distinguish between slices and providing a more immersive viewing experience. "
        "This type of chart is particularly useful for presenting data in a visually appealing and engaging manner, "
        "especially when depth perception is important for understanding the data."
    )

    st.write(
        "---"
    )

    st.write(
        "Ein 3D-Kreisdiagramm ist eine Variation des traditionellen 2D-Kreisdiagramms, mit einer zusätzlichen Dimension der Tiefe. "
        "Ähnlich wie ein 2D-Kreisdiagramm stellt es numerische Verhältnisse mithilfe von Segmenten einer kreisförmigen Grafik dar. "
        "Das 3D-Kreisdiagramm fügt jedoch jedem Segment Tiefe hinzu, was die Illusion eines dreidimensionalen Raums erzeugt. "
        "Jedes Segment des Kreisdiagramms repräsentiert nach wie vor einen Anteil des Ganzen, wobei die Größe jedes Segments "
        "proportional zur dargestellten Menge ist. Der 3D-Effekt wird verwendet, um die Visualisierung durch Hinzufügen von Tiefe "
        "und Perspektive zu verbessern, was es einfacher macht, zwischen den Segmenten zu unterscheiden und ein immersiveres Betrachtungserlebnis zu bieten. "
        "Diese Art von Diagramm ist besonders nützlich, um Daten auf eine visuell ansprechende und ansprechende Weise zu präsentieren, "
        "insbesondere wenn die Tiefenwahrnehmung für das Verständnis der Daten wichtig ist."
    )

st.markdown('<div id="3d-chart"></div>', unsafe_allow_html=True)
new_headers = {'städte': 'city', 'messergebnis_c': 'measurement'}
average_df.rename(columns=new_headers, inplace=True)
# fig_pie = px.pie(average_df, names='städte', values='messergebnis_c', title='Messungen nach Stadt')
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
# Header in English and German
st.header("Scatter Plot / Streudiagramm")

# Creating a collapsible section in English and German
with st.expander("Scatter Plot detail / Details zum Streudiagramm"):
    st.write(
        "A scatter plot is a type of data visualization that uses Cartesian coordinates to display the values of two "
        "variables as points on a two-dimensional plane. Each point on the plot represents an observation or data point, "
        "with its position determined by the values of the two variables. The horizontal axis (x-axis) typically represents one "
        "variable, while the vertical axis (y-axis) represents the other variable. Scatter plots are particularly useful for visualizing the relationship "
        "between two continuous variables and identifying patterns, trends, or correlations within the data. "
        "This type of chart allows you to quickly assess the relationship between two variables, such as identifying "
        "whether there is a positive or negative correlation, clusters of data points, or outliers."
    )

    st.write(
        "The scatter plot shows that there is a positive correlation between the number of measurements made in "
        "a city and the size of the city. In other words, larger cities tend to have more measurements made in "
        "them than smaller cities. However, there are also some exceptions to this trend. For example, "
        "the city of Sonsbeck has a relatively small number of measurements, while the city of Kamp-Lintfort has "
        "a relatively large number of measurements."
    )

    st.write(
        "---"
    )

    st.write(
        "Ein Streudiagramm ist eine Art der Datenvisualisierung, die kartesische Koordinaten verwendet, um die Werte von zwei "
        "Variablen als Punkte auf einer zweidimensionalen Ebene darzustellen. Jeder Punkt im Diagramm repräsentiert eine Beobachtung oder einen Datenpunkt, "
        "dessen Position durch die Werte der beiden Variablen bestimmt wird. Die horizontale Achse (x-Achse) stellt typischerweise eine "
        "Variable dar, während die vertikale Achse (y-Achse) die andere Variable repräsentiert. Streudiagramme sind besonders nützlich, um die Beziehung "
        "zwischen zwei kontinuierlichen Variablen zu visualisieren und Muster, Trends oder Korrelationen innerhalb der Daten zu identifizieren. "
        "Diese Art von Diagramm ermöglicht es Ihnen, schnell die Beziehung zwischen zwei Variablen zu beurteilen, wie zum Beispiel "
        "festzustellen, ob es eine positive oder negative Korrelation gibt, Cluster von Datenpunkten oder Ausreißer."
    )

    st.write(
        "Das Streudiagramm zeigt, dass es eine positive Korrelation zwischen der Anzahl der Messungen in "
        "einer Stadt und der Größe der Stadt gibt. Mit anderen Worten, größere Städte neigen dazu, mehr Messungen zu haben "
        "als kleinere Städte. Es gibt jedoch auch einige Ausnahmen von diesem Trend. Zum Beispiel hat "
        "die Stadt Sonsbeck eine relativ kleine Anzahl von Messungen, während die Stadt Kamp-Lintfort "
        "eine relativ große Anzahl von Messungen aufweist."
    )

# Create a scatter plot using the same data
# fig_scatter = px.scatter(df2, x='städte', y='messergebnis_c', title='Measurement by Cities (Scatter Plot)')
fig_scatter = px.scatter(df3, x='städte', y='messergebnis_c', color="städte",
                         title='Messungen nach Stadt (Scatter Plot)')
fig_scatter.update_layout(xaxis_title='Stadt', yaxis_title='Measurement',
                          width=1000,  # Set the width of the plot
                          height=500)
st.plotly_chart(fig_scatter)

# ---- Intensity Graph (Heatmap) ----
st.markdown('<div id="intensity-graph"></div>', unsafe_allow_html=True)# Header in English and German
st.header("Intensity Graph / Intensitätsdiagramm")

# Creating a collapsible section in English and German
with st.expander("Intensity Graph detail / Details zum Intensitätsdiagramm"):
    st.write(
        "An intensity graph is a type of data visualization that uses color or shading to "
        "represent variations in intensity or magnitude of a measured quantity. In the context of the following chart, "
        "the intensity likely refers to the average measurement value for each city. "
        "Visualize the average measurement values for different cities. "
        "Identify cities with higher or lower average measurements. "
        "Compare the distribution of average measurements across different cities."
    )

    st.write(
        "---"
    )

    st.write(
        "Ein Intensitätsdiagramm ist eine Art der Datenvisualisierung, die Farbe oder Schattierung verwendet, um "
        "Variationen in der Intensität oder Größe einer gemessenen Menge darzustellen. Im Kontext des folgenden Diagramms "
        "bezieht sich die Intensität wahrscheinlich auf den durchschnittlichen Messwert für jede Stadt. "
        "Visualisieren Sie die durchschnittlichen Messwerte für verschiedene Städte. "
        "Identifizieren Sie Städte mit höheren oder niedrigeren Durchschnittsmessungen. "
        "Vergleichen Sie die Verteilung der Durchschnittsmessungen über verschiedene Städte."
    )

fig_intensity = px.imshow([average_df['measurement']], x=average_df['city'], y=['Durchschnittliche Messung'])
fig_intensity.update_layout(xaxis_title='Stad', width=1000,  # Set the width of the plot
                            height=500)
st.plotly_chart(fig_intensity)

if st.button('Nach oben'):
    st.markdown("<a href='#top'>Nach oben</a>", unsafe_allow_html=True)

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
