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


# if st.button("clear all"):
#     st.session_state.clear()
#     st.experimental_rerun()  # Rerun the app to refresh the page

if uploaded_file is not None:
    st.page_link("pages/input.py", label="Naar input")

