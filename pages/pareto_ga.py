#!/usr/bin/env python
# coding: utf-8

# In[121]:


import streamlit as st
import random
import pandas as pd
import plotly.express as px


# In[ ]:


st.markdown("**Pareto oplossingen**")


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


# In[134]:


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


# In[135]:


fig = px.scatter(df, x='Milieukosten', y='Kosten', color = 'Pareto', color_discrete_map={'ja': 'blue', 'nee': 'green', 'optimaal': 'red'}, hover_data={"Oplossing": True})

st.plotly_chart(fig)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




