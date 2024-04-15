#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from menu2 import menu_with_redirect
menu_with_redirect()


# In[ ]:


st.markdown("optimalisatie")


# In[ ]:


st.dataframe(st.session_state.file)
st.markdown(st.session_state.weging_onderhoud)
st.markdown(st.session_state.weging_circulair)
st.markdown(st.session_state.weging_kwaliteit)
st.markdown(st.session_state.weging_budget)
st.markdown(st.session_state.weging_woonbeleving)


# In[ ]:


impact = st.session_state.file

data = {
        "productgroep": ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', '28 Hoofddraagconstructie', 
                         '31 Buitenkozijnen, -ramen, -deuren, en -puien', '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', 
                         '34 Balustrades en leuningen', '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '48 Na-isolatie', 
                         '52 Riolering en HWA', '53 Warm- en koud water installaties', '56 Verwarming en koeling', '57 Luchtbehandeling', 
                         '61 Elektrische installaties', '64 Vaste gebouwvoorziening', '65 Beveiliging', '66 Lift', '73 Keuken', '74 Sanitair', 
                         '90 Terreininrichting'],
        "impact onderhoud": [impact.iloc[i, 1] for i in range(len(impact))],
        "impact circulair": [impact.iloc[i, 2] for i in range(len(impact))],
        "impact kwaliteit": [impact.iloc[i, 3] for i in range(len(impact))],
        "impact budget": [impact.iloc[i, 4] for i in range(len(impact))], 
        "impact woonbeleving": [impact.iloc[i, 5] for i in range(len(impact))]
        }
        
        df = pd.DataFrame(data)
    
        onderhoud = df[['productgroep', 'impact onderhoud']]
        onderhoud = onderhoud.sort_values(by='impact onderhoud', ascending=False)
        onderhoud = onderhoud.reset_index(drop=True)
        
        circulair = df[['productgroep', 'impact circulair']]
        circulair = circulair.sort_values(by='impact circulair', ascending=False)
        circulair = circulair.reset_index(drop=True)
    
        kwaliteit = df[['productgroep', 'impact kwaliteit']]
        kwaliteit = kwaliteit.sort_values(by='impact kwaliteit', ascending=False)
        kwaliteit = kwaliteit.reset_index(drop=True)
        
        budget = df[['productgroep', 'impact budget']]
        budget = budget.sort_values(by='impact budget', ascending=False)
        budget = budget.reset_index(drop=True)
        
        woonbeleving = df[['productgroep', 'impact woonbeleving']]
        woonbeleving = woonbeleving.sort_values(by='impact woonbeleving', ascending=False)
        woonbeleving = woonbeleving.reset_index(drop=True)


# In[ ]:


if (onderhoud['impact onderhoud'].iloc[0] and onderhoud['impact onderhoud'].iloc[1] and onderhoud['impact onderhoud'].iloc[2]) > 0:
    st.markdown('**Onderhoud**')
    st.markdown(
    f"""
    De productgroepen die het meeste impact maken op het thema 'Onderhoud':
    - {onderhoud['productgroep'].iloc[0]}
    - {onderhoud['productgroep'].iloc[1]}
    - {onderhoud['productgroep'].iloc[2]}
    """
    )
if (circulair['impact circulair'].iloc[0] and circulair['impact circulair'].iloc[1] and circulair['impact circulair'].iloc[2]) > 0:
    st.markdown('**Circulair**')
    st.markdown(
    f"""
    De productgroepen die het meeste impact maken op het thema 'Duurzaam':
    - {circulair['productgroep'].iloc[0]}
    - {circulair['productgroep'].iloc[1]}
    - {circulair['productgroep'].iloc[2]}
    """
    )    
if (kwaliteit['impact kwaliteit'].iloc[0] and kwaliteit['impact kwaliteit'].iloc[1] and kwaliteit['impact kwaliteit'].iloc[2]) > 0:
    st.markdown('**Kwaliteit**')
    st.markdown(
    f"""
    De productgroepen die het meeste impact maken op het thema 'Kwaliteit':
    - {kwaliteit['productgroep'].iloc[0]}
    - {kwaliteit['productgroep'].iloc[1]}
    - {kwaliteit['productgroep'].iloc[2]}
    """
    )
if (budget['impact budget'].iloc[0] and budget['impact budget'].iloc[1] and budget['impact budget'].iloc[2]) > 0:
    st.markdown('**Budget**')
    st.markdown(
    f"""
    De productgroepen die het meeste impact maken op het thema 'Budget':
    - {budget['productgroep'].iloc[0]}
    - {budget['productgroep'].iloc[1]}
    - {budget['productgroep'].iloc[2]}
    """
    )
if (woonbeleving['impact woonbeleving'].iloc[0] and woonbeleving['impact woonbeleving'].iloc[1] and woonbeleving['impact woonbeleving'].iloc[2]) > 0:
    st.markdown('**Woonbeleving**')
    st.markdown(
    f"""
    De productgroepen die het meeste impact maken op het thema 'Woonbeleving':
    - {woonbeleving['productgroep'].iloc[0]}
    - {woonbeleving['productgroep'].iloc[1]}
    - {woonbeleving['productgroep'].iloc[2]}
    """
    )

