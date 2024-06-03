#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pulp as pl
# from menu2 import menu


# In[ ]:


if "budget" not in st.session_state:
    st.session_state.budget = None
    
st.session_state._budget = st.session_state.budget

def set_budget():
    st.session_state.budget = st.session_state._budget
    
if "appartementen" not in st.session_state:
    st.session_state.appartementen = None
    
st.session_state._appartementen = st.session_state.appartementen

def set_appartementen():
    st.session_state.appartementen = st.session_state._appartementen


# In[ ]:


if "Buitenwanden" not in st.session_state:
    st.session_state.Buitenwanden = None
    
st.session_state._Buitenwanden = st.session_state.Buitenwanden

def set_Buitenwanden():
    st.session_state.Buitenwanden = st.session_state._Buitenwanden
    
if "Binnenwanden" not in st.session_state:
    st.session_state.Binnenwanden = None
    
st.session_state._Binnenwanden = st.session_state.Binnenwanden

def set_Binnenwanden():
    st.session_state.Binnenwanden = st.session_state._Binnenwanden
    
if "Vloeren" not in st.session_state:
    st.session_state.Vloeren = None
    
st.session_state._Vloeren = st.session_state.Vloeren

def set_Vloeren():
    st.session_state.Vloeren = st.session_state._Vloeren
    
if "Trappen_en_hellingen" not in st.session_state:
    st.session_state.Trappen_en_hellingen = None
    
st.session_state._Trappen_en_hellingen = st.session_state.Trappen_en_hellingen

def set_Trappen_en_hellingen():
    st.session_state.Trappen_en_hellingen = st.session_state._Trappen_en_hellingen
    
if "Daken" not in st.session_state:
    st.session_state.Daken = None
    
st.session_state._Daken = st.session_state.Daken

def set_Daken():
    st.session_state.Daken = st.session_state._Daken
    
if "Hoofddraagconstructie" not in st.session_state:
    st.session_state.Hoofddraagconstructie = None
    
st.session_state._Hoofddraagconstructie = st.session_state.Hoofddraagconstructie

def set_Hoofddraagconstructie():
    st.session_state.Hoofddraagconstructie = st.session_state._Hoofddraagconstructie
    
if "Buitenkozijnen" not in st.session_state:
    st.session_state.Buitenkozijnen = None
    
st.session_state._Buitenkozijnen = st.session_state.Buitenkozijnen

def set_Buitenkozijnen():
    st.session_state.Buitenkozijnen = st.session_state._Buitenkozijnen
    
if "Binnenkozijnen_en__deuren" not in st.session_state:
    st.session_state.Binnenkozijnen_en__deuren = None
    
st.session_state._Binnenkozijnen_en__deuren = st.session_state.Binnenkozijnen_en__deuren

def set_Binnenkozijnen_en__deuren():
    st.session_state.Binnenkozijnen_en__deuren = st.session_state._Binnenkozijnen_en__deuren
    
if "Luiken_en_vensters" not in st.session_state:
    st.session_state.Luiken_en_vensters = None
    
st.session_state._Luiken_en_vensters = st.session_state.Luiken_en_vensters

def set_Luiken_en_vensters():
    st.session_state.Luiken_en_vensters = st.session_state._Luiken_en_vensters
    
if "Balustrades_en_leuningen" not in st.session_state:
    st.session_state.Balustrades_en_leuningen = None
    
st.session_state._Balustrades_en_leuningen = st.session_state.Balustrades_en_leuningen

def set_Balustrades_en_leuningen():
    st.session_state.Balustrades_en_leuningen = st.session_state._Balustrades_en_leuningen
    
if "Binnenwandafwerkingen" not in st.session_state:
    st.session_state.Binnenwandafwerkingen = None
    
st.session_state._Binnenwandafwerkingen = st.session_state.Binnenwandafwerkingen

def set_Binnenwandafwerkingen():
    st.session_state.Binnenwandafwerkingen = st.session_state._Binnenwandafwerkingen
    
if "Vloerafwerkingen" not in st.session_state:
    st.session_state.Vloerafwerkingen = None
    
st.session_state._Vloerafwerkingen = st.session_state.Vloerafwerkingen

def set_Vloerafwerkingen():
    st.session_state.Vloerafwerkingen = st.session_state._Vloerafwerkingen
    
if "Plafonds" not in st.session_state:
    st.session_state.Plafonds = None
    
st.session_state._Plafonds = st.session_state.Plafonds

def set_Plafonds():
    st.session_state.Plafonds = st.session_state._Plafonds
    
if "Vaste_gebouwvoorziening" not in st.session_state:
    st.session_state.Vaste_gebouwvoorziening = None
    
