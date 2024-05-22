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


# In[ ]:


if "doelstelling" not in st.session_state:
    st.session_state.doelstelling = None
    
st.session_state._doelstelling = st.session_state.doelstelling

def set_doelstelling():
    st.session_state.doelstelling = st.session_state._doelstelling
    
if "bvo" not in st.session_state:
    st.session_state.bvo = None
    
st.session_state._bvo = st.session_state.bvo

def set_bvo():
    st.session_state.bvo = st.session_state._bvo
    


# In[ ]:


st.markdown("**Primair thema**")
st.selectbox("Welke thema heeft prioriteit in dit project?", 
            ("Circulair", "Budget"), 
            index = None, 
            placeholder='selecteer een thema...', key='_doelstelling', on_change=set_doelstelling)

st.markdown("**Bruto vloeroppervlak**")
st.number_input("Wat is het totale bvo in dit project?", value = 0, key = '_bvo', on_change=set_bvo)


# In[20]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
data


# In[21]:


data2 = pd.read_csv("dataframe2.csv", sep=';', decimal = ',')
data2


# In[ ]:


data2['minimaal'] = data2['minimaal'] * st.session_state.appartementen
data2['maximaal'] = data2['maximaal'] * st.session_state.appartementen
data2['constant'] = ['']*len(data2)
data.head()


# In[ ]:


data['minimaal'] = data['minimaal'] * st.session_state.appartementen
data['maximaal'] = data['maximaal'] * st.session_state.appartementen
data['constant'] = ['']*len(data)
data.head()


# In[ ]:


filtered = data.dropna(subset=['minimaal', 'maximaal'])

productgroepen = filtered['productgroep'].unique()
selected_productgroepen = st.multiselect("Selecteer een productgroep", productgroepen)
filtered_data = filtered[filtered['productgroep'].isin(selected_productgroepen)]

fig = make_subplots(rows=2, cols=1)

fig.append_trace(go.Scatter(x=filtered_data['kosten'], y=filtered_data['constant'], mode='markers'), row=1, col=1)
fig.append_trace(go.Scatter(x=filtered_data['circulair'], y=filtered_data['constant'], mode='markers'), row=2, col=1)

fig.update_yaxes(visible=False)

x_min_kosten = min(filtered['kosten']) - 100
x_max_kosten = max(filtered['kosten']) + 100

fig.update_xaxes(range=[x_min_kosten, x_max_kosten], row=1, col=1)

x_min_circulair = min(filtered['circulair']) - 10
x_max_circulair = max(filtered['circulair']) + 10

fig.update_xaxes(range=[x_min_circulair, x_max_circulair], row=2, col=1)

st.plotly_chart(fig)


# In[9]:


# filtered = data.dropna(subset=['minimaal', 'maximaal'])

# productgroepen = filtered['productgroep'].unique()
# selected_productgroepen = st.multiselect("Selecteer een productgroep", productgroepen)
# filtered_data = filtered[filtered['productgroep'].isin(selected_productgroepen)]

# fig_kosten = px.scatter(filtered_data, x='kosten', y = ['constant'], color='productgroep')
# fig_kosten.update_traces(marker_size=10)

# fig_kosten.update_yaxes(visible=False)

# # Bepaal de minimum- en maximumwaarden voor de x-as
# x_min = min(filtered['kosten']) - 100
# x_max = max(filtered['kosten']) + 100

# # Vastzetten van de x-as range
# fig_kosten.update_xaxes(range=[x_min, x_max])

# st.plotly_chart(fig_kosten)


# In[ ]:


# fig_circulair = px.scatter(filtered_data, x='circulair', y = ['constant'], color='productgroep')
# fig_circulair.update_traces(marker_size=10, showlegend=False)

# fig_circulair.update_yaxes(visible=False)

# # Bepaal de minimum- en maximumwaarden voor de x-as
# x_min = min(filtered['circulair']) - 10
# x_max = max(filtered['circulair']) + 10

# # Vastzetten van de x-as range
# fig_circulair.update_xaxes(range=[x_min, x_max])

# st.plotly_chart(fig_circulair)


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

# In[ ]:


# import streamlit as st
# import pulp as pl
# import pandas as pd

# # Controleer of het projectbestand is geüpload
# if st.session_state.projectbestand is None:
#     st.markdown("Upload een bestand")
# else:
#     # Definieer de LP variabelen
#     variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows()}

#     # Maak de variabelenlijst
#     lp_variabelen = [(key, value) for key, value in variabelen.items()]

#     # Functie om het eerste doelstellingprobleem op te lossen
#     if st.session_state.doelstelling == 'Circulair':
#         prob1 = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
#         # Impact themas op productgroepen
#         variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
#         impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

#         circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
# #         st.markdown(f"Circulair doelstelling: {circulair}")

#         variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
#         impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

#         budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
# #         st.markdown(f"Budget doelstelling: {budget}")
        
#         prob1 += circulair

#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
# #         prob1 += sum([lp_variabelen[i][1] for i in range(len(lp_variabelen)) if data.iloc[i, 1] == "m2"]) == st.session_state.bvo
# #         prob1 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) <= st.session_state.budget
            
#         status = prob1.solve()
#         st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
#         st.markdown(f"Waarde van de doelfunctie (circulair): {prob1.objective.value()}")
#         Z1_opt = pl.value(prob1.objective)
        
#         prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
        
#         prob2 += budget
        
#         prob2 += pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair))) <= Z1_opt
        
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 prob2 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob2 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
# #         prob2 += sum([lp_variabelen[i][1] for i in range(len(lp_variabelen)) if data.iloc[i, 1] == "m2"]) == st.session_state.bvo
# #         prob2 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) <= st.session_state.budget

#         status = prob2.solve()
#         st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
#         st.markdown(f"Waarde van de doelfunctie (budget): {prob2.objective.value()}")

#         # Maak een DataFrame van de variabelen en hun waarden
#         variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
#         df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])
#         st.dataframe(df)
        
#     if st.session_state.doelstelling == 'Budget':
#         prob1 = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
#         variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
#         impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

#         budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
# #         st.markdown(f"Budget doelstelling: {budget}")
        
#         prob1 += budget
        
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
# #         prob1 += sum([lp_variabelen[i][1] for i in range(len(lp_variabelen)) if data.iloc[i, 1] == "m2"]) == st.session_state.bvo
                
# #         prob1 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) == st.session_state.budget

#         status = prob1.solve()
#         st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
#         st.markdown(f"Waarde van de doelfunctie (budget): {prob1.objective.value()}")
#         Z1_opt = pl.value(prob1.objective)
        
#         prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
        
#         # Impact themas op productgroepen
#         variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
#         impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

#         circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair))) 
# #         st.markdown(f"Circulair doelstelling: {circulair}")
        
#         prob2 += circulair
        
#         prob2 += pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) <= Z1_opt
        
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 prob2 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob2 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
# #         prob2 += sum([lp_variabelen[i][1] for i in range(len(lp_variabelen)) if data.iloc[i, 1] == "m2"]) == st.session_state.bvo

# #         prob2 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) == st.session_state.budget

#         status = prob2.solve()
#         st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
#         st.markdown(f"Waarde van de doelfunctie (circulair): {prob2.objective.value()}")

#         # Maak een DataFrame van de variabelen en hun waarden
#         variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
#         df = pd.DataFrame(variabelen_waarden, columns=['productgroep', 'waarde'])
#         st.dataframe(df)


# In[ ]:


import streamlit as st
import pulp as pl
import pandas as pd

# Controleer of het projectbestand is geüpload
if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    st.markdown("levensduur")
    # Definieer de LP variabelen
    variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows()}

    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]

    # Functie om het eerste doelstellingprobleem op te lossen
    if st.session_state.doelstelling == 'Circulair':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))

        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        
        prob += 2 * circulair + budget 

        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data.iloc[i, 3]
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (circulair): {prob.objective.value()}")
        
    if st.session_state.doelstelling == 'Budget':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        
        prob += 2 * budget + circulair
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data.iloc[i, 3]
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (budget): {prob.objective.value()}")

    # Maak een DataFrame van de variabelen en hun waarden
    variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
    df = pd.DataFrame(variabelen_waarden, columns=['productgroep', 'waarde'])
    st.dataframe(df)


# **levensduur**

# In[ ]:


import streamlit as st
import pulp as pl
import pandas as pd

# Controleer of het projectbestand is geüpload
if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    st.markdown("levensduur")
    # Definieer de LP variabelen
    variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data2.iterrows()}

    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]

    # Functie om het eerste doelstellingprobleem op te lossen
    if st.session_state.doelstelling == 'Circulair':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMaximize)
        
        # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        impact_circulair = [data2.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))

        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        impact_budget = [data2.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        
        prob += 2 * circulair - budget 

        for i in range(len(lp_variabelen)):
            if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data2.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data2.iloc[i, 3]
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (circulair): {prob.objective.value()}")
        
    if st.session_state.doelstelling == 'Budget':
        prob = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        impact_budget = [data2.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        impact_circulair = [data2.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]) and pd.notna(data2.iloc[i, 4]) and pd.notna(data2.iloc[i, 5])]
        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        
        prob += 2 * budget - circulair
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data2.iloc[i, 2]) and pd.notna(data2.iloc[i, 3]):
                prob += lp_variabelen[i][1] >= data2.iloc[i, 2]
                prob += lp_variabelen[i][1] <= data2.iloc[i, 3]
        
        status = prob.solve()
        st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (budget): {prob.objective.value()}")

    # Maak een DataFrame van de variabelen en hun waarden
    variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
    df = pd.DataFrame(variabelen_waarden, columns=['productgroep', 'waarde'])
    st.dataframe(df)


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    if st.session_state.doelstelling is not None:
        st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")

        df = pd.merge(df, data[['productgroep', 'eenheid']], on='productgroep')
        
        for index, row in df.iterrows():
            st.markdown(f"- Binnen de productgroep {row['productgroep']} moet er {row['waarde']} {row['eenheid']} besteed worden")

