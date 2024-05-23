#!/usr/bin/env python
# coding: utf-8

# In[121]:


import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import timedelta


# In[ ]:


st.markdown("**Pareto oplossingen**")
st.page_link("simplex.py", label="Homepagina")


# In[122]:


def kosten(x):
    return (223.07 * x[0] + 82.85 * x[1] + 271.83 * x[2] + 5437.50 * x[3] + 1359.22 * x[4] + 158.24 * x[5] + 2486.31 * x[6] + 
            830.05 * x[7] + 2195 * x[8] + 290.39 * x[9] + 26.54 * x[10] + 71.58 * x[11] + 107.67 * x[12] + 4529.66 * x[14] + 
            80.30 * x[15] + 5802.38 * x[16] + 5919.05 * x[17] + 2261.15 * x[18] + 342.39 * x[19] + 2800 * x[20] + 
            11694.64 * x[21] + 680.43 * x[22] + 1169.44 * x[23] + 90 * x[24]) 

def mki(x):
    return (1.22 * x[0] + 2.50 * x[1] + 9.84 * x[2] + 39.97 * x[3] + 1.06 * x[4] + 2.91 * x[5] + 1.46 * x[6] + 2.47 * x[7] + 
            5.24 * x[8] + 1.15 * x[10] + 0.84 * x[11] + 1.95 * x[12] + 0.82 * x[13] + 0.85 * x[14] + 43.87 * x[15] + 
            45.05 * x[16] + 19.43 * x[19] + 119.39 * x[21] + 18.97 * x[22] + 8.60 * x[23] + 2.22 * x[24])


# In[123]:


def dominates(x, y):
    return (x[0] <= y[0] and x[1] <= y[1] and 
            (x[0] < y[0] or x[1] < y[1]))


# In[124]:


def uitkomsten(oplossing):
    f1 = kosten(oplossing)
    f2 = mki(oplossing)
    return (f1 + f2)


# In[125]:


def startoplossing():
    grenzen = [(442, 1448), (754, 1067), (896, 1689), (3, 6), (234, 810), 
           (270, 787), (90, 112), (33, 154), (3, 11), (100, 159), 
           (661, 1847), (895, 1425), (755, 1155), (0, 0), (0, 0),
           (0, 0), (0, 0), (0, 0), (0, 0), (14, 32),
           (0, 0), (0, 0), (29, 61), (0, 0), (33, 34)]
    
    startoplossing = tuple(random.uniform(a, b) for a, b in grenzen)
    return startoplossing


# In[126]:


def startpopulatie(startoplossing):
    grenzen = [(442, 1448), (754, 1067), (896, 1689), (3, 6), (234, 810), 
           (270, 787), (90, 112), (33, 154), (3, 11), (100, 159), 
           (661, 1847), (895, 1425), (755, 1155), (0, 0), (0, 0),
           (0, 0), (0, 0), (0, 0), (0, 0), (14, 32),
           (0, 0), (0, 0), (29, 61), (0, 0), (33, 34)]
    
    huidige_oplossing = startoplossing
    
    populatie = [huidige_oplossing]
    
    for _ in range(199):
        nieuwe_oplossing = tuple(random.uniform(a, b) for a, b in grenzen)
        populatie.append(nieuwe_oplossing)
        
    for x in range(len(populatie)):
        populatie[x] = (list(populatie[x]), uitkomsten(populatie[x]))
    populatie.sort(key=lambda uitkomst: uitkomst[1])
    
    return populatie


# In[127]:


def ouders_maken(populatie):
    ouders = []
    beste = [i for i in populatie[0:100]]
    slechtste = [i for i in populatie[100:]] 
    i = 0
    while i < 80:    
        ouders.append(random.choice(beste))
        i = i + 1

    j = 0
    while j < 40:
        ouders.append(random.choice(slechtste))
        j = j + 1
    return ouders


# In[128]:


def kinderen_maken(ouders):
    grenzen = [(442, 1448), (754, 1067), (896, 1689), (3, 6), (234, 810), 
           (270, 787), (90, 112), (33, 154), (3, 11), (100, 159), 
           (661, 1847), (895, 1425), (755, 1155), (0, 0), (0, 0),
           (0, 0), (0, 0), (0, 0), (0, 0), (14, 32),
           (0, 0), (0, 0), (29, 61), (0, 0), (33, 34)]
    
    kinderen = []
    while len(ouders) != 0:
        parent1 = random.choice(ouders)
        ouders.remove(parent1)
        parent2 = random.choice(ouders)
        ouders.remove(parent2)
        for k in range(2):
            kind = []
            for i, g in zip(range(25), grenzen):
                if random.randint(0, 10) == 1:
                    kind.append(random.uniform(g[0], g[1]))
                    i = i + 1
                else:
                    kind.append(random.choice([parent1[i], parent2[i]]))
            kinderen.append(kind)
            k = k + 1
    return kinderen


# In[129]:


startoplossing = startoplossing()
# print(f"Startoplossing: {startoplossing}\n")

startpopulatie = startpopulatie(startoplossing)
# print(f"Startpopulatie: {startpopulatie}\n")


# In[130]:


def optimalisatie(startpopulatie):

    iteraties = 0
    while iteraties < 5:
        populatie = [tuple(i[0]) for i in startpopulatie]
        ouders = ouders_maken(populatie)
        populatie = [i for i in populatie[0:100]]
        kinderen = kinderen_maken(ouders)
        for a in kinderen:
            populatie.append(tuple(a))
        for x in range(len(populatie)):
            populatie[x] = (list(populatie[x]), uitkomsten(populatie[x]))
        populatie.sort(key=lambda uitkomst: uitkomst[1])
        iteraties = iteraties + 1
    populatie = [tuple(i[0]) for i in populatie]

    return populatie


# In[131]:


populatie = optimalisatie(startpopulatie)
# print(f"Populatie: {populatie}")


# In[132]:


def pareto_populatie(populatie):

    pareto_populatie = [i for i in populatie]
    
    for pareto in populatie:
        dominate = False
        uitkomsten_pareto = [kosten(pareto), mki(pareto)]
        for sol in pareto_populatie:
            if dominates(uitkomsten_pareto, [kosten(sol), mki(sol)]):
#                 st.markdown(f"pareto {pareto} dominates sol {sol}")
                pareto_populatie.remove(sol)
            if dominates([kosten(sol), mki(sol)], uitkomsten_pareto):
#                 st.markdown(f"pareto {pareto} dominates sol {sol}")
                dominate = True
        if dominate:
            if pareto in pareto_populatie:
                pareto_populatie.remove(pareto)
    return pareto_populatie


# In[133]:


populatie_pareto = pareto_populatie(populatie)
# print(f"Pareto {populatie_pareto}")


# In[164]:


f1_kosten = []
f2_mki = []
pareto =[]

for oplossing in populatie:
    f1_kosten.append(kosten(oplossing))
    f2_mki.append(mki(oplossing))
    pareto.append("nee")

dict = {'Oplossing': populatie, 'Kosten': f1_kosten, 'Milieukosten': f2_mki, 'Pareto': pareto} 

df = pd.DataFrame(dict)
df.loc[df['Oplossing'].isin(populatie_pareto), 'Pareto'] = 'ja'

nieuwe_rij = {'Oplossing': (442.50, 754.76, 896.78, 3.18, 234.85, 270.62, 90.92, 33.69, 3.44, 100.20, 661.43, 
                            895.78, 755.53, 0, 0, 0, 0, 0, 0, 14.16, 0, 0, 29.51, 0, 33.57), 'Kosten': 1265997.64, 
              'Milieukosten': 16541.15, 'Pareto': 'optimaal'}

# Toevoegen van de nieuwe rij
df = df._append(nieuwe_rij, ignore_index=True)

# df.head()
optimaal = nieuwe_rij.get("Oplossing")


# In[ ]:


st.markdown("**Optimale oplossing**")


# In[135]:


fig = px.scatter(df, x='Milieukosten', y='Kosten', color = 'Pareto', color_discrete_map={'ja': 'blue', 'nee': 'green', 'optimaal': 'red'}, hover_data={"Oplossing": True})

st.plotly_chart(fig)


# In[ ]:


if st.button('Herlaad pagina'):
    st.experimental_rerun()


# In[ ]:





# In[151]:


# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd

# # Voorbeeld data
# data = {
#     'productgroepen': ['Product A', 'Product B', 'Product C'],
#     'min_waarden': [10, 15, 20],
#     'max_waarden': [30, 25, 35],
#     'optimaal_waarden': [20, 20, 30]
# }

# df = pd.DataFrame(data)

# # Maak de min-max balken met Plotly Express
# fig = px.bar(
#     df,
#     x=df['max_waarden'] - df['min_waarden'],
#     y='productgroepen',
#     orientation='h',
#     range_x=[0, max(df['max_waarden'])+10],
#     labels={'x': 'Waarden', 'y': 'Productgroepen'},
#     title='Productgroepen met Min-Max en Optimaal waarden'
# )

# # Voeg de optimale waarden toe met Plotly Express
# optimal_fig = px.scatter(
#     df,
#     x='optimaal_waarden',
#     y='productgroepen',
#     color_discrete_sequence=['rgba(246, 78, 139, 1.0)'],
#     size=[10]*len(df),
#     labels={'x': 'Waarden', 'y': 'Productgroepen'}
# )

# # Voeg de scatter plot toe aan de bar plot
# for trace in optimal_fig.data:
#     fig.add_trace(trace)


# # Toon de figuur
# fig.show()


# In[154]:


# import plotly.express as px
# import pandas as pd

# # Voorbeeld data
# data = {
#     {'Productgroep': ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', 
#                       '28 Hoofddraagconstructie', '31 Buitenkozijnen, -ramen, -deuren, en -puien', 
#                       '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', '34 Balustrades en leuningen', 
#                       '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '64 Vaste gebouwvoorziening',
#                       '73 Keuken', '90 Terreininrichting'],
#     'min_waarden': [442, 754, 896, 3, 234, 270, 90, 33, 3, 100, 661, 895, 755, 14, 29, 33],
#     'max_waarden': [1448, 1067, 1689, 6, 810, 787, 112, 154, 11, 159, 1847, 1425, 1155, 32, 61, 34],
#     'optimaal_waarden': [optimaal[0], optimaal[1], optimaal[2], optimaal[3], optimaal[4], optimaal[5], 
#                          optimaal[6], optimaal[7], optimaal[8], optimaal[9], optimaal[10], optimaal[11], 
#                         optimaal[12], optimaal[19], optimaal[22], optimaal[24]]
# }

# df = pd.DataFrame(data)

# # Maak de data voor de bar plot
# df['length'] = df['max_waarden'] - df['min_waarden']
# df['min_point'] = df['min_waarden']

# # Maak de bar plot met Plotly Express
# fig = px.bar(df, 
#              x=['min_point', 'length'],  # Beginpunt en lengte van de balken
#              y='productgroepen',
#              color_discrete_sequence=['rgba(58, 71, 80, 0.6)', 'rgba(58, 71, 80, 0.6)'],  # Kleur van de balken
#              orientation='h',
#              title='Productgroepen met Min-Max en Optimaal waarden',
#              labels={'x': 'Waarden', 'y': 'Productgroepen'},
#              category_orders={"productgroepen": list(df["productgroepen"])}
#             )

# # Voeg de optimale waarden toe
# fig.add_trace(px.scatter(df, x='optimaal_waarden', y='productgroepen', color_discrete_sequence=['rgba(246, 78, 139, 1.0)']).data[0])

# # Toon de figuur
# fig.show()


# In[168]:


# import plotly.express as px
# import pandas as pd

# # Voorbeeld data
# data = {
#     'Productgroep': ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', 
#                       '28 Hoofddraagconstructie', '31 Buitenkozijnen, -ramen, -deuren, en -puien', 
#                       '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', '34 Balustrades en leuningen', 
#                       '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '64 Vaste gebouwvoorziening',
#                       '73 Keuken', '90 Terreininrichting'],
#     'min_waarden': [442, 754, 896, 3, 234, 270, 90, 33, 3, 100, 661, 895, 755, 14, 29, 33],
#     'max_waarden': [1448, 1067, 1689, 6, 810, 787, 112, 154, 11, 159, 1847, 1425, 1155, 32, 61, 34],
#     'optimaal_waarden': [optimaal[0], optimaal[1], optimaal[2], optimaal[3], optimaal[4], optimaal[5], 
#                          optimaal[6], optimaal[7], optimaal[8], optimaal[9], optimaal[10], optimaal[11], 
#                         optimaal[12], optimaal[19], optimaal[22], optimaal[24]]
# }


