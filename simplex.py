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
    
if 'list' not in st.session_state:
    st.session_state.list = None

st.session_state._list = st.session_state.list

def set_list():
    st.session_state.list = st.session_state._list


# In[ ]:


st.title("Eigen Haard")


# **input tab**

# In[ ]:


st.session_state.file = None 
st.markdown("**Afdeling**")
st.selectbox(
    "Welke afdeling? *", 
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
uploaded_file = st.file_uploader("Kies een bestand *", help='Upload hier het projectbestand, op basis van dit bestand wordt de optimalisatie uitgevoerd. ')
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

    def status(status_series):
        if (status_series == 'vervallen').all():
            return 'vervallen'
        elif (status_series == 'n.v.t.').all(): 
            return 'n.v.t.'
        elif status_series.isin(['vervallen', 'n.v.t.']).all():
            return 'vervallen of n.v.t.'
        elif (status_series == 'actueel').any():
            return 'actueel'
        else:
            return 'onbekend'

    df1 = dataframe[['status in ontwerp:', 'productgroep']]
    df2 = df1.groupby('productgroep')['status in ontwerp:'].apply(status).reset_index()

#     st.dataframe(df2)
    lijst = [df2.iloc[i, 0][:2] for i in range(len(df2)) if df2.iloc[i, 1] == 'actueel']
    st.session_state.list = lijst

    st.dataframe(dataframe, hide_index = True)
    st.session_state.dataframe = dataframe


# In[ ]:


if st.button("clear all"):
    st.session_state.clear()
    st.experimental_rerun()  # Rerun the app to refresh the page

if uploaded_file is not None:
    st.page_link("pages/input.py", label="Naar input")


# In[ ]:


# with tab2:
#     data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
#     data['optimalisatie'] = data.apply(lambda row: 'nee' if row.isnull().any() else 'ja', axis=1)
#     data.iloc[-1, 3] = data.iloc[-1, 3] + 1
    
#     data['minimaal'] = data['minimaal'] * st.session_state.appartementen
#     data['maximaal'] = data['maximaal'] * st.session_state.appartementen
#     data['constant'] = ['']*len(data)
    
#     st.markdown("##### Verdeling productgroepen")
#     filtered = data.dropna(subset=['minimaal', 'maximaal'])

#     opties = st.selectbox("Soort visualisatie", 
#                              ["Alleen de productgroepen met m2 als eenheid", 
#                               "Alleen de productgroepen met stuks als eenheid", "Alle productgroepen"], index = None, 
#                           placeholder = 'Kies een visualisatie')

#     if opties == "Alleen de productgroepen met m2 als eenheid":
#         filtered = filtered[filtered['eenheid'] == 'm2']
#     if opties == "Alleen de productgroepen met stuks als eenheid":
#         filtered = filtered[filtered['eenheid'] == 'stuks']

#     productgroepen = filtered['productgroep'].unique()
#     selected_productgroepen = st.multiselect("Selecteer een productgroep", productgroepen, 
#                                              placeholder = 'Selecteer productgroep(en)')
#     filtered_data = filtered[filtered['productgroep'].isin(selected_productgroepen)]

#     result_kosten = filtered_data[['productgroep', 'kosten']]
#     result_kosten = result_kosten.transpose()
#     result_kosten.columns = result_kosten.iloc[0]
#     result_kosten = result_kosten[1:]
#     result_kosten.insert(0, 'minimaal', min(filtered['kosten']))
#     result_kosten.insert(1, 'maximaal', max(filtered['kosten']))
#     result_kosten.insert(2, 'code', '01')
#     result_kosten['Kosten per eenheid'] = result_kosten['maximaal'] - result_kosten['minimaal']

#     # Voorbeeld lijst met kleuren
#     kleuren_schema = [
#         'rgba(212, 0, 60, 1.0)',
#         'rgba(241, 142, 47, 1.0)', 
#         'rgba(255, 211, 0, 1.0)',
#         'rgba(0, 158, 224, 1.0)', 
#         'rgba(151, 191, 13, 1.0)', 
#         'rgba(147, 16, 126, 1.0)',  
#         'rgba(119, 118, 121, 1.0)']

#     fig_kosten = px.bar(result_kosten, x='Kosten per eenheid', y = 'code', base = 'minimaal', 
#                         color_discrete_sequence=['rgba(119, 118, 121, 0.1)'])

#     kleur_teller = 0
#     # fig_kosten.update_traces(marker_size=20)
#     for i in range(len(selected_productgroepen)):
#         if result_kosten.columns[i+3] in selected_productgroepen:
#             kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
#             kleur_teller += 1
#             fig_kosten.add_trace(px.scatter(result_kosten, x=result_kosten.columns[i+3], y='code', 
#                                          color_discrete_sequence=[kleur], labels={'x': ''}, 
#                                          size=[10], symbol = [result_kosten.columns[i+3]]).data[0])

#     fig_kosten.update_yaxes(visible=False)

#     fig_kosten.update_layout(
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="right",
#             x=1))

#     fig_kosten.update_layout(height=250)

#     st.plotly_chart(fig_kosten)
    

#     result_milieukosten = filtered_data[['productgroep', 'circulair']]
#     result_milieukosten = result_milieukosten.transpose()
#     result_milieukosten.columns = result_milieukosten.iloc[0]
#     result_milieukosten = result_milieukosten[1:]
#     result_milieukosten.insert(0, 'minimaal', min(filtered['circulair']))
#     result_milieukosten.insert(1, 'maximaal', max(filtered['circulair']))
#     result_milieukosten.insert(2, 'code', '02')
#     result_milieukosten['Milieukosten per eenheid'] = result_milieukosten['maximaal'] - result_milieukosten['minimaal']

#     # Voorbeeld lijst met kleuren
#     kleuren_schema = [
#         'rgba(212, 0, 60, 1.0)',
#         'rgba(241, 142, 47, 1.0)', 
#         'rgba(255, 211, 0, 1.0)',
#         'rgba(0, 158, 224, 1.0)', 
#         'rgba(151, 191, 13, 1.0)', 
#         'rgba(147, 16, 126, 1.0)',  
#         'rgba(119, 118, 121, 1.0)']

#     fig_circulair = px.bar(result_milieukosten, x='Milieukosten per eenheid', y = 'code', base = 'minimaal', 
#                         color_discrete_sequence=['rgba(119, 118, 121, 0.1)'])

#     kleur_teller = 0
#     # fig_kosten.update_traces(marker_size=20)
#     for i in range(len(selected_productgroepen)):
#         if result_milieukosten.columns[i+3] in selected_productgroepen:
#             kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
#             kleur_teller += 1
#             fig_circulair.add_trace(px.scatter(result_milieukosten, x=result_milieukosten.columns[i+3], y='code', 
#                                          color_discrete_sequence=[kleur], labels={'x': ''}, 
#                                          size=[10], symbol = [result_milieukosten.columns[i+3]]).data[0])

#     fig_circulair.update_yaxes(visible=False)

#     fig_circulair.update_layout(
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="right",
#             x=1))

#     fig_circulair.update_layout(height=250)

#     st.plotly_chart(fig_circulair)


# In[ ]:




