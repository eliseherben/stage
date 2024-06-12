#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
st.page_link("pages/input.py", label = "Terug naar input")


# In[ ]:


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


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
data['optimalisatie'] = data.apply(lambda row: 'nee' if row.isnull().any() else 'ja', axis=1)
data.iloc[-1, 3] = data.iloc[-1, 3] + 1


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


st.markdown("##### Verdeling productgroepen")
filtered = data.dropna(subset=['minimaal', 'maximaal'])

opties = st.selectbox("Soort visualisatie", 
                         ["Alleen de productgroepen met m2 als eenheid", 
                          "Alleen de productgroepen met stuks als eenheid", "Alle productgroepen"], index = None, 
                      placeholder = 'Kies een visualisatie')

if opties == "Alleen de productgroepen met m2 als eenheid":
    filtered = filtered[filtered['eenheid'] == 'm2']
if opties == "Alleen de productgroepen met stuks als eenheid":
    filtered = filtered[filtered['eenheid'] == 'stuks']


productgroepen = filtered['productgroep'].unique()
selected_productgroepen = st.multiselect("Selecteer een productgroep", productgroepen, 
                                         placeholder = 'Selecteer productgroep(en)')
filtered_data = filtered[filtered['productgroep'].isin(selected_productgroepen)]

result_kosten = filtered_data[['productgroep', 'kosten']]
result_kosten = result_kosten.transpose()
result_kosten.columns = result_kosten.iloc[0]
result_kosten = result_kosten[1:]
result_kosten.insert(0, 'minimaal', min(filtered['kosten']))
result_kosten.insert(1, 'maximaal', max(filtered['kosten']))
result_kosten.insert(2, 'code', '01')
result_kosten['Kosten per eenheid'] = result_kosten['maximaal'] - result_kosten['minimaal']

# Voorbeeld lijst met kleuren
kleuren_schema = [
    'rgba(212, 0, 60, 1.0)',
    'rgba(241, 142, 47, 1.0)', 
    'rgba(255, 211, 0, 1.0)',
    'rgba(0, 158, 224, 1.0)', 
    'rgba(151, 191, 13, 1.0)', 
    'rgba(147, 16, 126, 1.0)',  
    'rgba(119, 118, 121, 1.0)' 
]

fig_kosten = px.bar(result_kosten, x='Kosten per eenheid', y = 'code', base = 'minimaal', 
                    color_discrete_sequence=['rgba(119, 118, 121, 0.1)'])

kleur_teller = 0
# fig_kosten.update_traces(marker_size=20)
for i in range(len(selected_productgroepen)):
    if result_kosten.columns[i+3] in selected_productgroepen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        fig_kosten.add_trace(px.scatter(result_kosten, x=result_kosten.columns[i+3], y='code', 
                                     color_discrete_sequence=[kleur], labels={'x': ''}, 
                                     size=[10], symbol = [result_kosten.columns[i+3]]).data[0])

fig_kosten.update_yaxes(visible=False)

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


if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    result_milieukosten = filtered_data[['productgroep', 'circulair']]
    result_milieukosten = result_milieukosten.transpose()
    result_milieukosten.columns = result_milieukosten.iloc[0]
    result_milieukosten = result_milieukosten[1:]
    result_milieukosten.insert(0, 'minimaal', min(filtered['circulair']))
    result_milieukosten.insert(1, 'maximaal', max(filtered['circulair']))
    result_milieukosten.insert(2, 'code', '02')
    result_milieukosten['Milieukosten per eenheid'] = result_milieukosten['maximaal'] - result_milieukosten['minimaal']

    # Voorbeeld lijst met kleuren
    kleuren_schema = [
        'rgba(212, 0, 60, 1.0)',
        'rgba(241, 142, 47, 1.0)', 
        'rgba(255, 211, 0, 1.0)',
        'rgba(0, 158, 224, 1.0)', 
        'rgba(151, 191, 13, 1.0)', 
        'rgba(147, 16, 126, 1.0)',  
        'rgba(119, 118, 121, 1.0)' 
    ]

    fig_circulair = px.bar(result_milieukosten, x='Milieukosten per eenheid', y = 'code', base = 'minimaal', 
                        color_discrete_sequence=['rgba(119, 118, 121, 0.1)'])

    kleur_teller = 0
    # fig_kosten.update_traces(marker_size=20)
    for i in range(len(selected_productgroepen)):
        if result_milieukosten.columns[i+3] in selected_productgroepen:
            kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
            kleur_teller += 1
            fig_circulair.add_trace(px.scatter(result_milieukosten, x=result_milieukosten.columns[i+3], y='code', 
                                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                                         size=[10], symbol = [result_milieukosten.columns[i+3]]).data[0])

    fig_circulair.update_yaxes(visible=False)

    fig_circulair.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig_circulair.update_layout(height=250)

    st.plotly_chart(fig_circulair)


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    st.markdown("#")
    col1, col2 = st.columns(2)
    with col1:
        budget = data.sort_values(by='kosten')

        st.markdown(
            f"""
            Minste kosten per eenheid:
            - {budget['productgroep'].iloc[0]}
            - {budget['productgroep'].iloc[1]}
            - {budget['productgroep'].iloc[2]}
            """
            )
    
    with col2:
        circulair = data.sort_values(by='circulair')

        st.markdown(
            f"""
            Laagste milieukosten per eenheid:
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
    st.markdown("#")
    st.markdown("##### Minimale afwijking in productgroepen")
    
    for i in range(len(data)):
        if data.iloc[i, 0][:2] not in st.session_state.list:
            data.drop(index = i, inplace = True)
    
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
    
    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]
    lp_variabelen2 = [(key, value) for key, value in variabelen2.items()]
    lp_variabelen3 = lp_variabelen + [(key, value) for key, value in variabelen2.items()]

    lp_variabelen3.sort()
    
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
    if st.session_state.doelstelling == 'Geen voorkeur':
        gewichten = [(0, 1), (0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6), (0.5, 0.5), 
                     (0.6, 0.4), (0.7, 0.3), (0.8, 0.2), (0.9, 0.1), (1, 0)]

    oplossingen = {}
    doelwaardes = []
    
    for w_circulair, w_afwijkingen in gewichten:
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen))]
        impact_circulair = [data.iloc[i, 5] for i in range(len(data)) if data.iloc[i, 6] == 'ja']
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        
        variabelen_budget = [lp_variabelen3[i][1] for i in range(len(lp_variabelen3))]
        impact_budget = [data.iloc[i, 4] for i in range(len(data)) if pd.notna(data.iloc[i, 4])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        
        variabelen_milieukosten = [lp_variabelen3[i][1] for i in range(len(lp_variabelen3))]
        impact_milieukosten = [data.iloc[i, 5] for i in range(len(data)) if pd.notna(data.iloc[i, 4])]
        milieukosten = pl.lpSum(variabelen_milieukosten[i] * impact_milieukosten[i] for i in range(len(variabelen_milieukosten)))
            
        afwijkingen = pl.lpSum(afwijkingen_list)
        
        prob += w_circulair * circulair + w_afwijkingen * afwijkingen
        
        data2 = data[data['optimalisatie'] == 'ja']
        data2 = data2.reset_index(drop=True)
        for i in range(len(lp_variabelen)):
            prob += lp_variabelen[i][1] >= data2.iloc[i, 2]
            prob += lp_variabelen[i][1] <= data2.iloc[i, 3]
                
        for a in range(len(afwijkingen_list)):
            prob += afwijkingen_list[a] >= lp_variabelen[a][1] - startwaardes[a]
            prob += afwijkingen_list[a] >= startwaardes[a] - lp_variabelen[a][1]
        
        data3 = data[data['optimalisatie'] == 'nee']
        data3 = data3[data3['productgroep'] != '48 Na-isolatie']
        data3 = data3.reset_index(drop=True)
        for i in range(len(lp_variabelen2)):
            prob += lp_variabelen2[i][1] == data3.iloc[i, 9]
        
        prob += budget == st.session_state.budget
        
        status = prob.solve()

        oplossingen[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] = [var.varValue for key, var in lp_variabelen]
        oplossingswaarden = list(oplossingen[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"])

        data[f"circulair_{w_circulair}_afwijkingen_{w_afwijkingen}"] = None
        if pl.LpStatus[status] == 'Optimal':
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

    kolommen_uitsluiten = ['minimaal', 'maximaal', 'kosten', 'circulair', 'optimalisatie', 'constant', 'code']
    uitkomsten = data.drop(columns=kolommen_uitsluiten)
    uitkomsten[uitkomsten.columns[3:]] = uitkomsten[uitkomsten.columns[3:]].apply(pd.to_numeric)
    uitkomsten = uitkomsten.round(1) 
    
    columns = uitkomsten.columns.tolist()
    for i in range(len(uitkomsten)):
        columns[i+3] = f'Oplossing {1+1}'
    
    st.dataframe(uitkomsten, hide_index = True)
    st.session_state.oplossingen = data
    st.session_state.doelwaardes = doelwaardes
    


# In[ ]:


st.markdown('#')
st.markdown("##### Visualisaties")
df = st.session_state.oplossingen
    
kolommen_te_uitsluiten = ['eenheid', 'kosten', 'circulair', 'optimalisatie', 
                          'constant', 'productgroep', 'code', 'minimaal', 'maximaal']
kolommen_te_selecteren = [kolom for kolom in df.columns if kolom not in kolommen_te_uitsluiten]
geselecteerde_kolommen = st.multiselect('Selecteer oplossingen', kolommen_te_selecteren)

df = df[df['eenheid'].notna()]

df['minimaal'] = pd.to_numeric(df['minimaal'])
df['maximaal'] = pd.to_numeric(df['maximaal'])
df['minimaal'] = df['minimaal'].round(1)
df['maximaal'] = df['maximaal'].round(1)

for productgroep in df['productgroep']:
    kleur_teller = 0
    # Selecteer de data voor de huidige productgroep
    df_productgroep = df[df['productgroep'] == productgroep]

    # Selecteer alle kolommen behalve de uitgesloten kolommen
    df_geselecteerd = df_productgroep.drop(columns=kolommen_te_uitsluiten)

    df_productgroep['aantal'] = df_productgroep['maximaal'] - df_productgroep['minimaal']

    fig = px.bar(df_productgroep, x='aantal', y='code', base = 'minimaal', 
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title=f'{productgroep} ',
                hover_data = {'minimaal': True, 'maximaal': True, 'code': False, 'aantal': False})
    
    bar_hovertemplate = 'Minimaal: %{customdata[0]} %{customdata[2]}<br>Maximaal: %{customdata[1]} %{customdata[2]}<br>'
    fig.update_traces(hovertemplate=bar_hovertemplate, customdata=df_productgroep[['minimaal', 'maximaal', 'eenheid']].values)

    if df_productgroep.columns[9] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_productgroep, x='huidige_waarden', y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['huidig'])
        
        scatter_hovertemplate = f'Huidige waarde: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig.add_trace(scatter.data[0])
    
    if df_productgroep.columns[10] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_productgroep, x=df_productgroep.columns[10], y='code', 
                                 color_discrete_sequence=[kleur], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 1'])
        
        scatter_hovertemplate = f'Oplossing 1: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig.add_trace(scatter.data[0])

    if df_productgroep.columns[11] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_productgroep, x=df_productgroep.columns[11], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 2'])
        
        scatter_hovertemplate = f'Oplossing 2: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig.add_trace(scatter.data[0])

    if df_productgroep.columns[12] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_productgroep, x=df_productgroep.columns[12], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 3'])
    
        scatter_hovertemplate = f'Oplossing 3: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig.add_trace(scatter.data[0])

    if df_productgroep.columns[13] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_productgroep, x=df_productgroep.columns[13], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 4'])
        
        scatter_hovertemplate = f'Oplossing 4: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig.add_trace(scatter.data[0])

    if df_productgroep.columns[14] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_productgroep, x=df_productgroep.columns[14], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 5'])
        
        scatter_hovertemplate = f'Oplossing 5: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig.add_trace(scatter.data[0])

    if st.session_state.doelstelling == 'Geen voorkeur':
        if df_productgroep.columns[15] in geselecteerde_kolommen:
            kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
            kleur_teller += 1
            scatter = px.scatter(df_productgroep, x=df_productgroep.columns[15], y='code', 
                                 color_discrete_sequence=[kleur], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 6'])
            
            scatter_hovertemplate = f'Oplossing 6: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
            scatter.update_traces(hovertemplate=scatter_hovertemplate)
            fig.add_trace(scatter.data[0])

        if df_productgroep.columns[16] in geselecteerde_kolommen:
            kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
            kleur_teller += 1
            scatter = px.scatter(df_productgroep, x=df_productgroep.columns[16], y='code', 
                                 color_discrete_sequence=[kleur], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 7'])
            
            scatter_hovertemplate = f'Oplossing 7: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
            scatter.update_traces(hovertemplate=scatter_hovertemplate)
            fig.add_trace(scatter.data[0])

        if df_productgroep.columns[17] in geselecteerde_kolommen:
            kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
            kleur_teller += 1
            scatter = px.scatter(df_productgroep, x=df_productgroep.columns[17], y='code', 
                                 color_discrete_sequence=[kleur], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 8'])
            
            scatter_hovertemplate = f'Oplossing 8: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
            scatter.update_traces(hovertemplate=scatter_hovertemplate)
            fig.add_trace(scatter.data[0])

        if df_productgroep.columns[18] in geselecteerde_kolommen:
            kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
            kleur_teller += 1
            scatter = px.scatter(df_productgroep, x=df_productgroep.columns[18], y='code', 
                                 color_discrete_sequence=[kleur], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 9'])
            
            scatter_hovertemplate = f'Oplossing 9: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
            scatter.update_traces(hovertemplate=scatter_hovertemplate)
            fig.add_trace(scatter.data[0])

        if df_productgroep.columns[19] in geselecteerde_kolommen:
            kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
            kleur_teller += 1
            scatter = px.scatter(df_productgroep, x=df_productgroep.columns[19], y='code', 
                                 color_discrete_sequence=[kleur], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 10'])
            
            scatter_hovertemplate = f'Oplossing 10: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
            scatter.update_traces(hovertemplate=scatter_hovertemplate)
            fig.add_trace(scatter.data[0])
            
        if df_productgroep.columns[20] in geselecteerde_kolommen:
            kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
            kleur_teller += 1
            scatter = px.scatter(df_productgroep, x=df_productgroep.columns[20], y='code', 
                                 color_discrete_sequence=[kleur], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 11'])
            
            scatter_hovertemplate = f'Oplossing 11: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
            scatter.update_traces(hovertemplate=scatter_hovertemplate)
            fig.add_trace(scatter.data[0])

    fig.update_layout(height=250)
    
    fig.update_yaxes(visible=False, showticklabels=False)

    st.plotly_chart(fig)


# In[ ]:


df2 = pd.DataFrame(st.session_state.doelwaardes, columns=['oplossing', 'kosten', 'milieukosten'])
df_k = df2[['oplossing', 'kosten']]

df_k = df_k.T
df_k.columns = df_k.iloc[0]
df_k = df_k[1:]

df_k['minimaal'] = pd.to_numeric(df_k['minimaal'])
df_k['maximaal'] = pd.to_numeric(df_k['maximaal'])

df_k['aantal'] = df_k['maximaal'] - df_k['minimaal']
df_k['code'] = '00'

kleur_teller = 0
fig2 = px.bar(df_k, x='aantal', y='code', base = 'minimaal',
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title='kosten', 
             hover_data = {'minimaal': True, 'maximaal': True, 'code': False, 'aantal': False})

bar_hovertemplate = 'Minimaal: €%{customdata[0]:,.2f}<br>Maximaal: €%{customdata[1]:,.2f}<br>'
fig2.update_traces(hovertemplate=bar_hovertemplate, customdata=df_k[['minimaal', 'maximaal']].values)

if df_k.columns[-3] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_k, x='huidige_waarden', y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['huidig'])
    
    scatter_hovertemplate = f'Huidige waarde: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_k.columns[0] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_k, x=df_k.columns[0], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 1'])
    
    scatter_hovertemplate = f'Oplossing 1: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_k.columns[1] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_k, x=df_k.columns[1], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 2'])
    
    scatter_hovertemplate = f'Oplossing 2: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_k.columns[2] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_k, x=df_k.columns[2], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 3'])
    
    scatter_hovertemplate = f'Oplossing 3: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_k.columns[3] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_k, x=df_k.columns[3], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 4'])
    
    scatter_hovertemplate = f'Oplossing 4: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_k.columns[4] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_k, x=df_k.columns[4], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 5'])
    
    scatter_hovertemplate = f'Oplossing 5: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if st.session_state.doelstelling == 'Geen voorkeur':
    if df_k.columns[5] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_k, x=df_k.columns[5], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 6'])
        
        scatter_hovertemplate = f'Oplossing 6: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_k.columns[6] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_k, x=df_k.columns[6], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 7'])
        
        scatter_hovertemplate = f'Oplossing 7: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_k.columns[7] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_k, x=df_k.columns[7], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 8'])
        
        scatter_hovertemplate = f'Oplossing 8: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_k.columns[8] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_k, x=df_k.columns[8], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 9'])
        
        scatter_hovertemplate = f'Oplossing 9: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_k.columns[9] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_k, x=df_k.columns[9], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 10'])
        
        scatter_hovertemplate = f'Oplossing 10: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_k.columns[10] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_k, x=df_k.columns[10], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 11'])
        
        scatter_hovertemplate = f'Oplossing 11: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])
    
fig2.update_layout(height=250)

fig2.update_yaxes(visible=False, showticklabels=False)
st.plotly_chart(fig2)


# In[ ]:


df2 = pd.DataFrame(st.session_state.doelwaardes, columns=['oplossing', 'kosten', 'milieukosten'])

df_mk = df2[['oplossing', 'milieukosten']]

df_mk = df_mk.T
df_mk.columns = df_mk.iloc[0]
df_mk = df_mk[1:]

df_mk['minimaal'] = pd.to_numeric(df_mk['minimaal'])
df_mk['maximaal'] = pd.to_numeric(df_mk['maximaal'])

df_mk['aantal'] = df_mk['maximaal'] - df_mk['minimaal']
df_mk['code'] = '00'

kleur_teller = 0

fig2 = px.bar(df_mk, x='aantal', y='code', base = 'minimaal',
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title='milieukosten', 
                 hover_data={'minimaal': True, 'maximaal': True, 'code': False, 'aantal': False})

bar_hovertemplate = 'Minimaal: €%{customdata[0]:,.2f}<br>Maximaal: €%{customdata[1]:,.2f}<br>'
fig2.update_traces(hovertemplate=bar_hovertemplate, customdata=df_mk[['minimaal', 'maximaal']].values)

if df_mk.columns[-3] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_mk, x='huidige_waarden', y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol=['huidig'])
    
    scatter_hovertemplate = f'Huidige waarde: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_mk.columns[0] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_mk, x=df_mk.columns[0], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 1'])
    
    scatter_hovertemplate = f'Oplossing 1: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])
    
if df_mk.columns[1] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_mk, x=df_mk.columns[1], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 2'])
    
    scatter_hovertemplate = f'Oplossing 2: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_mk.columns[2] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_mk, x=df_mk.columns[2], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 3'])
    
    scatter_hovertemplate = f'Oplossing 3: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_mk.columns[3] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_mk, x=df_mk.columns[3], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 4'])
    
    scatter_hovertemplate = f'Oplossing 4: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if df_mk.columns[4] in geselecteerde_kolommen:
    kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
    kleur_teller += 1
    scatter = px.scatter(df_mk, x=df_mk.columns[4], y='code', 
                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                         size=[10], symbol = ['oplossing 5'])
    
    scatter_hovertemplate = f'Oplossing 5: €%{{x:,.2f}}<br>'
    scatter.update_traces(hovertemplate=scatter_hovertemplate)
    fig2.add_trace(scatter.data[0])

if st.session_state.doelstelling == 'Geen voorkeur':
    if df_mk.columns[5] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_mk, x=df_mk.columns[5], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 6'])
        
        scatter_hovertemplate = f'Oplossing 6: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_mk.columns[6] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_mk, x=df_mk.columns[6], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 7'])
        
        scatter_hovertemplate = f'Oplossing 7: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_mk.columns[7] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_mk, x=df_mk.columns[7], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 8'])
        
        scatter_hovertemplate = f'Oplossing 8: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_mk.columns[8] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_mk, x=df_mk.columns[8], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 9'])
        
        scatter_hovertemplate = f'Oplossing 9: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_mk.columns[9] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_mk, x=df_mk.columns[9], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 10'])
        
        scatter_hovertemplate = f'Oplossing 10: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

    if df_mk.columns[10] in geselecteerde_kolommen:
        kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
        kleur_teller += 1
        scatter = px.scatter(df_mk, x=df_mk.columns[10], y='code', 
                             color_discrete_sequence=[kleur], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 11'])
        
        scatter_hovertemplate = f'Oplossing 11: €%{{x:,.2f}}<br>'
        scatter.update_traces(hovertemplate=scatter_hovertemplate)
        fig2.add_trace(scatter.data[0])

fig2.update_layout(height=250)

fig2.update_yaxes(visible=False, showticklabels=False)
st.plotly_chart(fig2)


# In[2]:


import locale


# In[ ]:


# st.page_link("pages/advies.py", label="Naar advies")
# st.page_link("pages/visualisatie.py", label="Visualisatie oplossingen")

