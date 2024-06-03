#!/usr/bin/env python
# coding: utf-8

# https://discuss.streamlit.io/t/how-to-use-session-state-to-save-file-uploads-and-filters/36443

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pulp as pl
from io import BytesIO
# from menu2 import menu


# In[ ]:


if "projectbestand" not in st.session_state:
    st.session_state.projectbestand = None
    
st.session_state._projectbestand = st.session_state.projectbestand

def set_projectbestand():
    st.session_state.projectbestand = st.session_state._projectbestand

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None
    
st.session_state._dataframe = st.session_state.dataframe

def set_dataframe():
    st.session_state.dataframe = st.session_state._dataframe
    
if 'file' not in st.session_state:
    st.session_state.file = None

st.session_state._file = st.session_state.file

def set_file():
    st.session_state.file = st.session_state._file
    
if 'file2' not in st.session_state:
    st.session_state.file2 = None

st.session_state._file2 = st.session_state.file2

def set_file2():
    st.session_state.file2 = st.session_state._file2

if 'afdeling' not in st.session_state:
    st.session_state.afdeling = None

st.session_state._afdeling = st.session_state.afdeling

def set_afdeling():
    st.session_state.afdeling = st.session_state._afdeling
    
if 'name' not in st.session_state:
    st.session_state.name = None

st.session_state._name = st.session_state.name

def set_name():
    st.session_state.name = st.session_state._name


# In[ ]:


st.title("Eigen Haard")


# **input tab**

# In[ ]:


st.session_state.file = None 
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
    st.session_state.name = uploaded_file.name
    dataframe = pd.read_csv(uploaded_file)
    
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
        
    if st.session_state.afdeling in ['Nieuwbouw realisatie', 'Renovatie realisatie', 'Planmatig onderhoud realisatie']:
        dataframe = dataframe.drop(dataframe.columns[[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 29]], axis = 1)
        dataframe.rename(columns={dataframe.columns[12]: "impact onderhoud"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[13]: "impact circulair"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[14]: "impact kwaliteit"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[15]: "impact budget"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[16]: "impact woonbeleving"}, inplace=True)
        
        dataframe = dataframe.dropna(how='all')
        dataframe = dataframe.drop(0)
        dataframe = dataframe.reset_index(drop=True)

    if st.session_state.afdeling in ['Mutatie onderhoud', 'Dagelijks onderhoud']:
        dataframe = dataframe.drop(dataframe.columns[[1, 3, 5, 7, 9, 11, 13, 15, 17]], axis = 1)
        dataframe = dataframe

    st.markdown("dataframe") 
    st.dataframe(dataframe, hide_index = True)
    st.session_state.dataframe = dataframe
    
    dataframe_plus = dataframe[dataframe["norm / \n'+' optie"] == " '+' optie"]
#     st.markdown("Dataframe met alleen plus opties:")
#     st.dataframe(dataframe_plus)

#     st.markdown(dataframe['impact circulair'].value_counts()['CD'])
    
    impact = dataframe.copy()
    impact2 = dataframe.copy()
    
    impact2['impact O'] = impact2.groupby(['productgroep'])['impact onderhoud'].transform('count')/impact2.groupby(['productgroep'])['productgroep'].transform('count')
    impact2['impact CD'] = impact2.groupby(['productgroep'])['impact circulair'].transform('count')/impact2.groupby(['productgroep'])['productgroep'].transform('count')
    impact2['impact K'] = impact2.groupby(['productgroep'])['impact kwaliteit'].transform('count')/impact2.groupby(['productgroep'])['productgroep'].transform('count')
    impact2['impact B'] = impact2.groupby(['productgroep'])['impact budget'].transform('count')/impact2.groupby(['productgroep'])['productgroep'].transform('count')
    impact2['impact W'] = impact2.groupby(['productgroep'])['impact woonbeleving'].transform('count')/impact2.groupby(['productgroep'])['productgroep'].transform('count')
    
    if 'O' in impact['impact onderhoud'].value_counts().index:
         impact['impact O'] = impact.groupby(['productgroep'])['impact onderhoud'].transform('count')/impact['impact onderhoud'].value_counts()['O']
    else:
        impact['impact O'] = 0
        
    if 'CD' in impact['impact circulair'].value_counts().index:
         impact['impact CD'] = impact.groupby(['productgroep'])['impact circulair'].transform('count')/impact['impact circulair'].value_counts()['CD']
    else:
        impact['impact CD'] = 0
    
    if 'K' in impact['impact kwaliteit'].value_counts().index:
         impact['impact K'] = impact.groupby(['productgroep'])['impact kwaliteit'].transform('count')/impact['impact kwaliteit'].value_counts()['K']
    else:
        impact['impact K'] = 0
        
    if 'B' in impact['impact budget'].value_counts().index:
         impact['impact B'] = impact.groupby(['productgroep'])['impact budget'].transform('count')/impact['impact budget'].value_counts()['B']
    else:
        impact['impact B'] = 0
        
    if 'W' in impact['impact woonbeleving'].value_counts().index:
         impact['impact W'] = impact.groupby(['productgroep'])['impact woonbeleving'].transform('count')/impact['impact woonbeleving'].value_counts()['W']
    else:
        impact['impact W'] = 0
    
    impact = impact[['productgroep', 'impact O', 'impact CD', 'impact K', 'impact B', 'impact W']]
    impact = impact.groupby('productgroep')[['impact O', 'impact CD', 'impact K', 'impact B', 'impact W']].first()
    impact = impact.reset_index()
    
    impact2 = impact2[['productgroep', 'impact O', 'impact CD', 'impact K', 'impact B', 'impact W']]
    impact2 = impact2.groupby('productgroep')[['impact O', 'impact CD', 'impact K', 'impact B', 'impact W']].first()
    impact2 = impact2.reset_index()
        
    productgroepen = pd.DataFrame({
    "productgroep": ['21. Buitenwanden', '22. Binnenwanden', '23. Vloeren', '24. Trappen en hellingen', '27. Daken', '28. Hoofddraag- constructie', 
                     '31. Buitenkozijnen, -ramen, -deuren en -puien.', '32. Binnenkozijnen en - deuren', '33. Luiken en vensters', 
                     '34. Balustrades en leuningen', '42. Binnenwand- afwerkingen', '43. Vloer- afwerkingen', '45 Plafonds', '48. Na-isolatie', 
                     '52. Riolering en HWA', '53. Warm- en koud water installaties', '56. Verwarming en koeling', '57. Lucht- behandeling', 
                     '61. Elektrische installaties', '64. Vaste gebouw- voorzieningen', '65. Beveiliging', '66. Liften', '73. Keuken', '74. Sanitair', 
                     '90.Terrein'],
    "impact O": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact CD": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact K": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact B": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "impact W": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
    
    for i, row in productgroepen.iterrows():
        if row['productgroep'] not in impact['productgroep'].values:
            impact = pd.concat([impact, row.to_frame().T], ignore_index=True)
    impact = impact.sort_values(by='productgroep', ascending=True)
    impact = impact.reset_index(drop=True)
    
    
    for i, row in productgroepen.iterrows():
        if row['productgroep'] not in impact['productgroep'].values:
            impact2 = pd.concat([impact, row.to_frame().T], ignore_index=True)
    impact2 = impact2.sort_values(by='productgroep', ascending=True)
    impact2 = impact2.reset_index(drop=True)
    
    st.session_state.file = impact
    st.session_state.file2 = impact2


# st.markdown("**Productgroepen**")
# st.markdown("Hierbij kan er aangegeven worden wat het aandeel van de productgroepen momenteel in het project is. Dit is uitgedrukt in percentages. ")
# st.number_input("Het aandeel van de productgroep 'Keuken' in dit project", value=0, min_value = 0, max_value = 100)
# st.number_input("Het aandeel van de productgroep 'Sanitair' in dit project", value=0, min_value = 0, max_value = 100)
# st.number_input("Het aandeel van de productgroep 'Na-isolatie' in dit project", value=0, min_value = 0, max_value = 100)


# In[ ]:


buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    dataframe.to_excel(writer, index=False)

# De buffer naar het begin van het bestand terugzetten
buffer.seek(0)

# Download button voor Excel-bestand
st.download_button(
    label="Download data as Excel",
    data=buffer,
    file_name="test.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# In[ ]:


if uploaded_file is not None:
    st.page_link("pages/input.py", label="Naar input")

