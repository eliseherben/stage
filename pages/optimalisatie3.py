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


# data


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
    'rgba(119, 118, 121, 1.0)']

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
        x=1))

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
        'rgba(119, 118, 121, 1.0)']

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
            x=1))

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
            """)
    
    with col2:
        circulair = data.sort_values(by='circulair')

        st.markdown(
            f"""
            Laagste milieukosten per eenheid:
            - {circulair['productgroep'].iloc[0]}
            - {circulair['productgroep'].iloc[1]}
            - {circulair['productgroep'].iloc[2]}
            """)


# **minimale afwijking**

# uitwerkingen voor visualisaties

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
    {"type": "90 Terreininrichting", "key_toggle": "Terreininrichting_on"}]
    
    for element in elements:
        if not st.session_state[element['key_toggle']]:
            for index, row in data.iterrows():
                if element['type'] == row['productgroep']:
                    data.at[index, 'optimalisatie'] = 'nee'

    data['code'] = data['productgroep'].str[:2]

    data['huidige_waarden'] = 0
    
    data['huidige_waarden'] = data.apply(
    lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['huidige_waarden'], axis=1)
    
    data.loc[data['productgroep'] == '48 Na-isolatie', 'huidige_waarden'] = 0
    
    data['minimaal'] = data.apply(
    lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['minimaal'], axis=1)
    
    data.loc[data['productgroep'] == '48 Na-isolatie', 'minimaal'] = 0
    
    data['maximaal'] = data.apply(
    lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['maximaal'], axis=1)

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
    {"type": "90 Terreininrichting", "key_input": "Terreininrichting"}]
    
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
    
#     if st.session_state.doelstelling == 'Minimale milieukosten':
#         gewichten = [(1, 0), (0.9, 0.1), (0.8, 0.2), (0.7, 0.3), (0.6, 0.4)]  # Lijst van wegingen
#     if st.session_state.doelstelling == 'Minimale afwijkingen van de huidge aantallen':
#         gewichten = [(0, 1), (0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6)]  # Lijst van wegingen
#     if st.session_state.doelstelling == 'Geen voorkeur':
    gewichten =  [(i/99, 1 - i/99) for i in range(100)]

#         [(0, 1), (0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6), (0.5, 0.5), 
#                      (0.6, 0.4), (0.7, 0.3), (0.8, 0.2), (0.9, 0.1), (1, 0)]
    
    oplossingen = {}
    doelwaardes = []
    vorige_oplossing = None
    omslagpunten = []
    j = 1
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
    
        oplossingen[f"Oplossing {j}"] = [var.varValue for key, var in lp_variabelen]
        oplossingswaarden = list(oplossingen[f"Oplossing {j}"])

#         data[f"Oplossing {j}"] = None
#         if pl.LpStatus[status] == 'Optimal':
#             index = 0
#             for i, row in data.iterrows():
#                 if row['optimalisatie'] == 'ja':
#                     if index < len(oplossingswaarden):
#                         data.at[i, f"Oplossing {j}"] = oplossingswaarden[index]
#                         index += 1
#                 else:
#                     data.at[i, f"Oplossing {j}"] = data.at[i, 'huidige_waarden']

#         doelwaardes.append((f"Oplossing {j}", 
#                             (data[f"Oplossing {j}"] * data['kosten']).sum(), 
#                             (data[f"Oplossing {j}"] * data['circulair']).sum(), 
#                             afwijkingen.value()))
        huidige_oplossing = {var.name: var.varValue for var in prob.variables() if var.varValue != 0 and not var.name.startswith('d_')}

        j += 1
        
 # Controleer of er een significante verandering is in de oplossing
        if vorige_oplossing is not None:
            significant_change = any(
                abs(huidige_oplossing.get(var, 0) - vorige_oplossing.get(var, 0)) > 1
                for var in set(huidige_oplossing) | set(vorige_oplossing)
            )
            if significant_change:
                omslagpunt = {"Gewicht_circulair": w_circulair, "Gewicht_afwijkingen": w_afwijkingen}
                omslagpunt.update(huidige_oplossing)
                omslagpunten.append(omslagpunt)
        vorige_oplossing = huidige_oplossing
    
    omslagpunten_df = pd.DataFrame(omslagpunten)
    if st.session_state.doelstelling == 'Minimale milieukosten':
        omslagpunten_df = omslagpunten_df[omslagpunten_df['Gewicht_circulair'] > omslagpunten_df['Gewicht_afwijkingen']]
        omslagpunten_df = omslagpunten_df.reset_index(drop = True)
    if st.session_state.doelstelling == 'Minimale afwijkingen van de huidge aantallen':
        omslagpunten_df = omslagpunten_df[omslagpunten_df['Gewicht_afwijkingen'] > omslagpunten_df['Gewicht_circulair']]
        omslagpunten_df = omslagpunten_df.reset_index(drop = True)
    current_index = omslagpunten_df.index

    # Nieuwe index met 'oplossing' ervoor en +1 toegevoegd aan elke indexwaarde
    new_index = ['Oplossing ' + str(idx + 1) for idx in current_index]

    # Toepassen van de nieuwe index op het DataFrame
    omslagpunten_df.index = new_index
        
    new_columns = [col.replace('__', ' -').replace('_', ' ') for col in omslagpunten_df.columns]
    omslagpunten_df.columns = new_columns
    omslagpunten_df = omslagpunten_df.transpose()
    omslagpunten_df['code'] = omslagpunten_df.index.str[:2]
    
    result_df = pd.merge(data, omslagpunten_df, on = 'code',  how = 'left')
    row_index = result_df.index[result_df['productgroep'] == '48 Na-isolatie'].tolist()[0]
    result_df.iloc[row_index, 2:] = result_df.iloc[row_index, 2:].fillna(0)
    
    afwijkingen = []
    for a in range(10, result_df.shape[1]):
        afwijking = []
        for i in range(result_df.shape[0]):
            afwijking.append(abs(result_df.iloc[i, 9] - result_df.iloc[i, a]))
        afwijkingen.append(sum(afwijking))

    for i in range(len(afwijkingen)):
        doelwaardes.append((f"Oplossing {i+1}", 
                                (result_df[f"Oplossing {i+1}"] * result_df['kosten']).sum(), 
                                (result_df[f"Oplossing {i+1}"] * result_df['circulair']).sum(), 
                                afwijkingen[i]))
            
    max_abs_diff = result_df.apply(lambda row: max(abs(row['huidige_waarden'] - row['minimaal']), 
                                                   abs(row['huidige_waarden'] - row['maximaal'])), axis=1)
    doelwaardes.append(('minimaal', (result_df['minimaal'] * result_df['kosten']).sum(), 
                        (result_df['minimaal'] * result_df['circulair']).sum(), 0))
    doelwaardes.append(('maximaal', (result_df['maximaal'] * result_df['kosten']).sum(), 
                        (result_df['maximaal'] * result_df['circulair']).sum(), 
                       max_abs_diff.sum()))
    doelwaardes.append(('huidige_waarden', (result_df['huidige_waarden'] * result_df['kosten']).sum(), 
                        (result_df['huidige_waarden'] * result_df['circulair']).sum()))
    
    kolommen_uitsluiten = ['minimaal', 'maximaal', 'kosten', 'circulair', 'optimalisatie', 'constant', 'code']
    uitkomsten = result_df.drop(columns=kolommen_uitsluiten)
    uitkomsten[uitkomsten.columns[3:]] = uitkomsten[uitkomsten.columns[3:]].apply(pd.to_numeric)
    uitkomsten = uitkomsten.round(1) 
    columns = uitkomsten.columns.tolist()
    
    def plot_pie(milieukosten, afwijkingen):
        labels = ['Milieukosten', 'Afwijkingen']
        values = [milieukosten, afwijkingen]
        fig = px.pie(values=values, names=labels)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update(layout_showlegend=False)
        return fig

    for i in range(len(columns)-3):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Oplossing {i+1}:**")
            st.markdown(f"- Milieukosten {round(omslagpunten_df.iloc[0, i] * 100)}%")
            st.markdown(f"- Afwijkingen {round(omslagpunten_df.iloc[1, i] * 100)}%")

#         with col2:
#             # Maak een pie chart
#             fig = plot_pie(gewichten[i][0] * 100, gewichten[i][1] * 100)

#             # Weergeven van de pie chart in Streamlit
#             st.plotly_chart(fig, use_container_width=True)
        
        columns[i+3] = f'Oplossing {i+1}'
        uitkomsten.columns = columns
        oplossing = uitkomsten[['productgroep', 'eenheid', 'huidige_waarden', f'Oplossing {i+1}']]
        st.dataframe(oplossing, hide_index = True)

    st.dataframe(result_df)
    uitkomsten.columns = columns
    st.session_state.oplossingen = result_df
    st.session_state.doelwaardes = doelwaardes
    gevoeligheidsanalyse = uitkomsten.drop(['eenheid', 'huidige_waarden'], axis=1)
    gevoeligheidsanalyse = gevoeligheidsanalyse.transpose()
    gevoeligheidsanalyse.columns = gevoeligheidsanalyse.iloc[0]
    gevoeligheidsanalyse = gevoeligheidsanalyse[1:]
#     gevoeligheidsanalyse['wegingen'] = gewichten
    
#     waardes = doelwaardes[:-1]
#     for (index, kosten, circulair, afwijking) in waardes:
#         # Controleren of de index bestaat in het dataframe
#         if index in gevoeligheidsanalyse.index:
#             gevoeligheidsanalyse.loc[index, 'kosten'] = kosten
#             gevoeligheidsanalyse.loc[index, 'circulair'] = circulair
#             gevoeligheidsanalyse.loc[index, 'afwijking'] = afwijking
    
#     st.dataframe(gevoeligheidsanalyse)
    
#     gevoeligheidsanalyse['x'] = gevoeligheidsanalyse['wegingen'].apply(lambda x: x[0])

    # Itereer over elke kolom behalve de laatste kolom (nu 'Y')
#     x = 'x'
#     for col in gevoeligheidsanalyse.columns[:-1]:
#         fig = px.line(gevoeligheidsanalyse, x=x, y=col)
#         st.plotly_chart(fig)

    col1, col2, col3 = st.columns(3)
    st.markdown("###### Vergelijking")
    options = st.multiselect(
    "Kies tot 4 oplossingen voor een vergelijking",
    [i for i in uitkomsten.columns[3:]], max_selections = 4)
    
    if len(options) != 0:
        cols = st.columns(len(options))

        for i, option in enumerate(options):
            with cols[i]:
                st.markdown(f"**{option}**")
                x = pd.to_numeric(option[10:])
                st.markdown(f"- Milieukosten {gewichten[x-1][0] * 100}%")
                st.markdown(f"- Afwijkingen {gewichten[x-1][1] * 100}%")
        kolommen = ['productgroep', 'eenheid', 'huidige_waarden'] + options
        vergelijken = uitkomsten[kolommen]
        st.dataframe(vergelijken, hide_index = True)


# gevoeligheidsanalyse

# In[ ]:


# # Controleer of het projectbestand is geüpload
# if st.session_state.projectbestand is None:
#     st.markdown("Upload een bestand")
# else:
#     st.markdown("#")
#     st.markdown("##### Minimale afwijking in productgroepen")
    
#     for i in range(len(data)):
#         if data.iloc[i, 0][:2] not in st.session_state.list:
#             data.drop(index = i, inplace = True)
    
#     elements = [
#     {"type": "21 Buitenwanden", "key_toggle": "Buitenwanden_on"},
#     {"type": "22 Binnenwanden", "key_toggle": "Binnenwanden_on"},
#     {"type": "23 Vloeren", "key_toggle": "Vloeren_on"},
#     {"type": "24 Trappen en hellingen", "key_toggle": "Trappen_en_hellingen_on"},
#     {"type": "27 Daken", "key_toggle": "Daken_on"},
#     {"type": "28 Hoofddraagconstructie", "key_toggle": "Hoofddraagconstructie_on"},
#     {"type": "31 Buitenkozijnen, -ramen, -deuren en -puien", "key_toggle": "Buitenkozijnen_on"},
#     {"type": "32 Binnenkozijnen en -deuren", "key_toggle": "Binnenkozijnen_en__deuren_on"},
#     {"type": "33 Luiken en vensters", "key_toggle": "Luiken_en_vensters_on"},
#     {"type": "34 Balustrades en leuningen", "key_toggle": "Balustrades_en_leuningen_on"},
#     {"type": "42 Binnenwandafwerkingen", "key_toggle": "Binnenwandafwerkingen_on"},
#     {"type": "43 Vloerafwerkingen", "key_toggle": "Vloerafwerkingen_on"},
#     {"type": "45 Plafonds", "key_toggle": "Plafonds_on"},
#     {"type": "64 Vaste gebouwvoorziening","key_toggle": "Vaste_gebouwvoorziening_on"},
#     {"type": "73 Keuken", "key_toggle": "Keuken_on"},
#     {"type": "90 Terreininrichting", "key_toggle": "Terreininrichting_on"}]
    
#     for element in elements:
#         if not st.session_state[element['key_toggle']]:
#             for index, row in data.iterrows():
#                 if element['type'] == row['productgroep']:
#                     data.at[index, 'optimalisatie'] = 'nee'

#     data['code'] = data['productgroep'].str[:2]

#     data['huidige_waarden'] = 0
    
#     data['huidige_waarden'] = data.apply(
#     lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['huidige_waarden'], axis=1)
    
#     data.loc[data['productgroep'] == '48 Na-isolatie', 'huidige_waarden'] = 0
    
#     data['minimaal'] = data.apply(
#     lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['minimaal'], axis=1)
    
#     data.loc[data['productgroep'] == '48 Na-isolatie', 'minimaal'] = 0
    
#     data['maximaal'] = data.apply(
#     lambda row: st.session_state.appartementen if pd.isna(row['eenheid']) else row['maximaal'], axis=1)

#     data.loc[data['productgroep'] == '48 Na-isolatie', 'maximaal'] = 0
     
#     huidigen = [
#     {"type": "21 Buitenwanden", "key_input": "Buitenwanden"},
#     {"type": "22 Binnenwanden", "key_input": "Binnenwanden"},
#     {"type": "23 Vloeren", "key_input": "Vloeren"},
#     {"type": "24 Trappen en hellingen", "key_input": "Trappen_en_hellingen"},
#     {"type": "27 Daken", "key_input": "Daken"},
#     {"type": "28 Hoofddraagconstructie", "key_input": "Hoofddraagconstructie"},
#     {"type": "31 Buitenkozijnen, -ramen, -deuren en -puien", "key_input": "Buitenkozijnen"},
#     {"type": "32 Binnenkozijnen en -deuren", "key_input": "Binnenkozijnen_en__deuren"},
#     {"type": "33 Luiken en vensters", "key_input": "Luiken_en_vensters"},
#     {"type": "34 Balustrades en leuningen", "key_input": "Balustrades_en_leuningen"},
#     {"type": "42 Binnenwandafwerkingen", "key_input": "Binnenwandafwerkingen"},
#     {"type": "43 Vloerafwerkingen", "key_input": "Vloerafwerkingen"},
#     {"type": "45 Plafonds", "key_input": "Plafonds"},
#     {"type": "64 Vaste gebouwvoorziening","key_input": "Vaste_gebouwvoorziening"},
#     {"type": "73 Keuken", "key_input": "Keuken"},
#     {"type": "90 Terreininrichting", "key_input": "Terreininrichting"}]
    
#     for huidige in huidigen:
#         for index, row in data.iterrows():
#             if huidige['type'] == row['productgroep']:
#                 data.at[index, 'huidige_waarden'] = st.session_state[huidige['key_input']]
    
#     # Definieer de LP variabelen
#     variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows() 
#                   if row["optimalisatie"] == 'ja'}
    
#     variabelen2 = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows() 
#                    if row["optimalisatie"] == 'nee' and row["productgroep"] != '48 Na-isolatie'}
    
#     # Maak de variabelenlijst
#     lp_variabelen = [(key, value) for key, value in variabelen.items()]
#     lp_variabelen2 = [(key, value) for key, value in variabelen2.items()]
#     lp_variabelen3 = lp_variabelen + [(key, value) for key, value in variabelen2.items()]

#     lp_variabelen3.sort()
    
#     dynamic_vars = {}
#     afwijkingen_list = []
#     doelwaardes = []
    
#     for (key, var), i in zip(lp_variabelen, range(len(lp_variabelen))):
#         if var.name == "31_Buitenkozijnen,__ramen,__deuren_en__puien":
#             var_name = (var.name.split("_")[1])[:-1] + '_start'
#             dynamic_vars[var_name] = st.session_state[(var.name.split("_")[1])[:-1]]

#             afwijkingen_var = pl.LpVariable('d_' + (var.name.split("_")[1])[:-1], lowBound = 0)
#             afwijkingen_list.append(afwijkingen_var)
#         else:
#             var_name = var.name[3:] + '_start'
#             dynamic_vars[var_name] = st.session_state[var.name[3:]]

#             afwijkingen_var = pl.LpVariable('d_' + var.name[3:], lowBound = 0) 
#             afwijkingen_list.append(afwijkingen_var)
                
#     startwaardes = list(dynamic_vars.values())
#     st.session_state.startwaardes = startwaardes
    
#     if st.session_state.doelstelling == 'Minimale milieukosten':
#         gewichten = [(1, 0), (0.9, 0.1), (0.8, 0.2), (0.7, 0.3), (0.6, 0.4)]  # Lijst van wegingen
#     if st.session_state.doelstelling == 'Minimale afwijkingen van de huidge aantallen':
#         gewichten = [(0, 1), (0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6)]  # Lijst van wegingen
#     if st.session_state.doelstelling == 'Geen voorkeur':
#         gewichten =  [(i/99, 1 - i/99) for i in range(100)]

# #         [(0, 1), (0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6), (0.5, 0.5), 
# #                      (0.6, 0.4), (0.7, 0.3), (0.8, 0.2), (0.9, 0.1), (1, 0)]
    
#     oplossingen = {}
#     doelwaardes = []
#     vorige_oplossing = None
#     omslagpunten = []
#     j = 1
#     for w_circulair, w_afwijkingen in gewichten:
#         prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
#         # Impact themas op productgroepen
#         variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen))]
#         impact_circulair = [data.iloc[i, 5] for i in range(len(data)) if data.iloc[i, 6] == 'ja']
#         circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        
#         variabelen_budget = [lp_variabelen3[i][1] for i in range(len(lp_variabelen3))]
#         impact_budget = [data.iloc[i, 4] for i in range(len(data)) if pd.notna(data.iloc[i, 4])]
#         budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        
#         variabelen_milieukosten = [lp_variabelen3[i][1] for i in range(len(lp_variabelen3))]
#         impact_milieukosten = [data.iloc[i, 5] for i in range(len(data)) if pd.notna(data.iloc[i, 4])]
#         milieukosten = pl.lpSum(variabelen_milieukosten[i] * impact_milieukosten[i] for i in range(len(variabelen_milieukosten)))
            
#         afwijkingen = pl.lpSum(afwijkingen_list)
        
#         prob += w_circulair * circulair + w_afwijkingen * afwijkingen
        
#         data2 = data[data['optimalisatie'] == 'ja']
#         data2 = data2.reset_index(drop=True)
#         for i in range(len(lp_variabelen)):
#             prob += lp_variabelen[i][1] >= data2.iloc[i, 2]
#             prob += lp_variabelen[i][1] <= data2.iloc[i, 3]
                
#         for a in range(len(afwijkingen_list)):
#             prob += afwijkingen_list[a] >= lp_variabelen[a][1] - startwaardes[a]
#             prob += afwijkingen_list[a] >= startwaardes[a] - lp_variabelen[a][1]
        
#         data3 = data[data['optimalisatie'] == 'nee']
#         data3 = data3[data3['productgroep'] != '48 Na-isolatie']
#         data3 = data3.reset_index(drop=True)
#         for i in range(len(lp_variabelen2)):
#             prob += lp_variabelen2[i][1] == data3.iloc[i, 9]
        
#         prob += budget == st.session_state.budget
        
#         status = prob.solve()
    
#         oplossingen[f"Oplossing {j}"] = [var.varValue for key, var in lp_variabelen]
#         oplossingswaarden = list(oplossingen[f"Oplossing {j}"])

#         data[f"Oplossing {j}"] = None
#         if pl.LpStatus[status] == 'Optimal':
#             index = 0
#             for i, row in data.iterrows():
#                 if row['optimalisatie'] == 'ja':
#                     if index < len(oplossingswaarden):
#                         data.at[i, f"Oplossing {j}"] = oplossingswaarden[index]
#                         index += 1
#                 else:
#                     data.at[i, f"Oplossing {j}"] = data.at[i, 'huidige_waarden']

#         doelwaardes.append((f"Oplossing {j}", 
#                             (data[f"Oplossing {j}"] * data['kosten']).sum(), 
#                             (data[f"Oplossing {j}"] * data['circulair']).sum(), 
#                             afwijkingen.value()))
#         huidige_oplossing = {var.name: var.varValue for var in prob.variables() if var.varValue != 0}

#         j += 1
#         st.markdown(vorige_oplossing)
        
#  # Controleer of er een significante verandering is in de oplossing
#         if vorige_oplossing is not None:
#             significant_change = any(
#                 abs(huidige_oplossing.get(var, 0) - vorige_oplossing.get(var, 0)) > 1
#                 for var in set(huidige_oplossing) | set(vorige_oplossing)
#             )
#             if significant_change:
#                 omslagpunt = {"Gewicht_circulair": w_circulair, "Gewicht_afwijkingen": w_afwijkingen}
#                 omslagpunt.update(huidige_oplossing)
#                 omslagpunten.append(omslagpunt)
#         vorige_oplossing = huidige_oplossing
    
#     omslagpunten_df = pd.DataFrame(omslagpunten)
#     st.dataframe(omslagpunten_df)

#     max_abs_diff = data.apply(lambda row: max(abs(row['huidige_waarden'] - row['minimaal']), abs(row['huidige_waarden'] - row['maximaal'])), axis=1)
#     doelwaardes.append(('minimaal', (data['minimaal'] * data['kosten']).sum(), (data['minimaal'] * data['circulair']).sum(), 0))
#     doelwaardes.append(('maximaal', (data['maximaal'] * data['kosten']).sum(), (data['maximaal'] * data['circulair']).sum(), 
#                        max_abs_diff.sum()))
#     doelwaardes.append(('huidige_waarden', (data['huidige_waarden'] * data['kosten']).sum(), (data['huidige_waarden'] * data['circulair']).sum()))
    
#     st.markdown(doelwaardes)
#     kolommen_uitsluiten = ['minimaal', 'maximaal', 'kosten', 'circulair', 'optimalisatie', 'constant', 'code']
#     uitkomsten = data.drop(columns=kolommen_uitsluiten)
#     uitkomsten[uitkomsten.columns[3:]] = uitkomsten[uitkomsten.columns[3:]].apply(pd.to_numeric)
#     uitkomsten = uitkomsten.round(1) 
#     columns = uitkomsten.columns.tolist()
    
#     def plot_pie(milieukosten, afwijkingen):
#         labels = ['Milieukosten', 'Afwijkingen']
#         values = [milieukosten, afwijkingen]
#         fig = px.pie(values=values, names=labels)
#         fig.update_traces(textposition='inside', textinfo='percent+label')
#         fig.update(layout_showlegend=False)
#         return fig

# #     for i in range(len(columns)-3):
# #         col1, col2 = st.columns([2, 1])
        
# #         with col1:
# #             st.markdown(f"**Oplossing {i+1}:**")
# #             st.markdown(f"- Milieukosten {gewichten[i][0] * 100}%")
# #             st.markdown(f"- Afwijkingen {gewichten[i][1] * 100}%")

# # #         with col2:
# # #             # Maak een pie chart
# # #             fig = plot_pie(gewichten[i][0] * 100, gewichten[i][1] * 100)

# # #             # Weergeven van de pie chart in Streamlit
# # #             st.plotly_chart(fig, use_container_width=True)
        
# #         columns[i+3] = f'Oplossing {i+1}'
# #         uitkomsten.columns = columns
# #         oplossing = uitkomsten[['productgroep', 'eenheid', 'huidige_waarden', f'Oplossing {i+1}']]
# #         st.dataframe(oplossing, hide_index = True)

#     uitkomsten.columns = columns
#     st.session_state.oplossingen = data
#     st.session_state.doelwaardes = doelwaardes
#     gevoeligheidsanalyse = uitkomsten.drop(['eenheid', 'huidige_waarden'], axis=1)
#     gevoeligheidsanalyse = gevoeligheidsanalyse.transpose()
#     gevoeligheidsanalyse.columns = gevoeligheidsanalyse.iloc[0]
#     gevoeligheidsanalyse = gevoeligheidsanalyse[1:]
#     gevoeligheidsanalyse['wegingen'] = gewichten
    
#     waardes = doelwaardes[:-1]
#     for (index, kosten, circulair, afwijking) in waardes:
#         # Controleren of de index bestaat in het dataframe
#         if index in gevoeligheidsanalyse.index:
#             gevoeligheidsanalyse.loc[index, 'kosten'] = kosten
#             gevoeligheidsanalyse.loc[index, 'circulair'] = circulair
#             gevoeligheidsanalyse.loc[index, 'afwijking'] = afwijking
    
#     st.dataframe(uitkomsten)
#     st.dataframe(gevoeligheidsanalyse)
    
#     gevoeligheidsanalyse['x'] = gevoeligheidsanalyse['wegingen'].apply(lambda x: x[0])

#     # Itereer over elke kolom behalve de laatste kolom (nu 'Y')
#     x = 'x'
#     for col in gevoeligheidsanalyse.columns[:-1]:
#         fig = px.line(gevoeligheidsanalyse, x=x, y=col)
#         st.plotly_chart(fig)

#     col1, col2, col3 = st.columns(3)
#     st.markdown("###### Vergelijking")
#     options = st.multiselect(
#     "Kies tot 4 oplossingen voor een vergelijking",
#     [i for i in uitkomsten.columns[3:]], max_selections = 4)
    
#     if len(options) != 0:
#         cols = st.columns(len(options))

#         for i, option in enumerate(options):
#             with cols[i]:
#                 st.markdown(f"**{option}**")
#                 x = pd.to_numeric(option[10:])
#                 st.markdown(f"- Milieukosten {gewichten[x-1][0] * 100}%")
#                 st.markdown(f"- Afwijkingen {gewichten[x-1][1] * 100}%")
#         kolommen = ['productgroep', 'eenheid', 'huidige_waarden'] + options
#         vergelijken = uitkomsten[kolommen]
#         st.dataframe(vergelijken, hide_index = True)


# In[ ]:


st.markdown('#')
st.markdown("##### Visualisaties")
df = st.session_state.oplossingen

kolommen_te_uitsluiten = ['eenheid', 'kosten', 'circulair', 'optimalisatie', 
                          'constant', 'productgroep', 'code', 'minimaal', 'maximaal']
kolommen_te_selecteren = [kolom for kolom in df.columns if kolom not in kolommen_te_uitsluiten]
geselecteerde_kolommen = st.multiselect('Selecteer oplossingen', kolommen_te_selecteren)

df = df[df['eenheid'].notna()]

df[df.columns[9:]] = df[df.columns[9:]].apply(pd.to_numeric)
df = df.round(1)
gewichten_df = omslagpunten_df.transpose()
gewichten_df['Gewicht circulair (%)'] = gewichten_df['Gewicht circulair'] * 100
gewichten_df['Gewicht afwijkingen (%)'] = gewichten_df['Gewicht afwijkingen'] * 100

gewichten_df = gewichten_df.iloc[:-1]
gewichten_df[gewichten_df.columns[:]] = gewichten_df[gewichten_df.columns[:]].apply(pd.to_numeric)

for productgroep in df['productgroep']:
    kleur_teller = 0
    # Selecteer de data voor de huidige productgroep
    df_productgroep = df[df['productgroep'] == productgroep]

    # Selecteer alle kolommen behalve de uitgesloten kolommen
    df_geselecteerd = df_productgroep.drop(columns=kolommen_te_uitsluiten)

    df_productgroep['aantal'] = df_productgroep['maximaal'] - df_productgroep['minimaal']

    fig = px.bar(df_productgroep, x='aantal', y='code', base='minimaal', color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], 
        title=f'{productgroep}',hover_data={'minimaal': True, 'maximaal': True, 'code': False, 'aantal': False}, 
        labels={'aantal': f'aantal ({df_productgroep["eenheid"].iloc[0]})'}
    )
    
    bar_hovertemplate = 'Minimaal: %{customdata[0]} %{customdata[2]}<br>Maximaal: %{customdata[1]} %{customdata[2]}<br>'
    fig.update_traces(hovertemplate=bar_hovertemplate, customdata=df_productgroep[['minimaal', 'maximaal', 'eenheid']].values)
    for i in range(len(kolommen_te_selecteren)):
        if kolommen_te_selecteren[i] in geselecteerde_kolommen:
            if kolommen_te_selecteren[i] == 'huidige_waarden':
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_productgroep, x='huidige_waarden', y='code', 
                                     color_discrete_sequence=[kleur], labels={'x': ''}, 
                                     size=[10], symbol = ['huidig'])

                scatter_hovertemplate = f'Huidige waarde: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
                scatter.update_traces(hovertemplate=scatter_hovertemplate)
                fig.add_trace(scatter.data[0])
            else:
                selected_row = gewichten_df.loc[[f'{kolommen_te_selecteren[i]}']]
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_productgroep, x=f'{kolommen_te_selecteren[i]}', y='code', 
                                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                                         size=[10], symbol = [f'{kolommen_te_selecteren[i]}'])

                scatter_hovertemplate = (
                    f'Oplossing 1: %{{x}} {df_productgroep["eenheid"].iloc[0]}<br>'
                    'Weging milieukosten: %{customdata[0]:.2f}%<br>'
                    'Weging afwijkingen: %{customdata[1]:.2f}%<br>'
                )
                scatter.update_traces(
                    hovertemplate=scatter_hovertemplate, 
                customdata=selected_row[['Gewicht circulair (%)', 'Gewicht afwijkingen (%)']])
                fig.add_trace(scatter.data[0])
            
    fig.update_layout(height=250)
    
    fig.update_yaxes(visible=False, showticklabels=False)

    st.plotly_chart(fig)


# In[ ]:


df2 = pd.DataFrame(st.session_state.doelwaardes, columns=['oplossing', 'kosten', 'milieukosten', 'afwijkingen'])
df_k = df2[['oplossing', 'kosten']]

df_k = df_k.T
df_k.columns = df_k.iloc[0]
df_k = df_k[1:]

df_k[df_k.columns[:]] = df_k[df_k.columns[:]].apply(pd.to_numeric)
df_k = df_k.round(2)

df_k['aantal'] = df_k['maximaal'] - df_k['minimaal']
df_k['code'] = '00'

kleur_teller = 0
fig2 = px.bar(df_k, x='aantal', y='code', base = 'minimaal',
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title='Kosten', 
             hover_data = {'minimaal': True, 'maximaal': True, 'code': False, 'aantal': False})

bar_hovertemplate = 'Minimaal: €%{customdata[0]:,.2f}<br>Maximaal: €%{customdata[1]:,.2f}<br>'
fig2.update_traces(hovertemplate=bar_hovertemplate, customdata=df_k[['minimaal', 'maximaal']].values)

for i in range(len(kolommen_te_selecteren)):
        if kolommen_te_selecteren[i] in geselecteerde_kolommen:
            if kolommen_te_selecteren[i] == 'huidige_waarden':
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_k, x='huidige_waarden', y='code', 
                                     color_discrete_sequence=[kleur], labels={'x': ''}, 
                                     size=[10], symbol = ['huidig'])

                scatter_hovertemplate = f'Huidige waarde: €%{{x:,.2f}}<br>'
                scatter.update_traces(hovertemplate=scatter_hovertemplate)
                fig2.add_trace(scatter.data[0])
            else:
                selected_row = gewichten_df.loc[[f'{kolommen_te_selecteren[i]}']]
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_k, x=f'{kolommen_te_selecteren[i]}', y='code', 
                                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                                         size=[10], symbol = [f'{kolommen_te_selecteren[i]}'])

                scatter_hovertemplate = (
                    f'Oplossing 1: €%{{x:,.2f}}<br>'
                    'Weging milieukosten: %{customdata[0]:.2f}%<br>'
                    'Weging afwijkingen: %{customdata[1]:.2f}%<br>'
                )
                scatter.update_traces(
                    hovertemplate=scatter_hovertemplate, 
                customdata=selected_row[['Gewicht circulair (%)', 'Gewicht afwijkingen (%)']])
                fig2.add_trace(scatter.data[0])
    
fig2.update_layout(height=250)

fig2.update_yaxes(visible=False, showticklabels=False)
st.plotly_chart(fig2)


# In[ ]:


df_mk = df2[['oplossing', 'milieukosten']]

df_mk = df_mk.T
df_mk.columns = df_mk.iloc[0]
df_mk = df_mk[1:]

df_mk[df_mk.columns[:]] = df_mk[df_mk.columns[:]].apply(pd.to_numeric)
df_mk = df_mk.round(2)

df_mk['aantal'] = df_mk['maximaal'] - df_mk['minimaal']
df_mk['code'] = '00'

kleur_teller = 0

fig2 = px.bar(df_mk, x='aantal', y='code', base = 'minimaal',
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title='Milieukosten', 
                 hover_data={'minimaal': True, 'maximaal': True, 'code': False, 'aantal': False})

bar_hovertemplate = 'Minimaal: €%{customdata[0]:,.2f}<br>Maximaal: €%{customdata[1]:,.2f}<br>'
fig2.update_traces(hovertemplate=bar_hovertemplate, customdata=df_mk[['minimaal', 'maximaal']].values)

for i in range(len(kolommen_te_selecteren)):
        if kolommen_te_selecteren[i] in geselecteerde_kolommen:
            if kolommen_te_selecteren[i] == 'huidige_waarden':
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_mk, x='huidige_waarden', y='code', 
                                     color_discrete_sequence=[kleur], labels={'x': ''}, 
                                     size=[10], symbol = ['huidig'])

                scatter_hovertemplate = f'Huidige waarde: €%{{x:,.2f}}<br>'
                scatter.update_traces(hovertemplate=scatter_hovertemplate)
                fig2.add_trace(scatter.data[0])
            else:
                selected_row = gewichten_df.loc[[f'{kolommen_te_selecteren[i]}']]
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_mk, x=f'{kolommen_te_selecteren[i]}', y='code', 
                                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                                         size=[10], symbol = [f'{kolommen_te_selecteren[i]}'])

                scatter_hovertemplate = (
                    f'Oplossing 1: €%{{x:,.2f}}<br>'
                    'Weging milieukosten: %{customdata[0]:.2f}%<br>'
                    'Weging afwijkingen: %{customdata[1]:.2f}%<br>'
                )
                scatter.update_traces(
                    hovertemplate=scatter_hovertemplate, 
                customdata=selected_row[['Gewicht circulair (%)', 'Gewicht afwijkingen (%)']])
                fig2.add_trace(scatter.data[0])
        
fig2.update_layout(height=250)

fig2.update_yaxes(visible=False, showticklabels=False)
st.plotly_chart(fig2)


# In[ ]:


df2 = pd.DataFrame(st.session_state.doelwaardes, columns=['oplossing', 'kosten', 'milieukosten', 'afwijkingen'])
df_a = df2[['oplossing', 'afwijkingen']]

df_a = df_a.T
df_a.columns = df_a.iloc[0]
df_a = df_a[1:]

df_a[df_a.columns[:]] = df_a[df_a.columns[:]].apply(pd.to_numeric)
df_a = df_a.round(1)

df_a['aantal'] = df_a['maximaal'] - df_a['minimaal']
df_a['code'] = '00'
df_a = df_a.round(1) 

kleur_teller = 0
fig2 = px.bar(df_a, x='aantal', y='code', base = 'minimaal',
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title='Afwijkingen', 
             hover_data = {'minimaal': True, 'maximaal': True, 'code': False, 'aantal': False})

bar_hovertemplate = 'Minimaal: %{customdata[0]}<br>Maximaal: %{customdata[1]}<br>'
fig2.update_traces(hovertemplate=bar_hovertemplate, customdata=df_a[['minimaal', 'maximaal']].values)

for i in range(len(kolommen_te_selecteren)):
        if kolommen_te_selecteren[i] in geselecteerde_kolommen:
            if kolommen_te_selecteren[i] == 'huidige_waarden':
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_a, x='huidige_waarden', y='code', 
                                     color_discrete_sequence=[kleur], labels={'x': ''}, 
                                     size=[10])

                scatter_hovertemplate = f'Huidige waarde: €%{{x:,.2f}}<br>'
                scatter.update_traces(hovertemplate=scatter_hovertemplate)
                fig2.add_trace(scatter.data[0])
            else:
                selected_row = gewichten_df.loc[[f'{kolommen_te_selecteren[i]}']]
                kleur = kleuren_schema[kleur_teller % len(kleuren_schema)]
                kleur_teller += 1
                scatter = px.scatter(df_a, x=f'{kolommen_te_selecteren[i]}', y='code', 
                                         color_discrete_sequence=[kleur], labels={'x': ''}, 
                                         size=[10], symbol = [f'{kolommen_te_selecteren[i]}'])

                scatter_hovertemplate = (
                    f'Oplossing 1: €%{{x:,.2f}}<br>'
                    'Weging milieukosten: %{customdata[0]:.2f}%<br>'
                    'Weging afwijkingen: %{customdata[1]:.2f}%<br>'
                )
                scatter.update_traces(
                    hovertemplate=scatter_hovertemplate, 
                customdata=selected_row[['Gewicht circulair (%)', 'Gewicht afwijkingen (%)']])
                fig2.add_trace(scatter.data[0])
    
fig2.update_layout(height=250)

fig2.update_yaxes(visible=False, showticklabels=False)
st.plotly_chart(fig2)


# In[ ]:


# st.markdown("##### Uitkomsten doelfuncties")
# df2 = df2[:-3]

# df2['gewichten'] = gewichten
# st.dataframe(df2)
# # Functie om de voorkeur te bepalen
# def bepaal_voorkeur(wegingen):
#     # Splitsen van de string en omzetten naar float
#     circulair = wegingen[0]
#     afwijkingen = wegingen[1]
    
#     # Bepalen van de voorkeur
#     if circulair > afwijkingen:
#         return "voorkeur voor milieukosten"
#     elif circulair < afwijkingen:
#         return "voorkeur voor afwijkingen"
#     else:
#         return "geen voorkeur"

# # Nieuwe kolom toevoegen met de voorkeur
# df2['voorkeur'] = df2['gewichten'].apply(bepaal_voorkeur)

# for i in range(len(df2)):
#     df2.iloc[i, 0] = f"Oplossing {i + 1}"
    
# df2 = df2.round(1) 
# df3 = df2[['oplossing', 'kosten', 'milieukosten', 'afwijkingen']]
# st.dataframe(df3, hide_index = True)

# # Kleuren toewijzen
# color_discrete_map = {
#     "voorkeur voor milieukosten": "rgba(212, 0, 60, 1.0)",
#     "voorkeur voor afwijkingen": "rgba(0, 158, 224, 1.0)", 
#     "geen voorkeur": "rgba(151, 191, 13, 1.0)"
# }

# # Scatter plot maken
# fig = px.scatter(df2, x="milieukosten", y="afwijkingen", color="voorkeur",
#                  color_discrete_map=color_discrete_map, 
#                  labels={
#                      "milieukosten": "Totale milieukosten in euro's",
#                      "afwijkingen": "Totale afwijkingen",
#                      "voorkeur": "Voorkeur"}, 
#                  title="Uitkomsten doelfuncties pareto", 
#                  hover_data = {'oplossing': True, 'kosten': True, 'milieukosten': True, 'afwijkingen': True, 
#                                'gewichten': False, 'voorkeur': False})

# st.plotly_chart(fig)


# In[ ]:


# st.page_link("pages/advies.py", label="Naar advies")
# st.page_link("pages/visualisatie.py", label="Visualisatie oplossingen")

