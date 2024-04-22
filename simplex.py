#!/usr/bin/env python
# coding: utf-8

# https://discuss.streamlit.io/t/how-to-use-session-state-to-save-file-uploads-and-filters/36443

# In[2]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pulp as pl
from menu2 import menu


# In[ ]:


if "projectbestand" not in st.session_state:
    st.session_state.projectbestand = None
    
st.session_state._projectbestand = st.session_state.projectbestand

def set_projectbestand():
    st.session_state.projectbestand = "tets"

if 'file' not in st.session_state:
    st.session_state.file = None

st.session_state._file = st.session_state.file

def set_file():
    st.session_state.file = st.session_state._file

if 'afdeling' not in st.session_state:
    st.session_state.afdeling = None

st.session_state._afdeling = st.session_state.afdeling

def set_afdeling():
    st.session_state.afdeling = st.session_state._afdeling

menu()


# In[ ]:


st.title("Eigen Haard")


# **input tab**

# In[ ]:


st.session_state.file = None 
st.markdown(st.session_state.afdeling)
st.markdown("**Afdeling**")
st.selectbox(
    "Welke afdeling?", 
    ['Nieuwbouw ontwikkeling', 'Nieuwbouw realisatie', 'Renovatie ontwikkeling', 'Renovatie realisatie', 'Planmatig onderhoud ontwikkeling', 
     'Planmatig onderhoud realisatie', 'Mutatie onderhoud', 'Dagelijks onderhoud'],
    index=None,
    placeholder="Selecteer een afdeling", key = "_afdeling", on_change = set_afdeling
)

st.markdown("**Projectfase**")
st.selectbox(
    "Wat is de fase van het project?",
    ['Projectdefinitie', 'Structuurontwerp', 'Voorontwerp', 'Definitief ontwerp', 'Technisch ontwerp bestek', 'Uitvoeringsgereed ontwerp', 'Gebruik'],
    index = None,
    placeholder = "Selecteer de fase van het project"
)

st.markdown("**Projectbestand**")
uploaded_file = st.file_uploader("Choose a file", help='Upload hier het projectbestand, op basis van dit bestand wordt de optimalisatie uitgevoerd. ')
st.session_state.projectbestand = uploaded_file
if uploaded_file is not None:
    # st.session_state.projectbestand = 'test'
    # st.markdown(st.session_state.projectbestand)
    dataframe = pd.read_csv(uploaded_file, sep=';')
    
    if st.session_state.afdeling in ['Nieuwbouw ontwikkeling', 'Renovatie ontwikkeling', 'Planmatig onderhoud ontwikkeling']:
        dataframe = dataframe.drop(dataframe.columns[[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 29, 31, 33, 35, 37]], axis = 1)
        dataframe.rename(columns={dataframe.columns[12]: "impact onderhoud"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[13]: "impact circulair"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[14]: "impact kwaliteit"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[15]: "impact budget"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[16]: "impact woonbeleving"}, inplace=True)
        
        dataframe = dataframe.dropna(how='all')
        dataframe = dataframe.drop(0)
        dataframe = dataframe.reset_index(drop=True)
        
    if st.session_state.afdeling in ['Nieuwbouw renovatie', 'Renovatie renovatie', 'Planmatig onderhoud renovatie', 
                                         'Mutatie onderhoud', 'Dagelijks onderhoud']:
        dataframe = dataframe.drop(dataframe.columns[[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 29, 31, 33, 35]], axis = 1)
        dataframe.rename(columns={dataframe.columns[12]: "impact onderhoud"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[13]: "impact circulair"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[14]: "impact kwaliteit"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[15]: "impact budget"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[16]: "impact woonbeleving"}, inplace=True)
        
        dataframe = dataframe.dropna(how='all')
        dataframe = dataframe.drop(0)
        dataframe = dataframe.reset_index(drop=True)

    st.markdown("dataframe") 
    st.dataframe(dataframe, hide_index = True)

    dataframe['impact O'] = dataframe.groupby(['PRODUCTGROEP'])['impact onderhoud'].transform('count')/dataframe.groupby(['PRODUCTGROEP'])['PRODUCTGROEP'].transform('count')
    dataframe['impact CD'] = dataframe.groupby(['PRODUCTGROEP'])['impact circulair'].transform('count')/dataframe.groupby(['PRODUCTGROEP'])['PRODUCTGROEP'].transform('count')
    dataframe['impact K'] = dataframe.groupby(['PRODUCTGROEP'])['impact kwaliteit'].transform('count')/dataframe.groupby(['PRODUCTGROEP'])['PRODUCTGROEP'].transform('count')
    dataframe['impact B'] = dataframe.groupby(['PRODUCTGROEP'])['impact budget'].transform('count')/dataframe.groupby(['PRODUCTGROEP'])['PRODUCTGROEP'].transform('count')
    dataframe['impact W'] = dataframe.groupby(['PRODUCTGROEP'])['impact woonbeleving'].transform('count')/dataframe.groupby(['PRODUCTGROEP'])['PRODUCTGROEP'].transform('count')
    
    impact = dataframe[['PRODUCTGROEP', 'impact O', 'impact CD', 'impact K', 'impact B', 'impact W']]
    impact = impact.groupby('PRODUCTGROEP')[['impact O', 'impact CD', 'impact K', 'impact B', 'impact W']].first()
    impact = impact.reset_index()
    
    productgroepen = pd.DataFrame({
    "PRODUCTGROEP": ['21. Buitenwanden', '22. Binnenwanden', '23. Vloeren', '24. Trappen en hellingen', '27. Daken', '28. Hoofddraag- constructie', 
                     '31. Buitenkozijnen, -ramen, -deuren en -puien.', '32. Binnenkozijnen en - deuren', '33. Luiken en vensters', 
                     '34. Balustrades en leuningen', '42. Binnenwand- afwerkingen', '43. Vloer- afwerkingen', '45 Plafonds', '48. Na-isolatie', 
                     '52. Riolering en HWA', '53. Warm- en koud water installaties', '56. Verwarming en koeling', '57. Lucht- behandeling', 
                     '61. Elektrische installaties', '64. Vaste gebouw- voorzieningen', '65. Beveiliging', '66. Lift', '73. Keuken', '74. Sanitair', 
                     '90.Terrein'],
    "impact O": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact CD": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact K": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact B": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact W": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
    
    for i, row in productgroepen.iterrows():
        if row['PRODUCTGROEP'] not in impact['PRODUCTGROEP'].values:
            impact = pd.concat([impact, row.to_frame().T], ignore_index=True)
    impact = impact.sort_values(by='PRODUCTGROEP', ascending=True)
    impact = impact.reset_index(drop=True)

    st.session_state.file = impact

st.markdown("**Budget**")
st.number_input("Vul het budget in voor het huidige project", value=None, placeholder="Typ een bedrag")

if uploaded_file is not None:
    st.page_link("pages/optimalisatie2.py", label="Naar optimalisatie")

# st.markdown("**Productgroepen**")
# st.markdown("Hierbij kan er aangegeven worden wat het aandeel van de productgroepen momenteel in het project is. Dit is uitgedrukt in percentages. ")
# st.number_input("Het aandeel van de productgroep 'Keuken' in dit project", value=0, min_value = 0, max_value = 100)
# st.number_input("Het aandeel van de productgroep 'Sanitair' in dit project", value=0, min_value = 0, max_value = 100)
# st.number_input("Het aandeel van de productgroep 'Na-isolatie' in dit project", value=0, min_value = 0, max_value = 100)

