#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import pulp as pl


# In[ ]:


st.write("#")
st.title("Optimalisatie")
st.page_link("pages/advies.py", label="Naar advies")
st.page_link("simplex.py", label="Homepagina")


# In[3]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
missing_values = data.isna()

print(missing_values)

# data.head()


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
    variabelen_circulair = []
    impact_circulair = []
    for i in range(len(lp_variabelen)):
        if not pd.isna(data.iloc[i, 5]):
            variabelen_circulair.append(lp_variabelen[i][1])
            impact_circulair.append(data.iloc[i, 5])

    circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
    st.markdown(circulair)

    variabelen_budget = []
    impact_budget = []
    for i in range(len(lp_variabelen)):
        if not pd.isna(data.iloc[i, 4]):
            variabelen_budget.append(lp_variabelen[i][1])
            impact_budget.append(data.iloc[i, 4])
    
    budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
    st.markdown(budget)

#     for i in range(len(lp_variabelen)):
#         if pd.isna(data.iloc[i, 2]) and pd.isna(data.iloc[i, 3]):
    
    prob += circulair + budget

    for i in range(len(lp_variabelen)):
        if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
            prob += lp_variabelen[i][1] >= data.iloc[i, 2]
            prob += lp_variabelen[i][1] <= data.iloc[i, 3]

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


f st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")

    for index, row in df.iterrows():
        st.markdown(f"- De productgroep {row['Productgroep']} is {row['Waarde']}% van het totale project")

    fig1 = px.pie(values=df['Waarde'], names=df['Productgroep'], color_discrete_sequence=px.colors.sequential.RdBu)
#         fig1.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig1)
