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


st.write("#")
st.title("Optimalisatie")
st.page_link("pages/advies.py", label="Naar advies")
st.page_link("simplex.py", label="Homepagina")


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    #barplot
#         st.dataframe(st.session_state.file, hide_index = True)
    df_fig = pd.melt(st.session_state.file, id_vars=['productgroep'], var_name='Optie', value_name='impact')

    df_fig = df_fig[df_fig['impact'] != 0]

    fig = px.bar(df_fig, x='productgroep', y='impact', color='Optie',
         barmode='group', title="Impact thema's op productgroepen")
#         st.plotly_chart(fig)

    with st.expander("oude impact cijfers"):
#         st.dataframe(st.session_state.file, hide_index = True)
        df_fig2 = pd.melt(st.session_state.file2, id_vars=['productgroep'], var_name='Optie', value_name='impact')

        df_fig2 = df_fig2[df_fig2['impact'] != 0]

        fig2 = px.bar(df_fig2, x='productgroep', y='impact', color='Optie',
             barmode='group', title="Impact thema's op productgroepen 2")
#             st.plotly_chart(fig2)

    st.write("#")

    st.markdown("**Rangschikken**")
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
#         st.dataframe(ranking_df)
#         st.dataframe(weights_df)

    rs_budget = weights_df['rank sum (RS)'].iloc[0]
    rs_circulariteit = weights_df['rank sum (RS)'].iloc[1]
    rs_kwaliteit = weights_df['rank sum (RS)'].iloc[2]
    rs_onderhoud = weights_df['rank sum (RS)'].iloc[3]
    rs_woonbeleving = weights_df['rank sum (RS)'].iloc[4]

    impact = st.session_state.file
#         st.dataframe(impact)

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


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
# Creëer een LP probleem
    prob = pl.LpProblem("Eigen Haard", pl.LpMaximize)

    variabelen = {}
    for index, row in df.iterrows():
        variabelen[row["productgroep"]] = pl.LpVariable(row["productgroep"], lowBound = 0)

    lp_variabelen = []
    for key, value in variabelen.items():
#             st.markdown(f"{key} = {value}")
        lp_variabelen.append((key, value))

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

    prob += rs_circulariteit * circulair - rs_budget * budget + rs_woonbeleving * woonbeleving + rs_kwaliteit * kwaliteit - rs_onderhoud * onderhoud

    # Voeg beperkingen toe (voorbeeldbeperkingen)
    prob += sum(t[1] for t in lp_variabelen) == 100

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
        prob += lp_variabelen[i][1] >= minimale[i]
        prob += lp_variabelen[i][1] <= maximale[i]

    # Los het probleem op
    status = prob.solve()

    # Maak een lege lijst om de variabelen en hun waarden op te slaan
    variabelen_waarden = []

    # Voeg de variabelen en hun waarden toe aan de lijst
    for key, var in lp_variabelen:
        variabelen_waarden.append((key, var.varValue))

    # Maak een DataFrame van de lijst
    df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])

    st.markdown(f"Status van de oplossing: {pl.LpStatus[status]}")
    st.markdown(f"Waarde van de doelfunctie: {prob.objective.value()}")


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")

    for index, row in df.iterrows():
        st.markdown(f"- De productgroep {row['Productgroep']} is {row['Waarde']}% van het totale project")

    fig1 = px.pie(values=df['Waarde'], names=df['Productgroep'], color_discrete_sequence=px.colors.sequential.RdBu)
#         fig1.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig1)


# In[ ]:




