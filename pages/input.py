#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pulp as pl


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

if "Buitenwanden_on" not in st.session_state:
    st.session_state.Buitenwanden_on = 0
    
st.session_state._Buitenwanden_on = st.session_state.Buitenwanden_on

def set_Buitenwanden_on():
    st.session_state.Buitenwanden_on = st.session_state._Buitenwanden_on
    
if "Binnenwanden" not in st.session_state:
    st.session_state.Binnenwanden = None
    
st.session_state._Binnenwanden = st.session_state.Binnenwanden

def set_Binnenwanden():
    st.session_state.Binnenwanden = st.session_state._Binnenwanden

if "Binnenwanden_on" not in st.session_state:
    st.session_state.Binnenwanden_on = 0
    
st.session_state._Binnenwanden_on = st.session_state.Binnenwanden_on

def set_Binnenwanden_on():
    st.session_state.Binnenwanden_on = st.session_state._Binnenwanden_on
    
if "Vloeren" not in st.session_state:
    st.session_state.Vloeren = None
    
st.session_state._Vloeren = st.session_state.Vloeren

def set_Vloeren():
    st.session_state.Vloeren = st.session_state._Vloeren
    
if "Vloeren_on" not in st.session_state:
    st.session_state.Vloeren_on = 0
    
st.session_state._Vloeren_on = st.session_state.Vloeren_on

def set_Vloeren_on():
    st.session_state.Vloeren_on = st.session_state._Vloeren_on
    
if "Trappen_en_hellingen" not in st.session_state:
    st.session_state.Trappen_en_hellingen = None
    
st.session_state._Trappen_en_hellingen = st.session_state.Trappen_en_hellingen

def set_Trappen_en_hellingen():
    st.session_state.Trappen_en_hellingen = st.session_state._Trappen_en_hellingen
    
if "Trappen_en_hellingen_on" not in st.session_state:
    st.session_state.Trappen_en_hellingen_on = 0
    
st.session_state._Trappen_en_hellingen_on = st.session_state.Trappen_en_hellingen_on

def set_Trappen_en_hellingen_on():
    st.session_state.Trappen_en_hellingen_on = st.session_state._Trappen_en_hellingen_on
    
if "Daken" not in st.session_state:
    st.session_state.Daken = None
    
st.session_state._Daken = st.session_state.Daken

def set_Daken():
    st.session_state.Daken = st.session_state._Daken
    
if "Daken_on" not in st.session_state:
    st.session_state.Daken_on = 0
    
st.session_state._Daken_on = st.session_state.Daken_on

def set_Daken_on():
    st.session_state.Daken_on = st.session_state._Daken_on
    
if "Hoofddraagconstructie" not in st.session_state:
    st.session_state.Hoofddraagconstructie = None
    
st.session_state._Hoofddraagconstructie = st.session_state.Hoofddraagconstructie

def set_Hoofddraagconstructie():
    st.session_state.Hoofddraagconstructie = st.session_state._Hoofddraagconstructie
    
if "Hoofddraagconstructie_on" not in st.session_state:
    st.session_state.Hoofddraagconstructie_on = 0
    
st.session_state._Hoofddraagconstructie_on = st.session_state.Hoofddraagconstructie_on

def set_Hoofddraagconstructie_on():
    st.session_state.Hoofddraagconstructie_on = st.session_state._Hoofddraagconstructie_on    

if "Buitenkozijnen" not in st.session_state:
    st.session_state.Buitenkozijnen = None
    
st.session_state._Buitenkozijnen = st.session_state.Buitenkozijnen

def set_Buitenkozijnen():
    st.session_state.Buitenkozijnen = st.session_state._Buitenkozijnen
    
if "Buitenkozijnen_on" not in st.session_state:
    st.session_state.Buitenkozijnen_on = 0
    
st.session_state._Buitenkozijnen_on = st.session_state.Buitenkozijnen_on

def set_Buitenkozijnen_on():
    st.session_state.Buitenkozijnen_on = st.session_state._Buitenkozijnen_on
    
if "Binnenkozijnen_en__deuren" not in st.session_state:
    st.session_state.Binnenkozijnen_en__deuren = None
    
st.session_state._Binnenkozijnen_en__deuren = st.session_state.Binnenkozijnen_en__deuren

def set_Binnenkozijnen_en__deuren():
    st.session_state.Binnenkozijnen_en__deuren = st.session_state._Binnenkozijnen_en__deuren
    
if "Binnenkozijnen_en__deuren_on" not in st.session_state:
    st.session_state.Binnenkozijnen_en__deuren_on = 0
    
st.session_state._Binnenkozijnen_en__deuren_on = st.session_state.Binnenkozijnen_en__deuren_on

def set_Binnenkozijnen_en__deuren_on():
    st.session_state.Binnenkozijnen_en__deuren_on = st.session_state._Binnenkozijnen_en__deuren_on
    
if "Luiken_en_vensters" not in st.session_state:
    st.session_state.Luiken_en_vensters = None
    
st.session_state._Luiken_en_vensters = st.session_state.Luiken_en_vensters

def set_Luiken_en_vensters():
    st.session_state.Luiken_en_vensters = st.session_state._Luiken_en_vensters
    
if "Luiken_en_vensters_on" not in st.session_state:
    st.session_state.Luiken_en_vensters_on = 0
    
st.session_state._Luiken_en_vensters_on = st.session_state.Luiken_en_vensters_on

def set_Luiken_en_vensters_on():
    st.session_state.Luiken_en_vensters_on = st.session_state._Luiken_en_vensters_on
    
if "Balustrades_en_leuningen" not in st.session_state:
    st.session_state.Balustrades_en_leuningen = None
    
st.session_state._Balustrades_en_leuningen = st.session_state.Balustrades_en_leuningen

def set_Balustrades_en_leuningen():
    st.session_state.Balustrades_en_leuningen = st.session_state._Balustrades_en_leuningen
    
if "Balustrades_en_leuningen_on" not in st.session_state:
    st.session_state.Balustrades_en_leuningen_on = 0
    
st.session_state._Balustrades_en_leuningen_on = st.session_state.Balustrades_en_leuningen_on

def set_Balustrades_en_leuningen_on():
    st.session_state.Balustrades_en_leuningen_on = st.session_state._Balustrades_en_leuningen_on
    
if "Binnenwandafwerkingen" not in st.session_state:
    st.session_state.Binnenwandafwerkingen = None
    
st.session_state._Binnenwandafwerkingen = st.session_state.Binnenwandafwerkingen

def set_Binnenwandafwerkingen():
    st.session_state.Binnenwandafwerkingen = st.session_state._Binnenwandafwerkingen
    
if "Binnenwandafwerkingen_on" not in st.session_state:
    st.session_state.Binnenwandafwerkingen_on = 0
    
st.session_state._Binnenwandafwerkingen_on = st.session_state.Binnenwandafwerkingen_on

def set_Binnenwandafwerkingen_on():
    st.session_state.Binnenwandafwerkingen_on = st.session_state._Binnenwandafwerkingen_on
    
if "Vloerafwerkingen" not in st.session_state:
    st.session_state.Vloerafwerkingen = None
    
st.session_state._Vloerafwerkingen = st.session_state.Vloerafwerkingen

def set_Vloerafwerkingen():
    st.session_state.Vloerafwerkingen = st.session_state._Vloerafwerkingen
    
if "Vloerafwerkingen_on" not in st.session_state:
    st.session_state.Vloerafwerkingen_on = 0
    
st.session_state._Vloerafwerkingen_on = st.session_state.Vloerafwerkingen_on

def set_Vloerafwerkingen_on():
    st.session_state.Vloerafwerkingen_on = st.session_state._Vloerafwerkingen_on
    
if "Plafonds" not in st.session_state:
    st.session_state.Plafonds = None
    
st.session_state._Plafonds = st.session_state.Plafonds

def set_Plafonds():
    st.session_state.Plafonds = st.session_state._Plafonds
    
if "Plafonds_on" not in st.session_state:
    st.session_state.Plafonds_on = 0
    
st.session_state._Plafonds_on = st.session_state.Plafonds_on

def set_Plafonds_on():
    st.session_state.Plafonds_on = st.session_state._Plafonds_on
    
if "Vaste_gebouwvoorziening" not in st.session_state:
    st.session_state.Vaste_gebouwvoorziening = None
    
st.session_state._Vaste_gebouwvoorziening = st.session_state.Vaste_gebouwvoorziening

def set_Vaste_gebouwvoorziening():
    st.session_state.Vaste_gebouwvoorziening = st.session_state._Vaste_gebouwvoorziening
    
if "Vaste_gebouwvoorziening_on" not in st.session_state:
    st.session_state.Vaste_gebouwvoorziening_on = 0
    
st.session_state._Vaste_gebouwvoorziening_on = st.session_state.Vaste_gebouwvoorziening_on

def set_Vaste_gebouwvoorziening_on():
    st.session_state.Vaste_gebouwvoorziening_on = st.session_state._Vaste_gebouwvoorziening_on
    
if "Keuken" not in st.session_state:
    st.session_state.Keuken = None
    
st.session_state._Keuken = st.session_state.Keuken

def set_Keuken():
    st.session_state.Keuken = st.session_state._Keuken
    
