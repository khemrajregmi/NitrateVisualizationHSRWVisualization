import streamlit as st

# Page Configuration
st.set_page_config(page_title="Nitratescouts", layout="wide")

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

# Page Content
st.title("Nitratescouts")

st.markdown('<p class="custom-header">Participatory development of educational modules to teach systemic interrelationships / Partizipative Entwicklung von Bildungsmodulen zur Vermittlung systemischer Zusammenhänge</p>', unsafe_allow_html=True)


# Bilingual Paragraphs
st.write("""
## English
The project aims at developing, testing, and publishing educational modules on the topic of nitrates in groundwater. The educational modules that will be developed in cooperation with citizens and various actors will cover the three areas of "environmental contexts", "digital methods" and "transformation and impact" and provide various teaching and learning tools for different target groups.

Research will be carried out in the field, e.g. at the participating project partners, as well as in various laboratories and facilities of Rhine-Waal University, such as the Green FabLab, the Computational Intelligence and Visualization Lab, or the energy and environment laboratories at the Faculty of Communication and Environment.

Citizens can actively participate in the development and implementation of these measures, for example in sampling, measurement or module development.

By developing different teaching and learning tools, the actors are to be sensitised to the problem of elevated nitrate levels in groundwater and invited to cooperate in developing solutions for sustainable action.

## Deutsch
Ziel des Projektes ist es, in Kooperation mit Bürger*innen und verschiedenen Akteur*innen Bildungsmodule zum Thema Nitrat im Grundwasser zu entwickeln, zu erproben und im Anschluss über verschiedene Netzwerke bereitzustellen. Die gemeinsam zu entwickelnden Bildungsmodule sollen die drei Bereiche „Umweltzusammenhänge“, „Digitale Methoden“ sowie „Transformation und Wirkung“ umfassen für die dann schrittweise diverse Lehr-und Lern-Tools für unterschiedliche Zielgruppen entwickelt werden.

Geforscht wird dabei sowohl draußen im Gelände, z. B. bei den teilnehmenden Projektpartnern, als auch in verschiedenen Laboren und Einrichtungen der Hochschule Rhein-Waal wie dem Green FabLab, dem Computational Intelligence and Visualization Lab, oder den Energie- und Umweltlaboren der Fakultät Kommunikation und Umwelt.

Bürger*innen können sich aktiv bei der Entwicklung und Umsetzung dieser Maßnahmen,  zum Beispiel bei der Probenahme, der Messung oder der Modulentwicklung beteiligen.

Durch die Entwicklung der Module als Lehr- und Lern-Tools sollen die Akteur*innen für die Problematik erhöhter Nitratgehalte im Grundwasser sensibilisiert werden und gemeinsam Lösungsansätze für nachhaltiges Handeln erarbeiten.""")

# You can add more content here as needed