# df1 = pd.DataFrame(data)

# # Maak de data voor de bar plot
# df1['length'] = df1['max_waarden'] - df1['min_waarden']
# df1['min_point'] = df1['min_waarden']

# # Maak de bar plot met Plotly Express
# fig = px.bar(df1, 
#              x=['min_point', 'length'],  # Beginpunt en lengte van de balken
#              y='Productgroep',
#              color_discrete_sequence=['rgba(0,0,0,0)', 'rgba(58, 71, 80, 0.6)'],  # Kleur van de balken
#              orientation='h',
#              title='Productgroepen met Min-Max en Optimaal waarden',
#              labels={'x': 'Waarden', 'y': 'Productgroepen'},
#              category_orders={"Productgroep": list(df1["Productgroep"])}
#             )

# # Voeg de optimale waarden toe
# fig.add_trace(px.scatter(df1, x='optimaal_waarden', y='Productgroep', color_discrete_sequence=['rgba(246, 78, 139, 1.0)']).data[0])

# # Toon de figuur
# fig.show()


# In[170]:


# import plotly.express as px
# import pandas as pd

# # Voorbeeld data
# data = {
#     'Productgroep': ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', 
#                       '28 Hoofddraagconstructie', '31 Buitenkozijnen, -ramen, -deuren, en -puien', 
#                       '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', '34 Balustrades en leuningen', 
#                       '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '64 Vaste gebouwvoorziening',
#                       '73 Keuken', '90 Terreininrichting'],
#     'min_waarden': [442, 754, 896, 3, 234, 270, 90, 33, 3, 100, 661, 895, 755, 14, 29, 33],
#     'max_waarden': [1448, 1067, 1689, 6, 810, 787, 112, 154, 11, 159, 1847, 1425, 1155, 32, 61, 34],
#     'optimaal_waarden': [optimaal[0], optimaal[1], optimaal[2], optimaal[3], optimaal[4], optimaal[5], 
#                          optimaal[6], optimaal[7], optimaal[8], optimaal[9], optimaal[10], optimaal[11], 
#                         optimaal[12], optimaal[19], optimaal[22], optimaal[24]]
# }

# df1 = pd.DataFrame(data)

# # Selecteer alleen de eerste productgroep
# df1_first = df1.head(1)

# # Maak de data voor de bar plot
# df1_first['length'] = df1_first['max_waarden'] - df1_first['min_waarden']
# df1_first['min_point'] = df1_first['min_waarden']

# # Maak de bar plot met Plotly Express
# fig = px.bar(df1_first, 
#              x=['min_point', 'length'],  # Beginpunt en lengte van de balken
#              y='Productgroep',
#              color_discrete_sequence=['rgba(0,0,0,0)', 'rgba(58, 71, 80, 0.6)'],  # Kleur van de balken
#              orientation='h',
#              title='Productgroepen met Min-Max en Optimaal waarden',
#              labels={'x': 'Waarden', 'y': 'Productgroepen'},
#              category_orders={"Productgroep": list(df1_first["Productgroep"])}
#             )

# # Voeg de optimale waarden toe
# fig.add_trace(px.scatter(df1_first, x='optimaal_waarden', y='Productgroep', color_discrete_sequence=['rgba(246, 78, 139, 1.0)']).data[0])

# # Pas de hoogte van de grafiek aan
# fig.update_layout(height=300)

# # Toon de figuur
# fig.show()


# In[ ]:


data = {
    'Productgroep': ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', 
                      '28 Hoofddraagconstructie', '31 Buitenkozijnen, -ramen, -deuren, en -puien', 
                      '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', '34 Balustrades en leuningen', 
                      '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '64 Vaste gebouwvoorziening',
                      '73 Keuken', '90 Terreininrichting'],
    'code': ['21', '22', '23', '24', '27', '28', '31', '32', '33', '34', '42', '43', '45', '64','73', '90'],
    'min_waarden': [442, 754, 896, 3, 234, 270, 90, 33, 3, 100, 661, 895, 755, 14, 29, 33],
    'max_waarden': [1448, 1067, 1689, 6, 810, 787, 112, 154, 11, 159, 1847, 1425, 1155, 32, 61, 34],
    'optimaal_waarden': [optimaal[0], optimaal[1], optimaal[2], optimaal[3], optimaal[4], optimaal[5], 
                         optimaal[6], optimaal[7], optimaal[8], optimaal[9], optimaal[10], optimaal[11], 
                        optimaal[12], optimaal[19], optimaal[22], optimaal[24]]
}