if "Keuken_on" not in st.session_state:
    st.session_state.Keuken_on = 0
    
st.session_state._Keuken_on = st.session_state.Keuken_on

def set_Keuken_on():
    st.session_state.Keuken_on = st.session_state._Keuken_on
    
if "Terreininrichting" not in st.session_state:
    st.session_state.Terreininrichting = None
    
st.session_state._Terreininrichting = st.session_state.Terreininrichting

def set_Terreininrichting():
    st.session_state.Terreininrichting = st.session_state._Terreininrichting
    
if "Terreininrichting_on" not in st.session_state:
    st.session_state.Terreininrichting_on = 0
    
st.session_state._Terreininrichting_on = st.session_state.Terreininrichting_on

def set_Terreininrichting_on():
    st.session_state.Terreininrichting_on = st.session_state._Terreininrichting_on


# In[ ]:


st.title("Productgroepen")


# In[ ]:


st.markdown("**21 Buitenwanden**")
st.number_input("Aantal m2 aan buitenwanden in het huidige project", value = None, 
                placeholder = "vul het aantal m2 in", key='_Buitenwanden', on_change=set_Buitenwanden)
st.toggle("Aanpassingen aan de hoeveelheid binnen buitenwanden mogelijk", key='_Buitenwanden_on', on_change=set_Buitenwanden_on)

st.markdown("**22 Binnenwanden**")
st.number_input("Aantal m2 aan binnenwanden in het huidige project", value = None, placeholder = "vul het aantal m2 in", 
                key='_Binnenwanden', on_change=set_Binnenwanden)
st.toggle("Aanpassingen aan de hoeveelheid binnen binnenwanden mogelijk", key='_Binnenwanden_on', on_change=set_Binnenwanden_on)

st.markdown("**23 Vloeren**")
st.number_input("Aantal m2 aan vloeren in het huidige project", value = None, placeholder = "vul het aantal m2 in", 
                key='_Vloeren', on_change=set_Vloeren)
st.toggle("Aanpassingen aan de hoeveelheid binnen vloeren mogelijk", key='_Vloeren_on', on_change=set_Vloeren_on)

st.markdown("**24 Trappen en hellingen**")
st.number_input("Aantal stuks aan trappen en hellingen in het huidige project", value = None, 
                placeholder = "vul het aantal stuks in", key='_Trappen_en_hellingen', on_change=set_Trappen_en_hellingen)
st.toggle("Aanpassingen aan de hoeveelheid binnen trappen en hellingen mogelijk", key='_Trappen_en_hellingen_on', 
          on_change=set_Trappen_en_hellingen_on)

st.markdown("**27 Daken**")
st.number_input("Aantal m2 aan daken in het huidige project", value = None, placeholder = "vul het aantal m2 in", 
                key='_Daken', on_change=set_Daken)
st.toggle("Aanpassingen aan de hoeveelheid binnen daken mogelijk", key='_Daken_on', on_change=set_Daken_on)

st.markdown("**28 Hoofddraagconstructie**")
st.number_input("Aantal m2 aan hoofddraagconstructie in het huidige project", value = None, 
                placeholder = "vul het aantal m2 in", key='_Hoofddraagconstructie', on_change=set_Hoofddraagconstructie)
st.toggle("Aanpassingen aan de hoeveelheid binnen hoofddraagconstructie mogelijk", key='_Hoofddraagconstructie_on', 
          on_change=set_Hoofddraagconstructie_on)

st.markdown("**31 Buitenkozijnen, -ramen, -deuren en -puien**")
st.number_input("Aantal m aan buitenkozijnen, -ramen, -deuren en -puien in het huidige project", value = None, 
                placeholder = "vul het aantal m in", key='_Buitenkozijnen', on_change=set_Buitenkozijnen)
st.toggle("Aanpassingen aan de hoeveelheid binnen buitenkozijnen, -ramen, -deuren en -puien mogelijk", 
          key='_Buitenkozijnen_on', on_change=set_Buitenkozijnen_on)

st.markdown("**32 Binnenkozijnen en -deuren**")
st.number_input("Aantal stuks aan binnenkozijnen en -deuren in het huidige project", value = None, 
                placeholder = "vul het aantal stuks in", key='_Binnenkozijnen_en__deuren', 
                on_change=set_Binnenkozijnen_en__deuren)
st.toggle("Aanpassingen aan de hoeveelheid binnen binnenkozijnen en -deuren mogelijk", key='_Binnenkozijnen_en__deuren_on', 
          on_change=set_Binnenkozijnen_en__deuren_on)

st.markdown("**33 Luiken en vensters**")
st.number_input("Aantal stuks aan luiken en vensters in het huidige project", value = None, 
                placeholder = "vul het aantal stuks in", key='_Luiken_en_vensters', on_change=set_Luiken_en_vensters)
