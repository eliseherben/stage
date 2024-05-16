#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pulp as pl


# In[ ]:


st.write("#")
st.title("Optimalisatie")
st.page_link("pages/advies.py", label="Naar advies")
st.page_link("simplex.py", label="Homepagina")


# In[ ]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
data.head()


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    budget = data.sort_values(by='kosten', ascending=False)
    
    st.markdown(
        f"""
        De productgroepen die het meeste impact maken op het thema 'budget':
        - {budget['productgroep'].iloc[0]}
        - {budget['productgroep'].iloc[1]}
        - {budget['productgroep'].iloc[2]}
        """
        )
    
    circulair = data.sort_values(by='circulair', ascending=False)

    st.markdown(
        f"""
        De productgroepen die het meeste impact maken op het thema 'circulair':
        - {circulair['productgroep'].iloc[0]}
        - {circulair['productgroep'].iloc[1]}
        - {circulair['productgroep'].iloc[2]}
        """
        )


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
# Creëer een LP probleem
    prob = pl.LpProblem("Eigen Haard", pl.LpMinimize)

    variabelen = {}
    for index, row in data.iterrows():
        variabelen[row["productgroep"]] = pl.LpVariable(row["productgroep"], lowBound = 0)

    lp_variabelen = []
    for key, value in variabelen.items():
#             st.markdown(f"{key} = {value}")
        lp_variabelen.append((key, value))

    #Impact themas op productgroepen
    impact_circulair = [data.iloc[a, 5] for a in range(len(data))]
    circulair = pl.lpSum(lp_variabelen[i][1] * impact_circulair[i] for i in range(25))

    impact_budget = [data.iloc[a, 4] for a in range(len(data))]
    budget = pl.lpSum(lp_variabelen[i][1] * impact_budget[i] for i in range(25))

    prob += circulair + budget

    for i in range(len(lp_variabelen)):
        st.markdown(f"{lp_variabelen[i][1]} >= {data.iloc[i, 2]}")
        st.markdown(f"{lp_variabelen[i][1]} >= {data.iloc[i, 3]}")
#         prob += lp_variabelen[i][1] >= data.iloc[i, 2]
#         prob += lp_variabelen[i][1] <= data.iloc[i, 3]

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

