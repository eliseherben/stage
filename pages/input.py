#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pulp as pl
import locale


# In[ ]:


if "budget" not in st.session_state:
    st.session_state.budget = None
    
st.session_state._budget = st.session_state.budget

def set_budget():
    st.session_state.budget = st.session_state._budget
    
if "huidig_budget" not in st.session_state:
    st.session_state.huidig_budget = None
    
st.session_state._huidig_budget = st.session_state.huidig_budget

def set_huidig_budget():
    st.session_state.huidig_budget = st.session_state._huidig_budget
    
if "streven_budget" not in st.session_state:
    st.session_state.streven_budget = None
    
st.session_state._set_streven_budget = st.session_state.streven_budget

def set_streven_budget():
    st.session_state.streven_budget = st.session_state._set_streven_budget
    
if "appartementen" not in st.session_state:
    st.session_state.appartementen = 0
    
st.session_state._appartementen = st.session_state.appartementen

def set_appartementen():
    st.session_state.appartementen = st.session_state._appartementen
    
if "doelstelling" not in st.session_state:
    st.session_state.doelstelling = None
    
st.session_state._doelstelling = st.session_state.doelstelling

def set_doelstelling():
    st.session_state.doelstelling = st.session_state._doelstelling


# productgroepen

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
    
if "Na_isolatie" not in st.session_state:
    st.session_state.Na_isolatie = None
    
st.session_state._Na_isolatie = st.session_state.Na_isolatie

def set_Na_isolatie():
    st.session_state.Na_isolatie = st.session_state._Na_isolatie
    
if "Riolering_en_HWA" not in st.session_state:
    st.session_state.Riolering_en_HWA = None
    
st.session_state._Riolering_en_HWA = st.session_state.Riolering_en_HWA

def set_Riolering_en_HWA():
    st.session_state.Riolering_en_HWA = st.session_state._Riolering_en_HWA
    
if "Warm__en_koud_water_installaties" not in st.session_state:
    st.session_state.Warm__en_koud_water_installaties = None
    
st.session_state._Warm__en_koud_water_installaties = st.session_state.Warm__en_koud_water_installaties

def set_Warm__en_koud_water_installaties():
    st.session_state.Warm__en_koud_water_installaties = st.session_state._Warm__en_koud_water_installaties
    
if "Verwarming_en_koeling" not in st.session_state:
    st.session_state.Verwarming_en_koeling = None
    
st.session_state._Verwarming_en_koeling = st.session_state.Verwarming_en_koeling

def set_Verwarming_en_koeling():
    st.session_state.Verwarming_en_koeling = st.session_state._Verwarming_en_koeling
    
if "Luchtbehandeling" not in st.session_state:
    st.session_state.Luchtbehandeling = None
    
st.session_state._Luchtbehandeling = st.session_state.Luchtbehandeling

def set_Luchtbehandeling():
    st.session_state.Luchtbehandeling = st.session_state._Luchtbehandeling
    
if "Elektrische_installaties" not in st.session_state:
    st.session_state.Elektrische_installaties = None
    
st.session_state._Elektrische_installaties = st.session_state.Elektrische_installaties

def set_Elektrische_installaties():
    st.session_state.Elektrische_installaties = st.session_state._Elektrische_installaties
    
if "Vaste_gebouwvoorziening" not in st.session_state:
    st.session_state.Vaste_gebouwvoorziening = None
    
st.session_state._Vaste_gebouwvoorziening = st.session_state.Vaste_gebouwvoorziening

def set_Vaste_gebouwvoorziening():
    st.session_state.Vaste_gebouwvoorziening = st.session_state._Vaste_gebouwvoorziening
    
if "Beveiliging" not in st.session_state:
    st.session_state.Beveiliging = None
    
st.session_state._Beveiliging = st.session_state.Beveiliging

def set_Beveiliging():
    st.session_state.Beveiliging = st.session_state._Beveiliging
    
if "Liften" not in st.session_state:
    st.session_state.Liften = None
    
st.session_state._Liften = st.session_state.Liften

def set_Liften():
    st.session_state.Liften = st.session_state._Liften
    
if "Keuken" not in st.session_state:
    st.session_state.Keuken = None
    
st.session_state._Keuken = st.session_state.Keuken

def set_Keuken():
    st.session_state.Keuken = st.session_state._Keuken
    
if "Sanitair" not in st.session_state:
    st.session_state.Sanitair = None
    
st.session_state._Sanitair = st.session_state.Sanitair

def set_Sanitair():
    st.session_state.Sanitair = st.session_state._Sanitair
    
if "Terreininrichting" not in st.session_state:
    st.session_state.Terreininrichting = None
    
st.session_state._Terreininrichting = st.session_state.Terreininrichting

def set_Terreininrichting():
    st.session_state.Terreininrichting = st.session_state._Terreininrichting


# productgroepen toggle

# In[ ]:


if "Buitenwanden_on" not in st.session_state:
    st.session_state.Buitenwanden_on = 1
    
st.session_state._Buitenwanden_on = st.session_state.Buitenwanden_on

def set_Buitenwanden_on():
    st.session_state.Buitenwanden_on = st.session_state._Buitenwanden_on

if "Binnenwanden_on" not in st.session_state:
    st.session_state.Binnenwanden_on = 1
    
st.session_state._Binnenwanden_on = st.session_state.Binnenwanden_on

def set_Binnenwanden_on():
    st.session_state.Binnenwanden_on = st.session_state._Binnenwanden_on
    
if "Vloeren_on" not in st.session_state:
    st.session_state.Vloeren_on = 1
    
st.session_state._Vloeren_on = st.session_state.Vloeren_on

def set_Vloeren_on():
    st.session_state.Vloeren_on = st.session_state._Vloeren_on
    
if "Trappen_en_hellingen_on" not in st.session_state:
    st.session_state.Trappen_en_hellingen_on = 1
    
st.session_state._Trappen_en_hellingen_on = st.session_state.Trappen_en_hellingen_on

def set_Trappen_en_hellingen_on():
    st.session_state.Trappen_en_hellingen_on = st.session_state._Trappen_en_hellingen_on
    
if "Daken_on" not in st.session_state:
    st.session_state.Daken_on = 1
    
st.session_state._Daken_on = st.session_state.Daken_on

def set_Daken_on():
    st.session_state.Daken_on = st.session_state._Daken_on
    
if "Hoofddraagconstructie_on" not in st.session_state:
    st.session_state.Hoofddraagconstructie_on = 1
    
st.session_state._Hoofddraagconstructie_on = st.session_state.Hoofddraagconstructie_on

def set_Hoofddraagconstructie_on():
    st.session_state.Hoofddraagconstructie_on = st.session_state._Hoofddraagconstructie_on    
    
if "Buitenkozijnen_on" not in st.session_state:
    st.session_state.Buitenkozijnen_on = 1
    
st.session_state._Buitenkozijnen_on = st.session_state.Buitenkozijnen_on

def set_Buitenkozijnen_on():
    st.session_state.Buitenkozijnen_on = st.session_state._Buitenkozijnen_on
    
if "Binnenkozijnen_en__deuren_on" not in st.session_state:
    st.session_state.Binnenkozijnen_en__deuren_on = 1
    
st.session_state._Binnenkozijnen_en__deuren_on = st.session_state.Binnenkozijnen_en__deuren_on

def set_Binnenkozijnen_en__deuren_on():
    st.session_state.Binnenkozijnen_en__deuren_on = st.session_state._Binnenkozijnen_en__deuren_on
    
if "Luiken_en_vensters_on" not in st.session_state:
    st.session_state.Luiken_en_vensters_on = 1
    
st.session_state._Luiken_en_vensters_on = st.session_state.Luiken_en_vensters_on

def set_Luiken_en_vensters_on():
    st.session_state.Luiken_en_vensters_on = st.session_state._Luiken_en_vensters_on
    
if "Balustrades_en_leuningen_on" not in st.session_state:
    st.session_state.Balustrades_en_leuningen_on = 1
    
st.session_state._Balustrades_en_leuningen_on = st.session_state.Balustrades_en_leuningen_on

def set_Balustrades_en_leuningen_on():
    st.session_state.Balustrades_en_leuningen_on = st.session_state._Balustrades_en_leuningen_on
    
if "Binnenwandafwerkingen_on" not in st.session_state:
    st.session_state.Binnenwandafwerkingen_on = 1
    
st.session_state._Binnenwandafwerkingen_on = st.session_state.Binnenwandafwerkingen_on

def set_Binnenwandafwerkingen_on():
    st.session_state.Binnenwandafwerkingen_on = st.session_state._Binnenwandafwerkingen_on
    
if "Vloerafwerkingen_on" not in st.session_state:
    st.session_state.Vloerafwerkingen_on = 1
    
st.session_state._Vloerafwerkingen_on = st.session_state.Vloerafwerkingen_on

def set_Vloerafwerkingen_on():
    st.session_state.Vloerafwerkingen_on = st.session_state._Vloerafwerkingen_on
    
if "Plafonds_on" not in st.session_state:
    st.session_state.Plafonds_on = 1
    
st.session_state._Plafonds_on = st.session_state.Plafonds_on

def set_Plafonds_on():
    st.session_state.Plafonds_on = st.session_state._Plafonds_on
    
if "Vaste_gebouwvoorziening_on" not in st.session_state:
    st.session_state.Vaste_gebouwvoorziening_on = 1
    
st.session_state._Vaste_gebouwvoorziening_on = st.session_state.Vaste_gebouwvoorziening_on

def set_Vaste_gebouwvoorziening_on():
    st.session_state.Vaste_gebouwvoorziening_on = st.session_state._Vaste_gebouwvoorziening_on
    
if "Keuken_on" not in st.session_state:
    st.session_state.Keuken_on = 1
    
st.session_state._Keuken_on = st.session_state.Keuken_on

def set_Keuken_on():
    st.session_state.Keuken_on = st.session_state._Keuken_on
    
if "Terreininrichting_on" not in st.session_state:
    st.session_state.Terreininrichting_on = 1
    
st.session_state._Terreininrichting_on = st.session_state.Terreininrichting_on

def set_Terreininrichting_on():
    st.session_state.Terreininrichting_on = st.session_state._Terreininrichting_on


# In[ ]:


st.title("Productgroepen")
st.page_link("simplex.py", label = 'Homepagina')


# In[ ]:


import streamlit as st


# Define a list of dictionaries for each wall type and their corresponding attributes
elements = [
    {"type": "21 Buitenwanden", "label": "Aantal m2 aan buitenwanden in het huidige project *", "key_input": "_Buitenwanden", "key_toggle": "_Buitenwanden_on", "on_change_input": set_Buitenwanden, "on_change_toggle": set_Buitenwanden_on},
    {"type": "22 Binnenwanden", "label": "Aantal m2 aan binnenwanden in het huidige project *", "key_input": "_Binnenwanden", "key_toggle": "_Binnenwanden_on", "on_change_input": set_Binnenwanden, "on_change_toggle": set_Binnenwanden_on},
    {"type": "23 Vloeren", "label": "Aantal m2 aan vloeren in het huidige project *", "key_input": "_Vloeren", "key_toggle": "_Vloeren_on", "on_change_input": set_Vloeren, "on_change_toggle": set_Vloeren_on},
    {"type": "24 Trappen en hellingen", "label": "Aantal stuks aan trappen en hellingen in het huidige project *", "key_input": "_Trappen_en_hellingen", "key_toggle": "_Trappen_en_hellingen_on", "on_change_input": set_Trappen_en_hellingen, "on_change_toggle": set_Trappen_en_hellingen_on},
    {"type": "27 Daken", "label": "Aantal m2 aan daken in het huidige project *", "key_input": "_Daken", "key_toggle": "_Daken_on", "on_change_input": set_Daken, "on_change_toggle": set_Daken_on},
    {"type": "28 Hoofddraagconstructie", "label": "Aantal m2 aan hoofddraagconstructie in het huidige project *", "key_input": "_Hoofddraagconstructie", "key_toggle": "_Hoofddraagconstructie_on", "on_change_input": set_Hoofddraagconstructie, "on_change_toggle": set_Hoofddraagconstructie_on},
    {"type": "31 Buitenkozijnen, -ramen, -deuren en -puien", "label": "Aantal stuks aan buitenkozijnen, -ramen, -deuren en -puien in het huidige project *", "key_input": "_Buitenkozijnen", "key_toggle": "_Buitenkozijnen_on", "on_change_input": set_Buitenkozijnen, "on_change_toggle": set_Buitenkozijnen_on},
    {"type": "32 Binnenkozijnen en -deuren", "label": "Aantal stuks aan binnenkozijnen en -deuren in het huidige project *", "key_input": "_Binnenkozijnen_en__deuren", "key_toggle": "_Binnenkozijnen_en__deuren_on", "on_change_input": set_Binnenkozijnen_en__deuren, "on_change_toggle": set_Binnenkozijnen_en__deuren_on},
    {"type": "33 Luiken en vensters", "label": "Aantal stuks aan luiken en vensters in het huidige project *", "key_input": "_Luiken_en_vensters", "key_toggle": "_Luiken_en_vensters_on", "on_change_input": set_Luiken_en_vensters, "on_change_toggle": set_Luiken_en_vensters_on},
    {"type": "34 Balustrades en leuningen", "label": "Aantal m aan balustrades en leuningen in het huidige project *", "key_input": "_Balustrades_en_leuningen", "key_toggle": "_Balustrades_en_leuningen_on", "on_change_input": set_Balustrades_en_leuningen, "on_change_toggle": set_Balustrades_en_leuningen_on},
    {"type": "42 Binnenwandafwerkingen", "label": "Aantal m2 aan binnenwandafwerkingen in het huidige project *", "key_input": "_Binnenwandafwerkingen", "key_toggle": "_Binnenwandafwerkingen_on", "on_change_input": set_Binnenwandafwerkingen, "on_change_toggle": set_Binnenwandafwerkingen_on},
    {"type": "43 Vloerafwerkingen", "label": "Aantal m2 aan vloerafwerkingen in het huidige project *", "key_input": "_Vloerafwerkingen", "key_toggle": "_Vloerafwerkingen_on", "on_change_input": set_Vloerafwerkingen, "on_change_toggle": set_Vloerafwerkingen_on},
    {"type": "45 Plafonds", "label": "Aantal m2 aan plafonds in het huidige project *", "key_input": "_Plafonds", "key_toggle": "_Plafonds_on", "on_change_input": set_Plafonds, "on_change_toggle": set_Plafonds_on},
    {"type": "64 Vaste gebouwvoorziening", "label": "Aantal stuks aan vaste gebouwvoorziening in het huidige project *", "key_input": "_Vaste_gebouwvoorziening", "key_toggle": "_Vaste_gebouwvoorziening_on", "on_change_input": set_Vaste_gebouwvoorziening, "on_change_toggle": set_Vaste_gebouwvoorziening_on},
    {"type": "73 Keuken", "label": "Aantal stuks aan keuken in het huidige project *", "key_input": "_Keuken", "key_toggle": "_Keuken_on", "on_change_input": set_Keuken, "on_change_toggle": set_Keuken_on},
    {"type": "90 Terreininrichting", "label": "Aantal stuks aan terreininrichting in het huidige project *", "key_input": "_Terreininrichting", "key_toggle": "_Terreininrichting_on", "on_change_input": set_Terreininrichting, "on_change_toggle": set_Terreininrichting_on}
]
keys = ['budget', 'appartementen', 'doelstelling']
# Loop through the list to create the UI elements for each element type
for element in elements:
    if element['type'][:2] in st.session_state.list:
        keys.append(element['key_input'][1:])
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
                st.markdown(f"Aanpassingen aan de hoeveelheid van {element['type'][2:].lower()} mogelijk")
            else:
                st.markdown(f"Aanpassingen aan de hoeveelheid van {element['type'][2:].lower()} **niet** mogelijk")


# In[3]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
# data


# In[ ]:


st.markdown("**Aantal appartementen**")
st.number_input("Het aantal appartementen dat gebouwd worden in dit project *", key='_appartementen', 
                on_change=set_appartementen)

st.markdown("**Budget**")
data['aantal'] = None
data.iloc[0, -1] = st.session_state.Buitenwanden
data.iloc[1, -1] = st.session_state.Binnenwanden
data.iloc[2, -1] = st.session_state.Vloeren
data.iloc[3, -1] = st.session_state.Trappen_en_hellingen
data.iloc[4, -1] = st.session_state.Daken
data.iloc[5, -1] = st.session_state.Hoofddraagconstructie
data.iloc[6, -1] = st.session_state.Buitenkozijnen
data.iloc[7, -1] = st.session_state.Binnenkozijnen_en__deuren
data.iloc[8, -1] = st.session_state.Luiken_en_vensters
data.iloc[9, -1] = st.session_state.Balustrades_en_leuningen
data.iloc[10, -1] = st.session_state.Binnenwandafwerkingen
data.iloc[11, -1] = st.session_state.Vloerafwerkingen
data.iloc[12, -1] = st.session_state.Plafonds
data.iloc[13, -1] = st.session_state.appartementen
data.iloc[14, -1] = st.session_state.appartementen
data.iloc[15, -1] = st.session_state.appartementen
data.iloc[16, -1] = st.session_state.appartementen
data.iloc[17, -1] = st.session_state.appartementen
data.iloc[18, -1] = st.session_state.appartementen
data.iloc[19, -1] = st.session_state.Vaste_gebouwvoorziening
data.iloc[20, -1] = st.session_state.appartementen
data.iloc[21, -1] = st.session_state.appartementen
data.iloc[22, -1] = st.session_state.Keuken
data.iloc[23, -1] = st.session_state.appartementen
data.iloc[24, -1] = st.session_state.Terreininrichting

st.markdown(f"Totale kosten gebasseerd op huidige hoeveelheden: €{((data['kosten'] * data['aantal']).sum()):.2f}")

data['minimaal'] = data['minimaal'].fillna(1)
data['maximaal'] = data['maximaal'].fillna(1)

# st.number_input("Vul het budget in voor het huidige project *",  
#                 min_value = (data['minimaal'] * st.session_state.appartementen * data['kosten']).sum(), 
#                 max_value = (data['maximaal'] * st.session_state.appartementen * data['kosten']).sum(),
#                 key='_budget', on_change=set_budget)

st.number_input("Vul het budget in op basis van de huidige hoeveelheden binnen het project", 
                               key = '_huidig_budget', on_change=set_huidig_budget)

# st.markdown(f'factor: {huidig_budget / streven_budget}, budget optimalisatie: {((data["kosten"] * data["aantal"]).sum())/(huidig_budget / streven_budget)}')

budget = ((data["kosten"] * data["aantal"]).sum())
minimaal = (data['minimaal'] * st.session_state.appartementen * data['kosten']).sum()
maximaal = (data['maximaal'] * st.session_state.appartementen * data['kosten']).sum()
st.markdown(minimaal)
st.markdown(maximaal)

st.markdown(minimaal * (st.session_state.huidig_budget/budget))
st.markdown(maximaal * (st.session_state.huidig_budget/budget))
    
st.number_input("Vul het te streven budget in voor het huidige project", 
                min_value = minimaal * (st.session_state.huidig_budget/budget), 
                max_value = maximaal * (st.session_state.huidig_budget/budget), 
               key = '_streven_budget', on_change=set_streven_budget)

st.markdown(st.session_state.streven_budget)

st.session_state.budget = st.session_state.streven_budget / (st.session_state.huidig_budget/budget)
st.markdown(st.session_state.budget)
st.markdown("**Primair thema**")
# st.markdown("De verschillende thema's krijgen in de optimalisatie een weging. Op basis van de keuze van het primaire thema zal de weging voor dit thema hoger liggen dan de weging voor het andere thema. Hiermee zal het primaire thema, met een hogere weging dus als belangrijker gezien worden in de optimalisatie. ")
st.selectbox("Wat heeft meer prioriteit binnen dit project? *", 
            ("Minimale milieukosten", "Minimale afwijkingen van de huidge aantallen", "Geen voorkeur"), 
            key='_doelstelling', on_change=set_doelstelling)


if all(st.session_state[key] is not None for key in keys): 
    st.page_link("pages/optimalisatie3.py", label="Naar optimalisatie")