st.toggle("Aanpassingen aan de hoeveelheid binnen luiken en vensters mogelijk", key='_Luiken_en_vensters_on', 
          on_change=set_Luiken_en_vensters_on)

st.markdown("**34 Balustrades en leuningen**")
st.number_input("Aantal m aan balustrades en leuningen in het huidige project", value = None, 
                placeholder = "vul het aantal m in", key='_Balustrades_en_leuningen', on_change=set_Balustrades_en_leuningen)
st.toggle("Aanpassingen aan de hoeveelheid binnen balustrades en leuningen mogelijk", key='_Balustrades_en_leuningen_on', 
          on_change=set_Balustrades_en_leuningen_on)

st.markdown("**42 Binnenwandafwerkingen**")
st.number_input("Aantal m2 aan binnenwandafwerkingen in het huidige project", value = None, 
                placeholder = "vul het aantal m2 in", key='_Binnenwandafwerkingen', on_change=set_Binnenwandafwerkingen)
st.toggle("Aanpassingen aan de hoeveelheid binnen binnenwandafwerkingen mogelijk", key='_Binnenwandafwerkingen_on', 
          on_change=set_Binnenwandafwerkingen_on)

st.markdown("**43 Vloerafwerkingen**")
st.number_input("Aantal m2 aan vloerafwerkingen in het huidige project", value = None, placeholder = "vul het aantal m2 in", 
                key='_Vloerafwerkingen', on_change=set_Vloerafwerkingen)
st.toggle("Aanpassingen aan de hoeveelheid binnen vloerafwerkingen mogelijk", key='_Vloerafwerkingen_on', 
          on_change=set_Vloerafwerkingen_on)

st.markdown("**45 Plafonds**")
st.number_input("Aantal m2 aan plafonds in het huidige project", value = None, placeholder = "vul het aantal m2 in", 
                key='_Plafonds', on_change=set_Plafonds)
st.toggle("Aanpassingen aan de hoeveelheid binnen plafonds mogelijk", key='_Plafonds_on', on_change=set_Plafonds_on)

st.markdown("**64 Vaste gebouwvoorziening**")
st.number_input("Aantal stuks aan vaste gebouwvoorziening huidige project", value = None, 
                placeholder = "vul het aantal stuks in", key='_Vaste_gebouwvoorziening', on_change=set_Vaste_gebouwvoorziening)
st.toggle("Aanpassingen aan de hoeveelheid binnen vaste gebouwvoorziening mogelijk", key='_Vaste_gebouwvoorziening_on', 
          on_change=set_Vaste_gebouwvoorziening_on)

st.markdown("**73 Keuken**")
st.number_input("Aantal stuks aan keuken in het huidige project", value = None, placeholder = "vul het aantal stuks in", 
                key='_Keuken', on_change=set_Keuken)
st.toggle("Aanpassingen aan de hoeveelheid binnen keuken mogelijk", key='_Keuken_on', on_change=set_Keuken_on)

st.markdown("**90 Terreininrichting**")
st.number_input("Aantal stuks aan terreininrichting in het huidige project", value = None, 
                placeholder = "vul het aantal stuks in", key='_Terreininrichting', on_change=set_Terreininrichting)
st.toggle("Aanpassingen aan de hoeveelheid binnen terreininrichting mogelijk", key='_Terreininrichting_on', 
          on_change=set_Terreininrichting_on)
        
st.markdown("**Budget**")
st.number_input("Vul het budget in voor het huidige project", value=None, placeholder="Typ een bedrag", 
                key='_budget', on_change=set_budget)

st.markdown("**Aantal appartementen**")
st.number_input("Het aantal appartementen dat gebouwd worden in dit project", value=0, key='_appartementen', 
                on_change=set_appartementen)
col1, col2 = st.columns([2, 8])
with col1:
    st.toggle("")
with col2:
    st.markdown("test")

keys = ['Buitenwanden', 'Binnenwanden', 'Vloeren', 'Trappen_en_hellingen', 'Daken', 'Hoofddraagconstructie', 'Buitenkozijnen', 
 'Binnenkozijnen_en__deuren', 'Luiken_en_vensters', 'Balustrades_en_leuningen', 'Binnenwandafwerkingen', 'Vloerafwerkingen', 
 'Plafonds', 'Vaste_gebouwvoorziening', 'Keuken', 'Terreininrichting', 'budget', 'appartementen']

st.page_link("simplex.py", label = 'Homepagina')

if all(st.session_state[key] is not None for key in keys): 
    st.page_link("pages/optimalisatie3.py", label="Naar optimalisatie")