st.session_state._Vaste_gebouwvoorziening = st.session_state.Vaste_gebouwvoorziening

def set_Vaste_gebouwvoorziening():
    st.session_state.Vaste_gebouwvoorziening = st.session_state._Vaste_gebouwvoorziening
    
if "Keuken" not in st.session_state:
    st.session_state.Keuken = None
    
st.session_state._Keuken = st.session_state.Keuken

def set_Keuken():
    st.session_state.Keuken = st.session_state._Keuken
    
if "Terreininrichting" not in st.session_state:
    st.session_state.Terreininrichting = None
    
st.session_state._Terreininrichting = st.session_state.Terreininrichting

def set_Terreininrichting():
    st.session_state.Terreininrichting = st.session_state._Terreininrichting


# In[ ]:


st.markdown("**Buitenwanden**")
st.number_input("Aantal m2 aan buitenwanden in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Buitenwanden', on_change=set_Buitenwanden)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Binnenwanden**")
st.number_input("Aantal m2 aan binnenwanden in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Binnenwanden', on_change=set_Binnenwanden)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Vloeren**")
st.number_input("Aantal m2 aan vloeren in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Vloeren', on_change=set_Vloeren)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Trappen en hellingen**")
st.number_input("Aantal stuks aan trappen en hellingen in het huidige project", value = None, placeholder = "vul het aantal stuks in", key='_Trappen_en_hellingen', on_change=set_Trappen_en_hellingen)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Daken**")
st.number_input("Aantal m2 aan daken in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Daken', on_change=set_Daken)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Hoofddroogconstructie**")
st.number_input("Aantal m2 aan hoofddraagconstructie in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Hoofddraagconstructie', on_change=set_Hoofddraagconstructie)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Buitenkozijnen, -ramen, -deuren en -puien**")
st.number_input("Aantal m aan buitenkozijnen, -ramen, -deuren en -puien in het huidige project", value = None, placeholder = "vul het aantal m in", key='_Buitenkozijnen', on_change=set_Buitenkozijnen)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Binnenkozijnen en -deuren**")
st.number_input("Aantal stuks aan binnenkozijnen en -deuren in het huidige project", value = None, placeholder = "vul het aantal stuks in", key='_Binnenkozijnen_en__deuren', on_change=set_Binnenkozijnen_en__deuren)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Luiken en vensters**")
st.number_input("Aantal stuks aan luiken en vensters in het huidige project", value = None, placeholder = "vul het aantal stuks in", key='_Luiken_en_vensters', on_change=set_Luiken_en_vensters)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Balustrades en leuningen**")
st.number_input("Aantal m aan balustrades en leuningen in het huidige project", value = None, placeholder = "vul het aantal m in", key='_Balustrades_en_leuningen', on_change=set_Balustrades_en_leuningen)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Binnenwandafwerkingen**")
st.number_input("Aantal m2 aan binnenwandafwerkingen in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Binnenwandafwerkingen', on_change=set_Binnenwandafwerkingen)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Vloerafwerkingen**")
st.number_input("Aantal m2 aan vloerafwerkingen in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Vloerafwerkingen', on_change=set_Vloerafwerkingen)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Plafonds**")
st.number_input("Aantal m2 aan plafonds in het huidige project", value = None, placeholder = "vul het aantal m2 in", key='_Plafonds', on_change=set_Plafonds)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Vaste gebouwvoorziening**")
st.number_input("Aantal stuks aan vaste gebouwvoorziening huidige project", value = None, placeholder = "vul het aantal stuks in", key='_Vaste_gebouwvoorziening', on_change=set_Vaste_gebouwvoorziening)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Keuken**")
st.number_input("Aantal stuks aan keuken in het huidige project", value = None, placeholder = "vul het aantal stuks in", key='_Keuken', on_change=set_Keuken)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")

st.markdown("**Terreininrichting**")
st.number_input("Aantal stuks aan terreininrichting in het huidige project", value = None, placeholder = "vul het aantal stuks in", key='_Terreininrichting', on_change=set_Terreininrichting)
st.toggle("Aanpassingen aan de hoeveelheid binnen de productgroep mogelijk")
        
st.markdown("**Budget**")
st.number_input("Vul het budget in voor het huidige project", value=None, placeholder="Typ een bedrag", key='_budget', on_change=set_budget)

st.markdown("**Aantal appartementen**")
st.number_input("Het aantal appartementen dat gebouwd worden in dit project", value=0, key='_appartementen', on_change=set_appartementen)

st.page_link("pages/optimalisatie3.py", label="Naar optimalisatie")

