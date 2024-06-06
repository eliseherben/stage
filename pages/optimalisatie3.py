#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import pulp as pl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[ ]:


st.write("#")
st.title("Optimalisatie")
st.page_link("simplex.py", label="Homepagina")


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
    
st.session_state._maximaal = st.session_state.maximaal

def set_maximaal():
    st.session_state.maximaal = st.session_state._maximaal
    
if 'oplossingen' not in st.session_state:
    st.session_state.oplossingen = None
    
st.session_state._oplossingen = st.session_state.oplossingen

def set_oplossingen():
    st.session_state.oplossingen = st.session_state._oplossingen
    
if "doelwaardes" not in st.session_state:
    st.session_state.doelwaardes = None
    
st.session_state._doelwaardes = st.session_state.doelwaardes

def set_doelwaardes():
    st.session_state.doelwaardes = st.session_state._doelwaardes


# In[ ]:


st.markdown("**Primair thema**")
st.markdown("De verschillende thema's krijgen in de optimalisatie een weging. Op basis van de keuze van het primaire thema zal de weging voor dit thema hoger liggen dan de weging voor het andere thema. Hiermee zal het primaire thema, met een hogere weging dus als belangrijker gezien worden in de optimalisatie. ")
st.selectbox("Wat heeft meer prioriteit binnen dit project?", 
            ("Minimale milieukosten", "Minimale afwijkingen van de huidge aantallen"), 
            index = None, 
            placeholder='Selecteer een thema...', key='_doelstelling', on_change=set_doelstelling)


# In[6]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
data['optimalisatie'] = data.apply(lambda row: 'nee' if row.isnull().any() else 'ja', axis=1)

data.iloc[-1, 3] = data.iloc[-1, 3] + 1


# In[7]:


data


# In[ ]:


data2 = pd.read_csv("dataframe2.csv", sep=';', decimal = ',')


# In[ ]:


data3 = pd.read_csv("dataframe3.csv", sep=';', decimal = ',')


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


# In[ ]:


# Filter de rijen waar geen NaN-waarden zijn in de specifieke kolommen
filtered_data = data.dropna(subset=['maximaal', 'kosten'])

# Maak een lijst van de waarden in de kolom 'minimaal' uit de gefilterde data
minimaal_list = filtered_data['minimaal'].tolist()
maximaal_list = filtered_data['maximaal'].tolist()

st.session_state.minimaal = minimaal_list
st.session_state.maximaal = maximaal_list


# In[ ]:


# filtered = data.dropna(subset=['minimaal', 'maximaal'])

# productgroepen = filtered['productgroep'].unique()
# selected_productgroepen = st.multiselect("Selecteer een productgroep", productgroepen)
# filtered_data = filtered[filtered['productgroep'].isin(selected_productgroepen)]

# fig = px.bar(filtered_data, x='kosten', y='constant', 
#                  color_discrete_sequence=['rgba(58, 71, 80, 0.1)'])
    
# fig.add_trace(px.scatter(filtered_data, x='kosten', y='constant', color='productgroep'))

# fig.update_yaxes(visible=False)


# st.plotly_chart(fig)


# In[ ]:


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

fig_kosten.update_layout(height=250)


st.plotly_chart(fig_kosten)


# In[ ]:


fig_circulair = px.scatter(filtered_data, x='circulair', y = ['constant'], color='productgroep')
fig_circulair.update_traces(marker_size=10, showlegend = False)

fig_circulair.update_yaxes(visible=False)

# Bepaal de minimum- en maximumwaarden voor de x-as
x_min = min(filtered['circulair']) - 10
x_max = max(filtered['circulair']) + 10

# Vastzetten van de x-as range
fig_circulair.update_xaxes(range=[0, 45])

fig_circulair.update_layout(height=250)

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

# In[ ]:


# Controleer of het projectbestand is geüpload
if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    st.markdown("**Minimale afwijking in productgroepen**")
    
    elements = [
    {"type": "21 Buitenwanden", "key_toggle": "Buitenwanden_on"},
    {"type": "22 Binnenwanden", "key_toggle": "Binnenwanden_on"},
    {"type": "23 Vloeren", "key_toggle": "Vloeren_on"},
    {"type": "24 Trappen en hellingen", "key_toggle": "Trappen_en_hellingen_on"},
    {"type": "27 Daken", "key_toggle": "Daken_on"},
    {"type": "28 Hoofddraagconstructie", "key_toggle": "Hoofddraagconstructie_on"},
    {"type": "31 Buitenkozijnen, -ramen, -deuren en -puien", "key_toggle": "Buitenkozijnen_on"},
    {"type": "32 Binnenkozijnen en -deuren", "key_toggle": "Binnenkozijnen_en__deuren_on"},
    {"type": "33 Luiken en vensters", "key_toggle": "Luiken_en_vensters_on"},
    {"type": "34 Balustrades en leuningen", "key_toggle": "Balustrades_en_leuningen_on"},
    {"type": "42 Binnenwandafwerkingen", "key_toggle": "Binnenwandafwerkingen_on"},
    {"type": "43 Vloerafwerkingen", "key_toggle": "Vloerafwerkingen_on"},
    {"type": "45 Plafonds", "key_toggle": "Plafonds_on"},
    {"type": "64 Vaste gebouwvoorziening","key_toggle": "Vaste_gebouwvoorziening_on"},
    {"type": "73 Keuken", "key_toggle": "Keuken_on"},
    {"type": "90 Terreininrichting", "key_toggle": "Terreininrichting_on"}
    ]
    
    for element in elements:
        if not st.session_state[element['key_toggle']]:
            for index, row in data.iterrows():
                if element['type'] == row['productgroep']:
                    data.at[index, 'optimalisatie'] = 'nee'

    data['code'] = data['productgroep'].str[:2]

    data['huidige_waarden'] = 0
    
    data['huidige_waarden'] = data.apply(
    lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['huidige_waarden'], axis=1
    )
    
    data.loc[data['productgroep'] == '48 Na-isolatie', 'huidige_waarden'] = 0
    
    data['minimaal'] = data.apply(
    lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['minimaal'], axis=1
    )
    
    data.loc[data['productgroep'] == '48 Na-isolatie', 'minimaal'] = 0
    
    data['maximaal'] = data.apply(
    lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['maximaal'], axis=1
    )

    data.loc[data['productgroep'] == '48 Na-isolatie', 'maximaal'] = 0
     
    huidigen = [
    {"type": "21 Buitenwanden", "key_input": "Buitenwanden"},
    {"type": "22 Binnenwanden", "key_input": "Binnenwanden"},
    {"type": "23 Vloeren", "key_input": "Vloeren"},
    {"type": "24 Trappen en hellingen", "key_input": "Trappen_en_hellingen"},
    {"type": "27 Daken", "key_input": "Daken"},
    {"type": "28 Hoofddraagconstructie", "key_input": "Hoofddraagconstructie"},
    {"type": "31 Buitenkozijnen, -ramen, -deuren en -puien", "key_input": "Buitenkozijnen"},
    {"type": "32 Binnenkozijnen en -deuren", "key_input": "Binnenkozijnen_en__deuren"},
    {"type": "33 Luiken en vensters", "key_input": "Luiken_en_vensters"},
    {"type": "34 Balustrades en leuningen", "key_input": "Balustrades_en_leuningen"},
    {"type": "42 Binnenwandafwerkingen", "key_input": "Binnenwandafwerkingen"},
    {"type": "43 Vloerafwerkingen", "key_input": "Vloerafwerkingen"},
    {"type": "45 Plafonds", "key_input": "Plafonds"},
    {"type": "64 Vaste gebouwvoorziening","key_input": "Vaste_gebouwvoorziening"},
    {"type": "73 Keuken", "key_input": "Keuken"},
    {"type": "90 Terreininrichting", "key_input": "Terreininrichting"}
    ]
    
    for huidige in huidigen:
        for index, row in data.iterrows():
            if huidige['type'] == row['productgroep']:
                data.at[index, 'huidige_waarden'] = st.session_state[huidige['key_input']]
    
    # Definieer de LP variabelen
    variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows() 
                  if row["optimalisatie"] == 'ja'}
    
    variabelen2 = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows() 
                   if row["optimalisatie"] == 'nee' and row["productgroep"] != '48 Na-isolatie'}
    
    st.markdown(variabelen2)
    st.markdown(len(variabelen2))
    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]
    lp_variabelen2 = lp_variabelen + [(key, value) for key, value in variabelen2.items()]

    lp_variabelen2.sort()
    st.markdown(lp_variabelen2)
    st.markdown(len(lp_variabelen2))
    
    dynamic_vars = {}
    afwijkingen_list = []
    doelwaardes = []
    
    for (key, var), i in zip(lp_variabelen, range(len(lp_variabelen))):
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
    
    if st.session_state.doelstelling == 'Minimale milieukosten':
        gewichten = [(1, 0), (0.9, 0.1), (0.8, 0.2), (0.7, 0.3), (0.6, 0.4)]  # Lijst van wegingen
    if st.session_state.doelstelling == 'Minimale afwijkingen van de huidge aantallen':
        gewichten = [(0, 1), (0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6)]  # Lijst van wegingen

    oplossingen = {}
    doelwaardes = []
    
    for w_circulair, w_afwijkingen in gewichten:
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen))]
        st.markdown(f"{variabelen_circulair} {len(variabelen_circulair)}")
        impact_circulair = [data.iloc[i, 5] for i in range(len(data)) if data.iloc[i, 6] == 'ja']
        st.markdown(f"{impact_circulair} {len(impact_circulair)}")
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        
        variabelen_budget = [lp_variabelen2[i][1] for i in range(len(lp_variabelen2))]
        impact_budget = [data.iloc[i, 4] for i in range(len(data)) if pd.notna(data.iloc[i, 4])]
        st.markdown(impact_budget)
        st.markdown(len(impact_budget))
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        st.markdown(budget)
        
        variabelen_milieukosten = [lp_variabelen2[i][1] for i in range(len(lp_variabelen2))]
        impact_milieukosten = [data.iloc[i, 5] for i in range(len(data)) if pd.notna(data.iloc[i, 4])]
        st.markdown(impact_milieukosten)
        st.markdown(len(variabelen_milieukosten))
        milieukosten = pl.lpSum(variabelen_milieukosten[i] * impact_milieukosten[i] for i in range(len(variabelen_milieukosten)))
        
#         impact_afwijkingen = [1/(data.iloc[i, 3] - data.iloc[i, 2]) for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4])]
#         afwijkingen2 = pl.lpSum(afwijkingen_list[i] * impact_afwijkingen[i] for i in range(len(impact_afwijkingen)))
        
        afwijkingen = pl.lpSum(afwijkingen_list)
        
        prob += w_circulair * circulair + w_afwijkingen * afwijkingen
        
        data2 = data[data['optimalisatie'] == 'ja']
        for i in range(len(lp_variabelen)):
            prob += lp_variabelen[i][1] >= data2.iloc[i, 2]
            prob += lp_variabelen[i][1] <= data2.iloc[i, 3]
        
#         lp_variabelen2 = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3])]
        
        for a in range(len(afwijkingen_list)):
            prob += afwijkingen_list[a] >= lp_variabelen[a][1] - startwaardes[a]
            prob += afwijkingen_list[a] >= startwaardes[a] - lp_variabelen[a][1]
        
        prob += budget == st.session_state.budget
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing met weging (circulair: {w_circulair}, afwijkingen: {w_afwijkingen}): {pl.LpStatus[status]}")
        st.markdown(f"milieukosten: {circulair.value()}")

        for name, constraint in prob.constraints.items():
            st.markdown(f"{name}: {constraint} = {constraint.value()}")
            
        # Sla de oplossing op in een dictionary
#         oplossingen[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] = [var.varValue for key, var in lp_variabelen]
#         oplossing_vars = [var.varValue for key, var in lp_variabelen]
        oplossingen[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] = [var.varValue for key, var in lp_variabelen]
        oplossingswaarden = list(oplossingen[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"])
        
        data[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] = None
        
        index = 0
        for i, row in data.iterrows():
            if row['optimalisatie'] == 'ja':
                if index < len(oplossingswaarden):
                    data.at[i, f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] = oplossingswaarden[index]
                    index += 1
            else:
                data.at[i, f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] = data.at[i, 'huidige_waarden']
        
        doelwaardes.append((f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}", 
                            (data[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] * data['kosten']).sum(), 
                            (data[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] * data['circulair']).sum()))

    doelwaardes.append(('minimaal', (data['minimaal'] * data['kosten']).sum(), (data['minimaal'] * data['circulair']).sum()))
    doelwaardes.append(('maximaal', (data['maximaal'] * data['kosten']).sum(), (data['maximaal'] * data['circulair']).sum()))
    doelwaardes.append(('huidige_waarden', (data['huidige_waarden'] * data['kosten']).sum(), (data['huidige_waarden'] * data['circulair']).sum()))

    st.dataframe(data)
    st.session_state.oplossingen = data
    st.session_state.doelwaardes = doelwaardes
    


# In[ ]:





# In[ ]:


st.page_link("pages/advies.py", label="Naar advies")
st.page_link("pages/visualisatie.py", label="Visualisatie oplossingen")


# maak er 1 dataframe van om te kunnen vergelijken

# In[ ]:


# if st.session_state.projectbestand is None:
#     st.markdown("upload een bestand")
# else: 
#     if st.session_state.doelstelling is not None:
#         st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")

#         df = pd.merge(df, data[['productgroep', 'eenheid']], on='productgroep')
        
#         for index, row in df.iterrows():
#             st.markdown(f"- Binnen de productgroep {row['productgroep']} moet er {row['waarde']} {row['eenheid']} besteed worden")


# In[6]:


[1, 2, 3] + [4, 7]


# In[ ]:




