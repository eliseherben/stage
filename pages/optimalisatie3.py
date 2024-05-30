#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import pulp as pl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[ ]:


st.write("#")
st.title("Optimalisatie")
st.page_link("pages/advies.py", label="Naar advies")
st.page_link("simplex.py", label="Homepagina")
st.page_link("pages/pareto_ga.py", label="Pareto oplossingen")


# In[ ]:


if "doelstelling" not in st.session_state:
    st.session_state.doelstelling = None
    
st.session_state._doelstelling = st.session_state.doelstelling

def set_doelstelling():
    st.session_state.doelstelling = st.session_state._doelstelling


# In[ ]:


st.markdown("**Primair thema**")
st.markdown("De verschillende thema's krijgen in de optimalisatie een weging. Op basis van de keuze van het primaire thema zal de weging voor dit thema hoger liggen dan de weging voor het andere thema. Hiermee zal het primaire thema, met een hogere weging dus als belangrijker gezien worden in de optimalisatie. ")
st.selectbox("Welke thema heeft prioriteit in dit project?", 
            ("Circulair", "Budget"), 
            index = None, 
            placeholder='selecteer een thema...', key='_doelstelling', on_change=set_doelstelling)


# In[3]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
data['woonbeleving'] = [0, 0, 0.25, 0.111, 0, 0, 0.029, 0.188, 0, 0, 0.385, 0.35, 0.25, 0, 0.053, 0.111, 0.091, 0.167, 0, 0.364, 0, 0, 0.2, 0, 0]
data.iloc[-1, 3] = data.iloc[-1, 3] + 1
data


# In[21]:


data2 = pd.read_csv("dataframe2.csv", sep=';', decimal = ',')


# In[5]:


data3 = pd.read_csv("dataframe3.csv", sep=';', decimal = ',')
data3


# In[ ]:


data3['minimaal'] = data3['minimaal'] * st.session_state.appartementen
data3['maximaal'] = data3['maximaal'] * st.session_state.appartementen
data3['constant'] = ['']*len(data3)


# In[ ]:


data2['minimaal'] = data2['minimaal'] * st.session_state.appartementen
data2['maximaal'] = data2['maximaal'] * st.session_state.appartementen
data2['constant'] = ['']*len(data2)


# In[ ]:


data['minimaal'] = data['minimaal'] * st.session_state.appartementen
data['maximaal'] = data['maximaal'] * st.session_state.appartementen
data['constant'] = ['']*len(data)


# In[9]:


filtered = data.dropna(subset=['minimaal', 'maximaal'])

productgroepen = filtered['productgroep'].unique()
selected_productgroepen = st.multiselect("Selecteer een productgroep", productgroepen)
filtered_data = filtered[filtered['productgroep'].isin(selected_productgroepen)]

fig_kosten = px.scatter(filtered_data, x='kosten', y = ['constant'], color='productgroep')
fig_kosten.update_traces(marker_size=10)

fig_kosten.update_yaxes(visible=False)

# Bepaal de minimum- en maximumwaarden voor de x-as
x_min = min(filtered['kosten']) - 100
x_max = max(filtered['kosten']) + 100

# Vastzetten van de x-as range
fig_kosten.update_xaxes(range=[x_min, x_max])

fig_kosten.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_kosten)


# In[ ]:


fig_circulair = px.scatter(filtered_data, x='circulair', y = ['constant'], color='productgroep')
fig_circulair.update_traces(marker_size=10, showlegend=False)

fig_circulair.update_yaxes(visible=False)

# Bepaal de minimum- en maximumwaarden voor de x-as
x_min = min(filtered['circulair']) - 10
x_max = max(filtered['circulair']) + 10

# Vastzetten van de x-as range
fig_circulair.update_xaxes(range=[x_min, x_max])

st.plotly_chart(fig_circulair)


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    budget = data.sort_values(by='kosten')
    
    st.markdown(
        f"""
        De productgroepen die het minste kosten per eenheid:
        - {budget['productgroep'].iloc[0]}
        - {budget['productgroep'].iloc[1]}
        - {budget['productgroep'].iloc[2]}
        """
        )
    
    circulair = data.sort_values(by='circulair')

    st.markdown(
        f"""
        De productgroepen die de laagste mki per eenheid hebben:
        - {circulair['productgroep'].iloc[0]}
        - {circulair['productgroep'].iloc[1]}
        - {circulair['productgroep'].iloc[2]}
        """
        )


# **mki**

# **levensduur**

# In[ ]:





# In[ ]:





# hieronder nog levensduur totaal genormaliseerd doen, met like mogelijke uitkomsten

# In[ ]:





# **minimale afwijking**

# minimale afwijking gewoon, genormaliseerd en genormaliseerd totaal

# In[ ]:





# In[ ]:


# Controleer of het projectbestand is geüpload
if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    st.markdown("**minimale afwijking genormaliseerd**")
    # Definieer de LP variabelen
    variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows()}

    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]
    st.markdown(lp_variabelen) 
    
    dynamic_vars = {}
    afwijkingen_list = []

    for (key, var), i in zip(lp_variabelen, range(len(lp_variabelen))):
        if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
            if var.name == "31_Buitenkozijnen,__ramen,__deuren_en__puien":
                var_name = (var.name.split("_")[1])[:-1] + '_start'
                dynamic_vars[var_name] = st.session_state[(var.name.split("_")[1])[:-1]]
                
                afwijkingen_var = pl.LpVariable('d_' + (var.name.split("_")[1])[:-1], lowBound = 0)
                afwijkingen_list.append(afwijkingen_var)
            else:
                var_name = var.name[3:] + '_start'
                dynamic_vars[var_name] = st.session_state[var.name[3:]]

                afwijkingen_var = pl.LpVariable('d_' + var.name[3:], lowBound = 0) 
                afwijkingen_list.append(afwijkingen_var)
                
    startwaardes = list(dynamic_vars.values())

    if st.session_state.doelstelling == 'Circulair':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
            
         # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        max_circulair = max(impact_circulair)
        min_circulair = min(impact_circulair)
        impact_circulair1 = [i-min_circulair for i in impact_circulair]
        circulair1 = pl.lpSum(variabelen_circulair[i] * impact_circulair1[i] for i in range(len(variabelen_circulair)))
        circulair_genormaliseerd = (circulair1) / (max_circulair - min_circulair)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        max_budget = max(impact_budget)
        min_budget = min(impact_budget)
        impact_budget1 = [i-min_budget for i in impact_budget]
        budget1 = pl.lpSum(variabelen_budget[i] * impact_budget1[i] for i in range(len(variabelen_budget)))
        budget_genormaliseerd = (budget1) / (max_budget - min_budget)
        st.markdown(budget_genormaliseerd)
        
        afwijkingen = pl.lpSum(afwijkingen_list)
        
        prob += 1/2 * circulair_genormaliseerd + 1/3 * budget_genormaliseerd + 1/6 * afwijkingen

        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data.iloc[i, 3]
        
        lp_variabelen2 = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3])]
        
        for a in range(len(afwijkingen_list)):
            prob += afwijkingen_list[a] >= lp_variabelen2[a] - startwaardes[a]
            prob += afwijkingen_list[a] >= startwaardes[a] - lp_variabelen2[a]
                
        prob += budget == st.session_state.budget
                        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (circulair): {prob.objective.value()}")
        st.markdown("\nRestricties met ingevulde waarden:")
        
        for name, constraint in prob.constraints.items():
            st.markdown(f"{name}: {constraint} = {constraint.value()}")
        
    if st.session_state.doelstelling == 'Budget':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
 
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        max_circulair = max(impact_circulair)
        min_circulair = min(impact_circulair)
        impact_circulair1 = [i-min_circulair for i in impact_circulair]
        circulair1 = pl.lpSum(variabelen_circulair[i] * impact_circulair1[i] for i in range(len(variabelen_circulair)))
        circulair_genormaliseerd = (circulair1) / (max_circulair - min_circulair)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        max_budget = max(impact_budget)
        min_budget = min(impact_budget)
        impact_budget1 = [i-min_budget for i in impact_budget]
        budget1 = pl.lpSum(variabelen_budget[i] * impact_budget1[i] for i in range(len(variabelen_budget)))
        budget_genormaliseerd = (budget1) / (max_budget - min_budget)
        
        afwijkingen = pl.lpSum(afwijkingen_list)
        
        prob += 1/3 * circulair_genormaliseerd + 1/2 * budget_genormaliseerd + 1/6 * afwijkingen
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data.iloc[i, 3]

        lp_variabelen2 = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3])]
        
        for a in range(len(afwijkingen_list)):
            prob += afwijkingen_list[a] >= lp_variabelen2[a] - startwaardes[a]
            prob += afwijkingen_list[a] >= startwaardes[a] - lp_variabelen2[a]
                
        prob += budget == st.session_state.budget
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (budget): {prob.objective.value()}")
        st.markdown("\nRestricties met ingevulde waarden:")
        for name, constraint in prob.constraints.items():
            st.markdown(f"{name}: {constraint} = {constraint.value()}")

    # Maak een DataFrame van de variabelen en hun waarden
    variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
    df = pd.DataFrame(variabelen_waarden, columns=['productgroep', 'waarde'])
    st.dataframe(df)

        
# # Afwijking in x1 en x2
# model += d_x1 >= x1 - x1_start
# model += d_x1 >= x1_start - x1
# model += d_x2 >= x2 - x2_start
# model += d_x2 >= x2_start - x2

# # Oplossen van het model
# model.solve()

# # Resultaten afdrukken
# print(f"x1: {x1.varValue}")
# print(f"x2: {x2.varValue}")
# print(f"d1_plus: {d1_plus.varValue}")
# print(f"d2_plus: {d2_plus.varValue}")
# print(f"d3_minus: {d3_minus.varValue}")
# print(f"d_x1: {d_x1.varValue}")
# print(f"d_x2: {d_x2.varValue}")
# print(f"Objective: {model.objective.value()}")


# In[ ]:


# Controleer of het projectbestand is geüpload
if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    st.markdown("**minimale afwijking genormaliseerd met kosten afwijking**")
    # Definieer de LP variabelen
    variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows()}

    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]
    st.markdown(lp_variabelen) 
    
    dynamic_vars = {}
    afwijkingen_list = []

    d_pos = pl.LpVariable("d_pos", lowBound = 0)
#     d_neg = pl.LpVariable("d_neg", lowBound = 0)

    for (key, var), i in zip(lp_variabelen, range(len(lp_variabelen))):
        if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
            if var.name == "31_Buitenkozijnen,__ramen,__deuren_en__puien":
                var_name = (var.name.split("_")[1])[:-1] + '_start'
                dynamic_vars[var_name] = st.session_state[(var.name.split("_")[1])[:-1]]
                
                afwijkingen_var = pl.LpVariable('d_' + (var.name.split("_")[1])[:-1], lowBound = 0)
                afwijkingen_list.append(afwijkingen_var)
            else:
                var_name = var.name[3:] + '_start'
                dynamic_vars[var_name] = st.session_state[var.name[3:]]

                afwijkingen_var = pl.LpVariable('d_' + var.name[3:], lowBound = 0) 
                afwijkingen_list.append(afwijkingen_var)
                
    startwaardes = list(dynamic_vars.values())

    if st.session_state.doelstelling == 'Circulair':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
            
         # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        max_circulair = max(impact_circulair)
        min_circulair = min(impact_circulair)
        impact_circulair1 = [i-min_circulair for i in impact_circulair]
        circulair1 = pl.lpSum(variabelen_circulair[i] * impact_circulair1[i] for i in range(len(variabelen_circulair)))
        circulair_genormaliseerd = (circulair1) / (max_circulair - min_circulair)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
#         max_budget = max(impact_budget)
#         min_budget = min(impact_budget)
#         impact_budget1 = [i-min_budget for i in impact_budget]
#         budget1 = pl.lpSum(variabelen_budget[i] * impact_budget1[i] for i in range(len(variabelen_budget)))
#         budget_genormaliseerd = (budget1) / (max_budget - min_budget)
#         st.markdown(budget_genormaliseerd)
        impact_afwijkingen = [1/(data.iloc[i, 3] - data.iloc[i, 2]) for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4])]
        afwijkingen = pl.lpSum(afwijkingen_list[i] * impact_afwijkingen[i] for i in range(len(impact_afwijkingen)))
    
        budget2 = 1 / 300000
        d_pos_n = pl.lpSum(d_pos * budget2)
#         d_neg_n = pl.lpSum(d_neg * budget2)

        
        prob += 1/2 * circulair_genormaliseerd + 1/3 * d_pos_n + 1/6 * afwijkingen

        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data.iloc[i, 3]
        
        lp_variabelen2 = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3])]
        
        for a in range(len(afwijkingen_list)):
            prob += afwijkingen_list[a] >= lp_variabelen2[a] - startwaardes[a]
            prob += afwijkingen_list[a] >= startwaardes[a] - lp_variabelen2[a]
            
        prob += d_pos >= st.session_state.budget - budget
        prob += d_pos >= budget - st.session_state.budget
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (circulair): {prob.objective.value()}")
        st.markdown("\nRestricties met ingevulde waarden:")
        for name, constraint in prob.constraints.items():
            st.markdown(f"{name}: {constraint} = {constraint.value()}")
        st.markdown(d_pos.value())

    if st.session_state.doelstelling == 'Budget':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
 
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        max_circulair = max(impact_circulair)
        min_circulair = min(impact_circulair)
        impact_circulair1 = [i-min_circulair for i in impact_circulair]
        circulair1 = pl.lpSum(variabelen_circulair[i] * impact_circulair1[i] for i in range(len(variabelen_circulair)))
        circulair_genormaliseerd = (circulair1) / (max_circulair - min_circulair)
        st.markdown(circulair_genormaliseerd)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
#         max_budget = max(impact_budget)
#         min_budget = min(impact_budget)
#         impact_budget1 = [i-min_budget for i in impact_budget]
#         budget1 = pl.lpSum(variabelen_budget[i] * impact_budget1[i] for i in range(len(variabelen_budget)))
#         budget_genormaliseerd = (budget1) / (max_budget - min_budget)
        
        impact_afwijkingen = [1/(data.iloc[i, 3] - data.iloc[i, 2]) for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4])]
        afwijkingen = pl.lpSum(afwijkingen_list[i] * impact_afwijkingen[i] for i in range(len(impact_afwijkingen)))
            
        budget2 = 1 / 300000
        d_pos_n = pl.lpSum(d_pos * budget2)
#         d_neg_n = pl.lpSum(d_neg * budget2)

        prob += 1/3 * circulair_genormaliseerd + 1/2 * d_pos_n + 1/6 * afwijkingen
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data.iloc[i, 3]

        lp_variabelen2 = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3])]
        
        for a in range(len(afwijkingen_list)):
            prob += afwijkingen_list[a] >= lp_variabelen2[a] - startwaardes[a]
            prob += afwijkingen_list[a] >= startwaardes[a] - lp_variabelen2[a]
                
        prob += d_pos >= st.session_state.budget - budget
        prob += d_pos >= budget - st.session_state.budget
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (budget): {prob.objective.value()}")
        st.markdown("\nRestricties met ingevulde waarden:")
        for name, constraint in prob.constraints.items():
            st.markdown(f"{name}: {constraint} = {constraint.value()}")

        st.markdown(d_pos.value())

    # Maak een DataFrame van de variabelen en hun waarden
    variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
    df = pd.DataFrame(variabelen_waarden, columns=['productgroep', 'waarde'])
    st.dataframe(df)

        
# # Afwijking in x1 en x2
# model += d_x1 >= x1 - x1_start
# model += d_x1 >= x1_start - x1
# model += d_x2 >= x2 - x2_start
# model += d_x2 >= x2_start - x2

# # Oplossen van het model
# model.solve()

# # Resultaten afdrukken
# print(f"x1: {x1.varValue}")
# print(f"x2: {x2.varValue}")
# print(f"d1_plus: {d1_plus.varValue}")
# print(f"d2_plus: {d2_plus.varValue}")
# print(f"d3_minus: {d3_minus.varValue}")
# print(f"d_x1: {d_x1.varValue}")
# print(f"d_x2: {d_x2.varValue}")
# print(f"Objective: {model.objective.value()}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# maak er 1 dataframe van om te kunnen vergelijken

# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    if st.session_state.doelstelling is not None:
        st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")

        df = pd.merge(df, data[['productgroep', 'eenheid']], on='productgroep')
        
        for index, row in df.iterrows():
            st.markdown(f"- Binnen de productgroep {row['productgroep']} moet er {row['waarde']} {row['eenheid']} besteed worden")

