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
    st.session_state.Buitenwanden_on = 1
    
st.session_state._Buitenwanden_on = st.session_state.Buitenwanden_on

def set_Buitenwanden_on():
    st.session_state.Buitenwanden_on = st.session_state._Buitenwanden_on
    
if "Binnenwanden" not in st.session_state:
    st.session_state.Binnenwanden = None
    
st.session_state._Binnenwanden = st.session_state.Binnenwanden

def set_Binnenwanden():
    st.session_state.Binnenwanden = st.session_state._Binnenwanden

if "Binnenwanden_on" not in st.session_state:
    st.session_state.Binnenwanden_on = 1
    
st.session_state._Binnenwanden_on = st.session_state.Binnenwanden_on

def set_Binnenwanden_on():
    st.session_state.Binnenwanden_on = st.session_state._Binnenwanden_on
    
if "Vloeren" not in st.session_state:
    st.session_state.Vloeren = None
    
st.session_state._Vloeren = st.session_state.Vloeren

def set_Vloeren():
    st.session_state.Vloeren = st.session_state._Vloeren
    
if "Vloeren_on" not in st.session_state:
    st.session_state.Vloeren_on = 1
    
st.session_state._Vloeren_on = st.session_state.Vloeren_on

def set_Vloeren_on():
    st.session_state.Vloeren_on = st.session_state._Vloeren_on
    
if "Trappen_en_hellingen" not in st.session_state:
    st.session_state.Trappen_en_hellingen = None
    
st.session_state._Trappen_en_hellingen = st.session_state.Trappen_en_hellingen

def set_Trappen_en_hellingen():
    st.session_state.Trappen_en_hellingen = st.session_state._Trappen_en_hellingen
    
if "Trappen_en_hellingen_on" not in st.session_state:
    st.session_state.Trappen_en_hellingen_on = 1
    
st.session_state._Trappen_en_hellingen_on = st.session_state.Trappen_en_hellingen_on

def set_Trappen_en_hellingen_on():
    st.session_state.Trappen_en_hellingen_on = st.session_state._Trappen_en_hellingen_on
    
if "Daken" not in st.session_state:
    st.session_state.Daken = None
    
st.session_state._Daken = st.session_state.Daken

def set_Daken():
    st.session_state.Daken = st.session_state._Daken
    
if "Daken_on" not in st.session_state:
    st.session_state.Daken_on = 1
    
st.session_state._Daken_on = st.session_state.Daken_on

def set_Daken_on():
    st.session_state.Daken_on = st.session_state._Daken_on
    
if "Hoofddraagconstructie" not in st.session_state:
    st.session_state.Hoofddraagconstructie = None
    
st.session_state._Hoofddraagconstructie = st.session_state.Hoofddraagconstructie

def set_Hoofddraagconstructie():
    st.session_state.Hoofddraagconstructie = st.session_state._Hoofddraagconstructie
    
if "Hoofddraagconstructie_on" not in st.session_state:
    st.session_state.Hoofddraagconstructie_on = 1
    
st.session_state._Hoofddraagconstructie_on = st.session_state.Hoofddraagconstructie_on

def set_Hoofddraagconstructie_on():
    st.session_state.Hoofddraagconstructie_on = st.session_state._Hoofddraagconstructie_on    

if "Buitenkozijnen" not in st.session_state:
    st.session_state.Buitenkozijnen = None
    
st.session_state._Buitenkozijnen = st.session_state.Buitenkozijnen

def set_Buitenkozijnen():
    st.session_state.Buitenkozijnen = st.session_state._Buitenkozijnen
    
if "Buitenkozijnen_on" not in st.session_state:
    st.session_state.Buitenkozijnen_on = 1
    
st.session_state._Buitenkozijnen_on = st.session_state.Buitenkozijnen_on

def set_Buitenkozijnen_on():
    st.session_state.Buitenkozijnen_on = st.session_state._Buitenkozijnen_on
    
if "Binnenkozijnen_en__deuren" not in st.session_state:
    st.session_state.Binnenkozijnen_en__deuren = None
    
st.session_state._Binnenkozijnen_en__deuren = st.session_state.Binnenkozijnen_en__deuren

def set_Binnenkozijnen_en__deuren():
    st.session_state.Binnenkozijnen_en__deuren = st.session_state._Binnenkozijnen_en__deuren
    
if "Binnenkozijnen_en__deuren_on" not in st.session_state:
    st.session_state.Binnenkozijnen_en__deuren_on = 1
    
st.session_state._Binnenkozijnen_en__deuren_on = st.session_state.Binnenkozijnen_en__deuren_on

def set_Binnenkozijnen_en__deuren_on():
    st.session_state.Binnenkozijnen_en__deuren_on = st.session_state._Binnenkozijnen_en__deuren_on
    
if "Luiken_en_vensters" not in st.session_state:
    st.session_state.Luiken_en_vensters = None
    
st.session_state._Luiken_en_vensters = st.session_state.Luiken_en_vensters

def set_Luiken_en_vensters():
    st.session_state.Luiken_en_vensters = st.session_state._Luiken_en_vensters
    
if "Luiken_en_vensters_on" not in st.session_state:
    st.session_state.Luiken_en_vensters_on = 1
    
st.session_state._Luiken_en_vensters_on = st.session_state.Luiken_en_vensters_on

def set_Luiken_en_vensters_on():
    st.session_state.Luiken_en_vensters_on = st.session_state._Luiken_en_vensters_on
    
if "Balustrades_en_leuningen" not in st.session_state:
    st.session_state.Balustrades_en_leuningen = None
    
st.session_state._Balustrades_en_leuningen = st.session_state.Balustrades_en_leuningen

def set_Balustrades_en_leuningen():
    st.session_state.Balustrades_en_leuningen = st.session_state._Balustrades_en_leuningen
    
if "Balustrades_en_leuningen_on" not in st.session_state:
    st.session_state.Balustrades_en_leuningen_on = 1
    
st.session_state._Balustrades_en_leuningen_on = st.session_state.Balustrades_en_leuningen_on

def set_Balustrades_en_leuningen_on():
    st.session_state.Balustrades_en_leuningen_on = st.session_state._Balustrades_en_leuningen_on
    
if "Binnenwandafwerkingen" not in st.session_state:
    st.session_state.Binnenwandafwerkingen = None
    
st.session_state._Binnenwandafwerkingen = st.session_state.Binnenwandafwerkingen

def set_Binnenwandafwerkingen():
    st.session_state.Binnenwandafwerkingen = st.session_state._Binnenwandafwerkingen
    
if "Binnenwandafwerkingen_on" not in st.session_state:
    st.session_state.Binnenwandafwerkingen_on = 1
    
st.session_state._Binnenwandafwerkingen_on = st.session_state.Binnenwandafwerkingen_on

def set_Binnenwandafwerkingen_on():
    st.session_state.Binnenwandafwerkingen_on = st.session_state._Binnenwandafwerkingen_on
    
if "Vloerafwerkingen" not in st.session_state:
    st.session_state.Vloerafwerkingen = None
    
st.session_state._Vloerafwerkingen = st.session_state.Vloerafwerkingen

def set_Vloerafwerkingen():
    st.session_state.Vloerafwerkingen = st.session_state._Vloerafwerkingen
    
if "Vloerafwerkingen_on" not in st.session_state:
    st.session_state.Vloerafwerkingen_on = 1
    
st.session_state._Vloerafwerkingen_on = st.session_state.Vloerafwerkingen_on

def set_Vloerafwerkingen_on():
    st.session_state.Vloerafwerkingen_on = st.session_state._Vloerafwerkingen_on
    
if "Plafonds" not in st.session_state:
    st.session_state.Plafonds = None
    
st.session_state._Plafonds = st.session_state.Plafonds

def set_Plafonds():
    st.session_state.Plafonds = st.session_state._Plafonds
    
if "Plafonds_on" not in st.session_state:
    st.session_state.Plafonds_on = 1
    
st.session_state._Plafonds_on = st.session_state.Plafonds_on

def set_Plafonds_on():
    st.session_state.Plafonds_on = st.session_state._Plafonds_on
    
if "Vaste_gebouwvoorziening" not in st.session_state:
    st.session_state.Vaste_gebouwvoorziening = None
    
st.session_state._Vaste_gebouwvoorziening = st.session_state.Vaste_gebouwvoorziening

def set_Vaste_gebouwvoorziening():
    st.session_state.Vaste_gebouwvoorziening = st.session_state._Vaste_gebouwvoorziening
    
if "Vaste_gebouwvoorziening_on" not in st.session_state:
    st.session_state.Vaste_gebouwvoorziening_on = 1
    
st.session_state._Vaste_gebouwvoorziening_on = st.session_state.Vaste_gebouwvoorziening_on

def set_Vaste_gebouwvoorziening_on():
    st.session_state.Vaste_gebouwvoorziening_on = st.session_state._Vaste_gebouwvoorziening_on
    
if "Keuken" not in st.session_state:
    st.session_state.Keuken = None
    
st.session_state._Keuken = st.session_state.Keuken

def set_Keuken():
    st.session_state.Keuken = st.session_state._Keuken
    
if "Keuken_on" not in st.session_state:
    st.session_state.Keuken_on = 1
    
st.session_state._Keuken_on = st.session_state.Keuken_on

def set_Keuken_on():
    st.session_state.Keuken_on = st.session_state._Keuken_on
    
if "Terreininrichting" not in st.session_state:
    st.session_state.Terreininrichting = None
    
st.session_state._Terreininrichting = st.session_state.Terreininrichting

def set_Terreininrichting():
    st.session_state.Terreininrichting = st.session_state._Terreininrichting
    
if "Terreininrichting_on" not in st.session_state:
    st.session_state.Terreininrichting_on = 1
    
st.session_state._Terreininrichting_on = st.session_state.Terreininrichting_on

def set_Terreininrichting_on():
    st.session_state.Terreininrichting_on = st.session_state._Terreininrichting_on


# In[ ]:


st.title("Productgroepen")


# In[ ]:


import streamlit as st

# Define a list of dictionaries for each wall type and their corresponding attributes
elements = [
    {"type": "21 Buitenwanden", "label": "Aantal m2 aan buitenwanden in het huidige project", "key_input": "_Buitenwanden", "key_toggle": "_Buitenwanden_on", "on_change_input": set_Buitenwanden, "on_change_toggle": set_Buitenwanden_on},
    {"type": "22 Binnenwanden", "label": "Aantal m2 aan binnenwanden in het huidige project", "key_input": "_Binnenwanden", "key_toggle": "_Binnenwanden_on", "on_change_input": set_Binnenwanden, "on_change_toggle": set_Binnenwanden_on},
    {"type": "23 Vloeren", "label": "Aantal m2 aan vloeren in het huidige project", "key_input": "_Vloeren", "key_toggle": "_Vloeren_on", "on_change_input": set_Vloeren, "on_change_toggle": set_Vloeren_on},
    {"type": "24 Trappen en hellingen", "label": "Aantal stuks aan trappen en hellingen in het huidige project", "key_input": "_Trappen_en_hellingen", "key_toggle": "_Trappen_en_hellingen_on", "on_change_input": set_Trappen_en_hellingen, "on_change_toggle": set_Trappen_en_hellingen_on},
    {"type": "27 Daken", "label": "Aantal m2 aan daken in het huidige project", "key_input": "_Daken", "key_toggle": "_Daken_on", "on_change_input": set_Daken, "on_change_toggle": set_Daken_on},
    {"type": "28 Hoofddraagconstructie", "label": "Aantal m2 aan hoofddraagconstructie in het huidige project", "key_input": "_Hoofddraagconstructie", "key_toggle": "_Hoofddraagconstructie_on", "on_change_input": set_Hoofddraagconstructie, "on_change_toggle": set_Hoofddraagconstructie_on},
    {"type": "31 Buitenkozijnen, -ramen, -deuren en -puien", "label": "Aantal m aan buitenkozijnen, -ramen, -deuren en -puien in het huidige project", "key_input": "_Buitenkozijnen", "key_toggle": "_Buitenkozijnen_on", "on_change_input": set_Buitenkozijnen, "on_change_toggle": set_Buitenkozijnen_on},
    {"type": "32 Binnenkozijnen en -deuren", "label": "Aantal stuks aan binnenkozijnen en -deuren in het huidige project", "key_input": "_Binnenkozijnen_en__deuren", "key_toggle": "_Binnenkozijnen_en__deuren_on", "on_change_input": set_Binnenkozijnen_en__deuren, "on_change_toggle": set_Binnenkozijnen_en__deuren_on},
    {"type": "33 Luiken en vensters", "label": "Aantal stuks aan luiken en vensters in het huidige project", "key_input": "_Luiken_en_vensters", "key_toggle": "_Luiken_en_vensters_on", "on_change_input": set_Luiken_en_vensters, "on_change_toggle": set_Luiken_en_vensters_on},
    {"type": "34 Balustrades en leuningen", "label": "Aantal m aan balustrades en leuningen in het huidige project", "key_input": "_Balustrades_en_leuningen", "key_toggle": "_Balustrades_en_leuningen_on", "on_change_input": set_Balustrades_en_leuningen, "on_change_toggle": set_Balustrades_en_leuningen_on},
    {"type": "42 Binnenwandafwerkingen", "label": "Aantal m2 aan binnenwandafwerkingen in het huidige project", "key_input": "_Binnenwandafwerkingen", "key_toggle": "_Binnenwandafwerkingen_on", "on_change_input": set_Binnenwandafwerkingen, "on_change_toggle": set_Binnenwandafwerkingen_on},
    {"type": "43 Vloerafwerkingen", "label": "Aantal m2 aan vloerafwerkingen in het huidige project", "key_input": "_Vloerafwerkingen", "key_toggle": "_Vloerafwerkingen_on", "on_change_input": set_Vloerafwerkingen, "on_change_toggle": set_Vloerafwerkingen_on},
    {"type": "45 Plafonds", "label": "Aantal m2 aan plafonds in het huidige project", "key_input": "_Plafonds", "key_toggle": "_Plafonds_on", "on_change_input": set_Plafonds, "on_change_toggle": set_Plafonds_on},
    {"type": "64 Vaste gebouwvoorziening", "label": "Aantal stuks aan vaste gebouwvoorziening in het huidige project", "key_input": "_Vaste_gebouwvoorziening", "key_toggle": "_Vaste_gebouwvoorziening_on", "on_change_input": set_Vaste_gebouwvoorziening, "on_change_toggle": set_Vaste_gebouwvoorziening_on},
    {"type": "73 Keuken", "label": "Aantal stuks aan keuken in het huidige project", "key_input": "_Keuken", "key_toggle": "_Keuken_on", "on_change_input": set_Keuken, "on_change_toggle": set_Keuken_on},
    {"type": "90 Terreininrichting", "label": "Aantal stuks aan terreininrichting in het huidige project", "key_input": "_Terreininrichting", "key_toggle": "_Terreininrichting_on", "on_change_input": set_Terreininrichting, "on_change_toggle": set_Terreininrichting_on}
]

# Loop through the list to create the UI elements for each element type
for element in elements:
    st.markdown(f"**{element['type']}**")
    st.number_input(element['label'], value=None, 
                    placeholder="vul het aantal m2 in" if 'm2' in element['label'] else "vul het aantal stuks in", 
                    key=element['key_input'], 
                    on_change=element['on_change_input'])
    col1, col2 = st.columns([0.5, 9.5])
    with col1:
        toggle = st.toggle("", key=element['key_toggle'], 
                           on_change=element['on_change_toggle'])
    with col2:
        if toggle:
            st.markdown(f"Aanpassingen aan de hoeveelheid binnen {element['type'][2:].lower()} mogelijk")
        else:
            st.markdown(f"Aanpassingen aan de hoeveelheid binnen {element['type'][2:].lower()} niet mogelijk")


# In[ ]:


st.markdown("**Budget**")
st.number_input("Vul het budget in voor het huidige project", value=None, placeholder="Typ een bedrag", 
                key='_budget', on_change=set_budget)

st.markdown("**Aantal appartementen**")
st.number_input("Het aantal appartementen dat gebouwd worden in dit project", value=0, key='_appartementen', 
                on_change=set_appartementen)


keys = ['Buitenwanden', 'Binnenwanden', 'Vloeren', 'Trappen_en_hellingen', 'Daken', 'Hoofddraagconstructie', 'Buitenkozijnen', 
 'Binnenkozijnen_en__deuren', 'Luiken_en_vensters', 'Balustrades_en_leuningen', 'Binnenwandafwerkingen', 'Vloerafwerkingen', 
 'Plafonds', 'Vaste_gebouwvoorziening', 'Keuken', 'Terreininrichting', 'budget', 'appartementen']

st.page_link("simplex.py", label = 'Homepagina')

if all(st.session_state[key] is not None for key in keys): 
    st.page_link("pages/optimalisatie3.py", label="Naar optimalisatie")

