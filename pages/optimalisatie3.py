#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import pulp as pl
import plotly.express as px


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


# In[ ]:


st.markdown("**Primair thema**")
st.selectbox("Welke thema heeft prioriteit in dit project?", 
            ("Circulair", "Budget"), 
            index = None, 
            placeholder='selecteer een thema...', key='_doelstelling', on_change=set_doelstelling)


# In[3]:


data = pd.read_csv("dataframe.csv", sep=';', decimal = ',')
data['minimaal'] = data['minimaal'] * st.session_state.appartementen
data['maximaal'] = data['maximaal'] * st.session_state.appartementen

missing_values = data.isna()

print(missing_values)

# data.head()


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


# In[ ]:


# if st.session_state.projectbestand is None:
#     st.markdown("upload een bestand")
# else: 
# # Creëer een LP probleem
#     prob = pl.LpProblem("Eigen Haard", pl.LpMinimize)

#     variabelen = {}
#     for index, row in data.iterrows():
#         variabelen[row["productgroep"]] = pl.LpVariable(row["productgroep"], lowBound = 0)

#     lp_variabelen = []
#     for key, value in variabelen.items():
# #             st.markdown(f"{key} = {value}")
#         lp_variabelen.append((key, value))

#     #Impact themas op productgroepen
#     variabelen_circulair = []
#     impact_circulair = []
#     for i in range(len(lp_variabelen)):
#         if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 5]):
#             variabelen_circulair.append(lp_variabelen[i][1])
#             impact_circulair.append(data.iloc[i, 5])

#     circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
#     st.markdown(circulair)

#     variabelen_budget = []
#     impact_budget = []
#     for i in range(len(lp_variabelen)):
#         if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]):
#             variabelen_budget.append(lp_variabelen[i][1])
#             impact_budget.append(data.iloc[i, 4])
    
#     budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
#     st.markdown(budget)

# #     for i in range(len(lp_variabelen)):
# #         if pd.isna(data.iloc[i, 2]) and pd.isna(data.iloc[i, 3]):
    
#     prob += 0.3 * circulair + 0.7 * budget

#     for i in range(len(lp_variabelen)):
#         if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#             prob += lp_variabelen[i][1] >= data.iloc[i, 2]
#             prob += lp_variabelen[i][1] <= data.iloc[i, 3]
            
#     prob +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) == st.session_state.budget

#     # Los het probleem op
#     status = prob.solve()

#     # Maak een lege lijst om de variabelen en hun waarden op te slaan
#     variabelen_waarden = []

#     # Voeg de variabelen en hun waarden toe aan de lijst
#     for key, var in lp_variabelen:
#         variabelen_waarden.append((key, var.varValue))

#     # Maak een DataFrame van de lijst
#     df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])

#     st.markdown(f"Status van de oplossing: {pl.LpStatus[status]}")
#     st.markdown(f"Waarde van de doelfunctie: {prob.objective.value()}")


# In[ ]:


# if st.session_state.projectbestand is None:
#     st.markdown("upload een bestand")
# else: 
# # Creëer een LP probleem
#     prob1 = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)

#     variabelen = {}
#     for index, row in data.iterrows():
#         variabelen[row["productgroep"]] = pl.LpVariable(row["productgroep"], lowBound = 0)

#     lp_variabelen = []
#     for key, value in variabelen.items():
# #             st.markdown(f"{key} = {value}")
#         lp_variabelen.append((key, value))

#     #Impact themas op productgroepen
#     if st.session_state.doelstelling == 'Circulair':
#         variabelen_circulair = []
#         impact_circulair = []
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5]):
#                 variabelen_circulair.append(lp_variabelen[i][1])
#                 impact_circulair.append(data.iloc[i, 5])

#         circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
#         st.markdown(circulair)
        
#         prob1 += circulair
        
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
            
#         status = prob1.solve()
        
#         Z1_opt = pl.value(prob1.objective)
        
#         st.markdown(f"Status van de oplossing: {pl.LpStatus[status]}")
#         st.markdown(f"Waarde van de doelfunctie: {prob1.objective.value()}")
        
#         prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
            
#         variabelen = {}
#         for index, row in data.iterrows():
#             variabelen[row["productgroep"]] = pl.LpVariable(row["productgroep"], lowBound = 0)

#         lp_variabelen = []
#         for key, value in variabelen.items():
#     #             st.markdown(f"{key} = {value}")
#             lp_variabelen.append((key, value))
        
#         variabelen_budget = []
#         impact_budget = []
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5]):
#                 variabelen_budget.append(lp_variabelen[i][1])
#                 impact_budget.append(data.iloc[i, 4])

#         budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
#         st.markdown(budget)

#         prob2 += budget
        
#         prob2 += pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair))) <= Z1_opt
#         st.markdown(pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair))))
#         st.markdown(Z1_opt)
        
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 st.markdown(lp_variabelen[i][1])
#                 st.markdown(data.iloc[i, 2])
#                 st.markdown(data.iloc[i, 3])
#                 prob2 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob2 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
#             # Los het probleem op
#         status = prob2.solve()

#         # Maak een lege lijst om de variabelen en hun waarden op te slaan
#         variabelen_waarden = []

#         # Voeg de variabelen en hun waarden toe aan de lijst
#         for key, var in lp_variabelen:
#             variabelen_waarden.append((key, var.varValue))

#         # Maak een DataFrame van de lijst
#         df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])

#         st.markdown(f"Status van de oplossing: {pl.LpStatus[status]}")
#         st.markdown(f"Waarde van de doelfunctie: {prob2.objective.value()}")
        
    
#     if st.session_state.doelstelling == 'Budget':
#         variabelen_budget = []
#         impact_budget = []
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5]):
#                 variabelen_budget.append(lp_variabelen[i][1])
#                 impact_budget.append(data.iloc[i, 4])

#         budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
#         st.markdown(budget)
        
#         prob1 += budget
        
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
            
#         prob1.solve()
        
#         Z1_opt = pl.value(prob1.objective)
        
#         prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
            
#         variabelen = {}
#         for index, row in data.iterrows():
#             variabelen[row["productgroep"]] = pl.LpVariable(row["productgroep"], lowBound = 0)

#         lp_variabelen = []
#         for key, value in variabelen.items():
#     #             st.markdown(f"{key} = {value}")
#             lp_variabelen.append((key, value))
        
#         variabelen_circulair = []
#         impact_circulair = []
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5]):
#                 variabelen_circulair.append(lp_variabelen[i][1])
#                 impact_circulair.append(data.iloc[i, 5])

#         circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
#         st.markdown(circulair)
        
#         prob2 += circulair
        
#         prob2 += pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) <= Z1_opt
        
#         for i in range(len(lp_variabelen)):
#             if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
#                 prob2 += lp_variabelen[i][1] >= data.iloc[i, 2]
#                 prob2 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
#             # Los het probleem op
#         status = prob2.solve()

#         # Maak een lege lijst om de variabelen en hun waarden op te slaan
#         variabelen_waarden = []

#         # Voeg de variabelen en hun waarden toe aan de lijst
#         for key, var in lp_variabelen:
#             variabelen_waarden.append((key, var.varValue))

#         # Maak een DataFrame van de lijst
#         df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])

#         st.markdown(f"Status van de oplossing: {pl.LpStatus[status]}")
#         st.markdown(f"Waarde van de doelfunctie: {prob2.objective.value()}")


# In[ ]:


import streamlit as st
import pulp as pl
import pandas as pd

# Controleer of het projectbestand is geüpload
if st.session_state.projectbestand is None:
    st.markdown("Upload een bestand")
else:
    # Definieer de LP variabelen
    variabelen = {row["productgroep"]: pl.LpVariable(row["productgroep"], lowBound=0) for index, row in data.iterrows()}

    # Maak de variabelenlijst
    lp_variabelen = [(key, value) for key, value in variabelen.items()]

    # Functie om het eerste doelstellingprobleem op te lossen
    if st.session_state.doelstelling == 'Circulair':
        prob1 = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 5])]

        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        st.markdown(f"Circulair doelstelling: {circulair}")

        prob1 += circulair

        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]

        status = prob1.solve()
        st.markdown(f"Status van de oplossing (Primary): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (Primary): {prob1.objective.value()}")

        prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 4])]

        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        st.markdown(f"Budget doelstelling: {budget}")

        prob2 += budget
        prob2 += pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair))) <= Z1_opt
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob2 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob2 += lp_variabelen[i][1] <= data.iloc[i, 3]

#         prob2 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) == st.session_state.budget

        status = prob2.solve()
        st.markdown(f"Status van de oplossing (Secondary): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (Secondary): {prob2.objective.value()}")

        # Maak een DataFrame van de variabelen en hun waarden
        variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
        df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])
        st.dataframe(df)
        
    if st.session_state.doelstelling == 'Budget':
        prob1 = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 4])]

        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        st.markdown(f"Budget doelstelling: {budget}")

        prob1 += budget
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
                
        status = prob1.solve()
        st.markdown(f"Status van de oplossing (Primary): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (Primary): {prob1.objective.value()}")
        
        prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
        
        # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 5])]

        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        st.markdown(f"Circulair doelstelling: {circulair}")

        prob2 += circulair
        prob2 += pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) <= Z1_opt
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
        status = prob2.solve()
        st.markdown(f"Status van de oplossing (Secondary): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (Secondary): {prob2.objective.value()}")

        # Maak een DataFrame van de variabelen en hun waarden
        variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
        df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])
        st.dataframe(df)


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")

    for index, row in df.iterrows():
        st.markdown(f"- Binnen de productgroep {row['Productgroep']} moet er {row['Waarde']} eenheid besteed worden")