df = pd.DataFrame(data)


for productgroep in df['Productgroep']:

    # Selecteer de data voor de huidige productgroep
    df_productgroep = df[df['Productgroep'] == productgroep]

    fig = px.bar(df_productgroep, x='max_waarden', y='code', base = 'min_waarden', 
                 color_discrete_sequence=['rgba(58, 71, 80, 0.6)'], title=f'{productgroep} ')
    
    fig.add_trace(px.scatter(df_productgroep, x='optimaal_waarden', y='code', 
                             color_discrete_sequence=['rgba(246, 78, 139, 1.0)'], labels={'x': ''}, marker_size=12).data[0])

    fig.update_layout(height=250)

    fig.update_yaxes(visible=False, showticklabels=False)

    st.plotly_chart(fig)


# In[ ]:


# import plotly.express as px
# import pandas as pd
# import streamlit as st

# # Voorbeeld data
# data = {
#     'Productgroep': ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', 
#                       '28 Hoofddraagconstructie', '31 Buitenkozijnen, -ramen, -deuren, en -puien', 
#                       '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', '34 Balustrades en leuningen', 
#                       '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '64 Vaste gebouwvoorziening',
#                       '73 Keuken', '90 Terreininrichting'],
#     'min_waarden': [442, 754, 896, 3, 234, 270, 90, 33, 3, 100, 661, 895, 755, 14, 29, 33],
#     'max_waarden': [1448, 1067, 1689, 6, 810, 787, 112, 154, 11, 159, 1847, 1425, 1155, 32, 61, 34],
#     'optimaal_waarden': [optimaal[0], optimaal[1], optimaal[2], optimaal[3], optimaal[4], optimaal[5], 
#                          optimaal[6], optimaal[7], optimaal[8], optimaal[9], optimaal[10], optimaal[11], 
#                         optimaal[12], optimaal[19], optimaal[22], optimaal[24]]
# }

# df = pd.DataFrame(data)

# # Loop over elke productgroep
# for productgroep in df['Productgroep']:

#     # Selecteer de data voor de huidige productgroep
#     df_productgroep = df[df['Productgroep'] == productgroep]
    
#     # Maak de data voor de bar plot
#     df_productgroep['length'] = df_productgroep['max_waarden'] - df_productgroep['min_waarden']
#     df_productgroep['min_point'] = df_productgroep['min_waarden']
    
#     # Maak de bar plot met Plotly Express
#     fig = px.bar(df_productgroep, 
#                  x=['length'],  # Beginpunt en lengte van de balken
#                  y='Productgroep',
#                  color_discrete_sequence=['rgba(58, 71, 80, 0.6)'],  # Kleur van de balken
#                  orientation='h',
#                  title=f'{productgroep} ',
#                  labels={'x': '', 'y': ''}, 
#                 base = 'min_point')
    
#     fig.update_xaxis(range=[df_productgroep['min_waarden'].min(), df_productgroep['max_waarden'].max()])  # Stel de range in van 1 tot 5

    
#     # Voeg de optimale waarden toe
#     fig.add_trace(px.scatter(df_productgroep, x='optimaal_waarden', y='Productgroep', color_discrete_sequence=['rgba(246, 78, 139, 1.0)'], size_max=15, labels={'x': ''}).data[0])

#     # Pas de hoogte van de grafiek aan
#     fig.update_layout(height=250)

    
#     # Voeg witruimte toe aan beide kanten van de x-as
# #     min_value = df_productgroep['min_waarden'].min()
# #     max_value = df_productgroep['max_waarden'].max()
# #     fig.update_xaxes(tickvals=[min_value, max_value], ticktext=[min_value, max_value])

#     fig.update_yaxes(visible=False, showticklabels=False)
    
#     # Verwijder de legenda
#     fig.update_layout(showlegend=False)

#     # Toon de figuur met Streamlit
#     st.plotly_chart(fig)


# In[ ]:





# In[ ]:





# In[ ]:




