#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import pulp as pl
import plotly.express as px
# from menu2 import menu_with_redirect
# menu_with_redirect()


# In[ ]:


if 'weging_onderhoud' not in st.session_state:
    st.session_state.weging_onderhoud = None

st.session_state._weging_onderhoud = st.session_state.weging_onderhoud

def set_weging_onderhoud():
    st.session_state.weging_onderhoud = st.session_state._weging_onderhoud

if 'weging_circulair' not in st.session_state:
    st.session_state.weging_circulair = None

st.session_state._weging_circulair = st.session_state.weging_circulair

def set_weging_circulair():
    st.session_state.weging_circulair = st.session_state._weging_circulair

if 'weging_kwaliteit' not in st.session_state:
    st.session_state.weging_kwaliteit = None

st.session_state._weging_kwaliteit = st.session_state.weging_kwaliteit

def set_weging_kwaliteit():
    st.session_state.weging_kwaliteit = st.session_state._weging_kwaliteit

if 'weging_budget' not in st.session_state:
    st.session_state.weging_budget = None

st.session_state._weging_budget = st.session_state.weging_budget

def set_weging_budget():
    st.session_state.weging_budget = st.session_state._weging_budget

if 'weging_woonbeleving' not in st.session_state:
    st.session_state.weging_woonbeleving = None

st.session_state._weging_woonbeleving = st.session_state.weging_woonbeleving

def set_weging_woonbeleving():
    st.session_state.weging_woonbeleving = st.session_state._weging_woonbeleving


# In[ ]:


st.write("#")
st.title("Optimalisatie")
tab1, tab2 = st.tabs(["Optimalisatie", "Aanpassingen"])
st.page_link("pages/advies.py", label="Naar advies")
st.page_link("simplex.py", label="Homepagina")


# In[ ]:


with tab1: 
    if st.session_state.projectbestand is None:
        st.markdown("upload een bestand")
    else: 
        #barplot
        st.dataframe(st.session_state.file, hide_index = True)
        df_fig = pd.melt(st.session_state.file, id_vars=['productgroep'], var_name='Optie', value_name='impact')

        df_fig = df_fig[df_fig['impact'] != 0]
        
        # Plot met Plotly Express
        fig = px.bar(df_fig, x='productgroep', y='impact', color='Optie',
             barmode='group', title="Impact thema's op productgroepen")
        st.plotly_chart(fig)
        
        st.write("#")
        
        st.markdown("**Rank**")
        data = {
          "thema": ['onderhoud', 'budget', 'kwaliteit', 'woonbeleving', 'circulariteit'],
          "rank": [1, 2, 3, 4, 5]
        }
        
        df = pd.DataFrame(data)
        ranking_df = st.data_editor(df, disabled = ["thema"], width = 500, hide_index = True)
        ranking_df = ranking_df.sort_values(by = ['rank'])
        ranking_df = ranking_df.reset_index(drop=True)
        
        ranking_df['rank sum (RS)'] = (len(ranking_df) - ranking_df['rank'] + 1)/sum(ranking_df['rank'])
        ranking_df['rank reciprocal (RR)'] = (1/ranking_df['rank'])/sum(1/ranking_df['rank'])
        ranking_df['rank order centroid (ROC)'] = (1/len(ranking_df))*((1/ranking_df['rank'].iloc[::-1]).cumsum())
        ranking_df = ranking_df.round({"rank":0, "rank sum (RS)":2, "rank reciprocal (RR)":2,"rank order centroid (ROC)":2})

        weights_df = ranking_df.sort_values(by = ['thema'])
        weights_df = weights_df.reset_index(drop=True)
        st.dataframe(ranking_df)
        st.dataframe(weights_df)

        rs_budget = weights_df['rank sum (RS)'].iloc[0]
        st.markdown(rs_budget)
        rs_circulariteit = weights_df['rank sum (RS)'].iloc[1]
        st.markdown(rs_circulariteit)
        rs_kwaliteit = weights_df['rank sum (RS)'].iloc[2]
        st.markdown(rs_kwaliteit)
        rs_onderhoud = weights_df['rank sum (RS)'].iloc[3]
        st.markdown(rs_onderhoud)
        rs_woonbeleving = weights_df['rank sum (RS)'].iloc[4]
        st.markdown(rs_woonbeleving)
        
        impact = st.session_state.file
        st.dataframe(impact)
        
        data = {
                "productgroep": ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', '28 Hoofddraagconstructie', 
                                 '31 Buitenkozijnen, -ramen, -deuren, en -puien', '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', 
                                 '34 Balustrades en leuningen', '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '48 Na-isolatie', 
                                 '52 Riolering en HWA', '53 Warm- en koud water installaties', '56 Verwarming en koeling', '57 Luchtbehandeling', 
                                 '61 Elektrische installaties', '64 Vaste gebouwvoorziening', '65 Beveiliging', '66 Liften', '73 Keuken', '74 Sanitair', 
                                 '90 Terreininrichting'],
                "impact onderhoud": [impact.iloc[i, 1] for i in range(len(impact))],
                "impact circulair": [impact.iloc[i, 2] for i in range(len(impact))],
                "impact kwaliteit": [impact.iloc[i, 3] for i in range(len(impact))],
                "impact budget": [impact.iloc[i, 4] for i in range(len(impact))], 
                "impact woonbeleving": [impact.iloc[i, 5] for i in range(len(impact))]
                }
                
        df = pd.DataFrame(data)
        st.markdown("dataframe impact?")
        st.dataframe(df)
        
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


with tab1:
    if st.session_state.projectbestand is None:
        st.markdown("upload een bestand")
    else: 
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


# In[ ]:


with tab1: 
    if st.session_state.projectbestand is None:
        st.markdown("upload een bestand")
    else: 
    # Creëer een LP probleem
        prob = pl.LpProblem("Eigen Haard", pl.LpMaximize)

        variabelen = {}
        st.markdown("df")
        st.dataframe(df)
        for index, row in df.iterrows():
            variabelen[row["productgroep"]] = pl.LpVariable(row["productgroep"], lowBound = 0)
        
        lp_variabelen = []
        for key, value in variabelen.items():
            st.markdown(f"{key} = {value}")
            lp_variabelen.append((key, value))

        st.markdown(lp_variabelen)
        
        #Impact themas op productgroepen
        impact_onderhoud = [impact.iloc[a, 1] for a in range(len(impact))]
        onderhoud = pl.lpSum(lp_variabelen[i][1] * impact_onderhoud[i] for i in range(25))
        
        impact_circulair = [impact.iloc[a, 2] for a in range(len(impact))]
        circulair = pl.lpSum(lp_variabelen[i][1] * impact_circulair[i] for i in range(25))
        
        impact_kwaliteit = [impact.iloc[a, 3] for a in range(len(impact))]
        kwaliteit = pl.lpSum(lp_variabelen[i][1] * impact_kwaliteit[i] for i in range(25))
        
        impact_budget = [impact.iloc[a, 4] for a in range(len(impact))]
        budget = pl.lpSum(lp_variabelen[i][1] * impact_budget[i] for i in range(25))
        
        impact_woonbeleving = [impact.iloc[a, 5] for a in range(len(impact))]
        woonbeleving = pl.lpSum(lp_variabelen[i][1] * impact_woonbeleving[i] for i in range(25))
        
        prob += rs_circulariteit * circulair - rs_budget * budget + rs_woonbeleving * woonbeleving + rs_kwaliteit * kwaliteit + rs_onderhoud * onderhoud
        
        # Voeg beperkingen toe (voorbeeldbeperkingen)
        prob += sum(lp_variabelen[1]) == 100
        
        data_restricties = {
            "productgroep": ["21 Buitenwanden", "22 Binnenwanden", "23 Vloeren", "24 Trappen en hellingen", "27 Daken", 
                             "28 Hoofddraagconstructie", "31 Buitenkozijnen, -ramen, -deuren en -puien", 
                             "32 Binnenkozijnen en -deuren", "33 Luiken en vensters", "34 Balustrades en leuningen", 
                            "42 Binnenwandafwerkingen", "43 Vloerafwerkingen", "45 Plafonds", "48 Na-isolatie", 
                            "52 Riolering en HWA", "53 Warm- en koud water installaties", "56 Verwarming en koeling", 
                            "57 Luchtbehandeling", "61 Elektrische installaties", "64 Vaste gebouwvoorziening", 
                             "65 Beveiliging", "66 Lift", "73 Keuken", "74 Sanitair", "90 Terreininrichting"], 
            "minimale": [15.5, 1.7, 12.0, 1.0, 2.3, 4.6, 13.7, 1.2, 0.1, 2.8, 0.4, 1.5, 1.4, 0, 0, 0, 0, 
                          0, 0, 0.3, 0, 0, 1.7, 0, 0], 
            "maximale": [35.0, 4.4, 21.6, 2.3, 6.1, 8.4, 18.0, 6.1, 0.2, 3.6, 3.5, 3.2, 2.5, 0, 5.6, 0, 5.6, 5.6, 
                         9.0, 0.4, 0, 0, 1.8, 2.0, 0.1]
        }
    
        minimale = [15.5, 1.7, 12.0, 1.0, 2.3, 4.6, 13.7, 1.2, 0.1, 2.8, 0.4, 1.5, 1.4, 0, 0, 0, 0, 0, 0, 0.3, 0, 0, 1.7, 0, 0]
        maximale = [35.0, 4.4, 21.6, 2.3, 6.1, 8.4, 18.0, 6.1, 0.2, 3.6, 3.5, 3.2, 2.5, 0, 5.6, 0, 5.6, 5.6, 9.0, 0.4, 0, 0, 1.8, 2.0, 0.1]
        
        for i in range(len(lp_variabelen)):
            prob += lp_variabelen[i] >= minimale[i]
            prob += lp_variabelen[i] <= maximale[i]

        # Los het probleem op
        status = prob.solve()
        
        # Maak een lege lijst om de variabelen en hun waarden op te slaan
        variabelen_waarden = []
        
        # Voeg de variabelen en hun waarden toe aan de lijst
        for var in lp_variabelen:
            variabelen_waarden.append((var.name, var.varValue))
        
        # Maak een DataFrame van de lijst
        df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])
        st.dataframe(df)
        
        st.markdown(f"Status van de oplossing: {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie: {prob.objective.value()}")


# In[ ]:


with tab1:
    if st.session_state.projectbestand is None:
        st.markdown("upload een bestand")
    else: 
        st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")
        
        for index, row in df.iterrows():
            st.markdown(f"- De productgroep {row['Productgroep']} is {row['Waarde']}% van het totale project")
        
        fig1 = px.pie(values=df['Waarde'], names=df['Productgroep'], color_discrete_sequence=px.colors.sequential.RdBu)
        
        st.plotly_chart(fig1)


# #### Aanpassingen

# In[ ]:


with tab2:
    if st.session_state.projectbestand is None:
        st.markdown("upload een bestand")
    else: 
        st.markdown("Hieronder kunnen de verschillende aandelen van productgroepen aangepast worden, om daarvan de invloed te zien op de verschillende thema's")
    
        def max_sliders(waardes):
            max_waarde = 100 - sum(waardes)
            return max_waarde
        
        waardes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
        buitenwanden_max = max_sliders(waardes)
        buitenwanden = st.number_input('Het aandeel van de productgroep Buitenwanden', value = 0.0, min_value = 0.0, max_value = buitenwanden_max, step = 0.1)
        
        binnenwanden_max = max_sliders([buitenwanden, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                        0.0, 0.0, 0.0, 0.0, 0.0])
        binnenwanden = st.number_input('Het aandeel van de productgroep Binnenwanden', value = 0.0, min_value = 0.0, max_value = binnenwanden_max,step = 0.1)
    
        vloeren_max = max_sliders([buitenwanden, binnenwanden, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        vloeren = st.number_input('Het aandeel van de productgroep Vloeren', value = 0.0, min_value = 0.0, max_value = vloeren_max, step = 0.1)
    
        trappen_hellingen_max = max_sliders([buitenwanden, binnenwanden, vloeren, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        trappen_hellingen = st.number_input('Het aandeel van de productgroep Trappen en hellingen', value = 0.0, min_value = 0.0, max_value = trappen_hellingen_max,step = 0.1)
    
        daken_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        daken = st.number_input('Het aandeel van de productgroep Daken', value = 0.0, min_value = 0.0, max_value = daken_max, step = 0.1)
    
        hoofddraagconstructie_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, 
                                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        hoofddraagconstructie = st.number_input('Het aandeel van de productgroep Hoofddraagconstructie', value = 0.0, min_value = 0.0, max_value = hoofddraagconstructie_max,step = 0.1)
    
        buitenkozijnen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, 
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        buitenkozijnen = st.number_input('Het aandeel van de productgroep Buitenkozijnen', value = 0.0, min_value = 0.0, max_value = buitenkozijnen_max, step = 0.1)
    
        binnenkozijnen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        binnenkozijnen = st.number_input('Het aandeel van de productgroep Binnenkozijnen', value = 0.0, min_value = 0.0, max_value = binnenkozijnen_max,step = 0.1)
    
        luiken_vensters_max =  max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        luiken_vensters = st.number_input('Het aandeel van de productgroep Luiken en vensters', value = 0.0, min_value = 0.0, max_value = luiken_vensters_max,step = 0.1)
        
        balustrades_leuningen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                                 binnenkozijnen, luiken_vensters, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        balustrades_leuningen = st.number_input('Het aandeel van de productgroep Balustrades', value = 0.0, min_value = 0.0, max_value = balustrades_leuningen_max, step = 0.1)
        
        binnenwandafwerkingen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                                 binnenkozijnen, luiken_vensters, balustrades_leuningen, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        binnenwandafwerkingen = st.number_input('Het aandeel van de productgroep Binnenwandafwerkingen', value = 0.0, min_value = 0.0, max_value = binnenwandafwerkingen_max, step = 0.1)
        
        vloerafwerkingen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        vloerafwerkingen = st.number_input('Het aandeel van de productgroep Vloerafwerkingen', value = 0.0, min_value = 0.0, max_value = vloerafwerkingen_max, step = 0.1)
        
        plafonds_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, 
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        plafonds = st.number_input('Het aandeel van de productgroep Plafonds', value = 0.0, min_value = 0.0, max_value = plafonds_max, step = 0.1)
        
        na_isolatie_max =  max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        na_isolatie = st.number_input('Het aandeel van de productgroep Na-isolatie', value = 0.0, min_value = 0.0, max_value = na_isolatie_max, step = 0.1)
        
        riolering_hwa_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                        binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                         na_isolatie, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        riolering_hwa = st.number_input('Het aandeel van de productgroep Riolering en HWA', value = 0.0, min_value = 0.0, max_value = riolering_hwa_max, step = 0.1)
        
        water_installaties_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        water_installaties = st.number_input('Het aandeel van de productgroep Warm- en koud water installaties', value = 0.0, min_value = 0.0, max_value = water_installaties_max, step = 0.1)
        
        verwarming_koeling_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        verwarming_koeling = st.number_input('Het aandeel van de productgroep Verwarming en koeling', value = 0.0, min_value = 0.0, max_value = verwarming_koeling_max, step = 0.1)
    
        luchtbehandeling_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                            0.0, 0.0])
        luchtbehandeling = st.number_input('Het aandeel van de productgroep Luchtbehandeling', value = 0.0, min_value = 0.0, max_value = luchtbehandeling_max, step = 0.1)
        
        elektrische_installaties_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, 0.0, 0.0, 0.0, 0.0, 
                                            0.0, 0.0, 0.0])
        elektrische_installaties = st.number_input('Het aandeel van de productgroep Elektrische installaties', value = 0.0, min_value = 0.0, max_value = elektrische_installaties_max, step = 0.1)
        
        gebouwvoorzieningen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties,
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        gebouwvoorzieningen = st.number_input('Het aandeel van de productgroep Gebouwvoorzieningen', value = 0.0, min_value = 0.0, max_value = gebouwvoorzieningen_max, step = 0.1)
        
        beveiliging_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                        binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds,
                                       na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                        gebouwvoorzieningen, 0.0, 0.0, 0.0, 0.0, 0.0])
        beveiliging = st.number_input('Het aandeel van de productgroep Beveiliging', value = 0.0, min_value = 0.0, max_value = beveiliging_max, step = 0.1)
        
        lift_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, 
                                riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                gebouwvoorzieningen, beveiliging, 0.0, 0.0, 0.0, 0.0])
        lift = st.number_input('Het aandeel van de productgroep Lift', value = 0.0, min_value = 0.0, max_value = lift_max, step = 0.1)
        
        keuken_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                    binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, 
                                    riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                    gebouwvoorzieningen, beveiliging, lift, 0.0, 0.0, 0.0])
        keuken = st.number_input('Het aandeel van de productgroep Keuken', value = 0.0, min_value = 0.0, max_value = keuken_max, step = 0.1)
        
        sanitair_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                    binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, 
                                    riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                    gebouwvoorzieningen, beveiliging, lift, keuken, 0.0, 0.0])
        sanitair = st.number_input('Het aandeel van de productgroep Sanitair', value = 0.0, min_value = 0.0, max_value = sanitair_max, step = 0.1)
        
        terreininrichting_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                             na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                               gebouwvoorzieningen, beveiliging, lift, keuken, sanitair, 0.0])
        terreininrichting = st.number_input('Het aandeel van de productgroep Terreininrichting', value = 0.0, min_value = 0.0, max_value = terreininrichting_max+0.05, step = 0.1)


# In[ ]:


with tab2:
    if st.session_state.projectbestand is None:
        st.markdown("upload een bestand")
    else: 
        col1, col2 = st.columns(2)
    
        with col2:
            st.markdown("**aanpassing**")
            variabelen = [buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, binnenkozijnen, luiken_vensters, 
                          balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, riolering_hwa, water_installaties, 
                          verwarming_koeling, luchtbehandeling, elektrische_installaties, gebouwvoorzieningen, beveiliging, lift, keuken, sanitair, terreininrichting]
            productgroep = ['buitenwanden', 'binnenwanden', 'vloeren', 'trappen_hellingen', 'daken', 'hoofddraagconstructie', 'buitenkozijnen', 
                            'binnenkozijnen', 'luiken_vensters', 'balustrades_leuningen', 'binnenwandafwerkingen', 'vloerafwerkingen', 'plafonds', 
                            'na_isolatie', 'riolering_hwa', 'water_installaties', 'verwarming_koeling', 'luchtbehandeling', 
                            'elektrische_installaties', 'gebouwvoorzieningen', 'beveiliging', 'lift', 'keuken', 'sanitair', 'terreininrichting']
            for i in range(25):
                st.markdown(f"- {productgroep[i]}: {variabelen[i]}%")
            
            #Impact themas op productgroepen
            impact_duurzaamheid = [impact.iloc[a, 2] for a in range(len(impact))]
            duurzaamheid = sum([variabelen[i] * impact_duurzaamheid[i] for i in range(25)])
            st.markdown(f"score duurzaamheid: {duurzaamheid}")
            
            impact_prijs = [impact.iloc[a, 4] for a in range(len(impact))]
            prijs = sum([variabelen[i] * impact_prijs[i] for i in range(25)])
            st.markdown(f"score prijs: {prijs}")  
        
            impact_woonbeleving = [impact.iloc[a, 5] for a in range(len(impact))]
            woonbeleving = sum([variabelen[i] * impact_woonbeleving[i] for i in range(25)])
            st.markdown(f"score woonbeleving: {woonbeleving}")  
            
            impact_kwaliteit = [impact.iloc[a, 3] for a in range(len(impact))]
            kwaliteit = sum([variabelen[i] * impact_kwaliteit[i] for i in range(25)])
            st.markdown(f"score kwaliteit: {kwaliteit}")  
            
            impact_onderhoud = [impact.iloc[a, 1] for a in range(len(impact))]
            onderhoud = sum([variabelen[i] * impact_onderhoud[i] for i in range(25)])
            st.markdown(f"score onderhoud: {onderhoud}")  
    
        with col1:
            st.markdown("**optimalisatie**")
            for index, row in df.iterrows():
                st.markdown(f"- {row['Productgroep']}: {row['Waarde']}%")
            duurzaam2 = sum([df['Waarde'][i] * impact_duurzaamheid[i] for i in range(25)])
            prijs2 = sum([df['Waarde'][i] * impact_prijs[i] for i in range(25)])
            woonbeleving2 = sum([df['Waarde'][i] * impact_woonbeleving[i] for i in range(25)])
            kwaliteit2 = sum([df['Waarde'][i] * impact_kwaliteit[i] for i in range(25)])
            onderhoud2 = sum([df['Waarde'][i] * impact_onderhoud[i] for i in range(25)])
            st.markdown(f"score duurzaamheid: {duurzaam2/sum(impact_duurzaamheid)}")
            st.markdown(f"score prijs: {prijs2/sum(impact_prijs)}")
            st.markdown(f"score woonbeleving: {woonbeleving2/sum(impact_woonbeleving)}")
            st.markdown(f"score kwaliteit: {kwaliteit2/sum(impact_kwaliteit)}")
            st.markdown(f"score onderhoud: {onderhoud2/sum(impact_onderhoud)}")


# In[2]:


minimale = [15.5, 1.7, 12.0, 1.0, 2.3, 4.6, 13.7, 1.2, 0.1, 2.8, 0.4, 1.5, 1.4, 0, 0, 0, 0, 0, 0, 0.3, 0, 0, 1.7, 0, 0]
maximale = [35.0, 4.4, 21.6, 2.3, 6.1, 8.4, 18.0, 6.1, 0.2, 3.6, 3.5, 3.2, 2.5, 0, 5.6, 0, 5.6, 5.6, 9.0, 0.4, 0, 0, 1.8, 2.0, 0.1]
len(maximale)


# In[ ]:




