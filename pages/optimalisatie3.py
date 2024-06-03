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
    
if 'startwaardes' not in st.session_state:
    st.session_state.startwaardes = None
    
st.session_state._startwaardes = st.session_state.startwaardes

def set_startwaardes():
    st.session_state.startwaardes = st.session_state._startwaardes
    
if 'lp_variabelen' not in st.session_state:
    st.session_state.lp_variabelen = None
    
st.session_state._lp_variabelen = st.session_state.lp_variabelen

def set_lp_variabelen():
    st.session_state.lp_variabelen = st.session_state._lp_variabelen
    
if 'minimaal' not in st.session_state:
    st.session_state.minimaal = None
    
st.session_state._minimaal = st.session_state.minimaal

def set_minimaal():
    st.session_state.minimaal = st.session_state._minimaal
    
if 'maximaal' not in st.session_state:
    st.session_state.maximaal = None
    
st.session_state.set_maximaal = st.session_state.maximaal

def set_maximaal():
    st.session_state.maximaal = st.session_state.set_maximaal


# In[ ]:


st.markdown("**Primair thema**")
st.markdown("De verschillende thema's krijgen in de optimalisatie een weging. Op basis van de keuze van het primaire thema zal de weging voor dit thema hoger liggen dan de weging voor het andere thema. Hiermee zal het primaire thema, met een hogere weging dus als belangrijker gezien worden in de optimalisatie. ")
st.selectbox("Wat heeft meer prioriteit binnen dit project?", 
            ("Minimale milieukosten indicator", "Minimale afwijkingen van de huidge aantallen"), 
            index = None, 
            placeholder='selecteer een thema...', key='_doelstelling', on_change=set_doelstelling)


# In[3]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
data['woonbeleving'] = [0, 0, 0.25, 0.111, 0, 0, 0.029, 0.188, 0, 0, 0.385, 0.35, 0.25, 0, 0.053, 0.111, 0.091, 0.167, 0, 0.364, 0, 0, 0.2, 0, 0]
data.iloc[-1, 3] = data.iloc[-1, 3] + 1


# In[21]:


data2 = pd.read_csv("dataframe2.csv", sep=';', decimal = ',')


# In[5]:


data3 = pd.read_csv("dataframe3.csv", sep=';', decimal = ',')


# In[ ]:


data3['minimaal'] = data3['minimaal'] * st.session_state.appartementen
data3['maximaal'] = data3['maximaal'] * st.session_state.appartementen
data3['constant'] = ['']*len(data3)


# In[ ]:


data2['minimaal'] = data2['minimaal'] * st.session_state.appartementen
data2['maximaal'] = data2['maximaal'] * st.session_state.appartementen
data2['constant'] = ['']*len(data2)


# In[4]:


data['minimaal'] = data['minimaal'] * st.session_state.appartementen
data['maximaal'] = data['maximaal'] * st.session_state.appartementen
data['constant'] = ['']*len(data)


# In[8]:


list(data['minimaal'] if pd.notna(data['minimaal']) and pd.notna(data['maximaal']) and pd.notna(data['kosten']) and pd.notna(data['circulair']))


# In[10]:


# Filter de rijen waar geen NaN-waarden zijn in de specifieke kolommen
filtered_data = data.dropna(subset=['maximaal', 'kosten', 'circulair'])

# Maak een lijst van de waarden in de kolom 'minimaal' uit de gefilterde data
minimaal_list = filtered_data['minimaal'].tolist()
maximaal_list = filtered_data['maximaal'].tolist()

st.session_state.minimaal = minimaal_list
st.session_state.maximaal = maximaal_list


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


# **minimale afwijking**

# minimale afwijking gewoon, genormaliseerd en genormaliseerd totaal

# In[ ]:


# Controleer of het projectbestand is geüpload
if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    st.markdown("**Minimale afwijking in productgroepen**")
    # Definieer de LP variabelen
    variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows()}

    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]
    
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
    st.session_state.startwaardes = startwaardes
    
    if st.session_state.doelstelling == 'Minimale milieukosten indicator':
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
        afwijkingen2 = pl.lpSum(afwijkingen_list[i] * impact_afwijkingen[i] for i in range(len(impact_afwijkingen)))

        afwijkingen = pl.lpSum(afwijkingen_list)
        
        prob +=  circulair 

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
        st.markdown(f"milieukosten: {circulair.value()}")
        st.markdown("Afwijkingen")
        for var in afwijkingen_list:
            st.markdown(f"{var.name}: {pl.value(var)}")

    if st.session_state.doelstelling == 'Minimale afwijkingen van de huidge aantallen':
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
#         max_budget = max(impact_budget)
#         min_budget = min(impact_budget)
#         impact_budget1 = [i-min_budget for i in impact_budget]
#         budget1 = pl.lpSum(variabelen_budget[i] * impact_budget1[i] for i in range(len(variabelen_budget)))
#         budget_genormaliseerd = (budget1) / (max_budget - min_budget)
        
        impact_afwijkingen = [1/(data.iloc[i, 3] - data.iloc[i, 2]) for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4])]
        afwijkingen2 = pl.lpSum(afwijkingen_list[i] * impact_afwijkingen[i] for i in range(len(impact_afwijkingen)))
            
        afwijkingen = pl.lpSum(afwijkingen_list)
            
        prob += afwijkingen
        
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
        st.markdown(f"milieukosten: {circulair.value()}")
        st.markdown("Afwijkingen")
        for var in afwijkingen_list:
            st.markdown(f"{var.name}: {pl.value(var)}")

    # Maak een DataFrame van de variabelen en hun waarden
    variabelen = [var.varValue for key, var in lp_variabelen]
    st.session_state.lp_variabelen = variabelen
    
    variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
    df = pd.DataFrame(variabelen_waarden, columns=['productgroep', 'waarde'])
    st.dataframe(df)


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

