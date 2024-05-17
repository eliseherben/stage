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
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair)))
        st.markdown(f"Circulair doelstelling: {circulair}")

        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        st.markdown(f"Budget doelstelling: {budget}")
        
        variabelen_beginoplossing = [1500, 945, 1400, 5, 250, 800, 93, 157, 5, 1900, 1500, 900, 23, 61, 35]
        beginoplossing = pl.lpSum(variabelen_beginoplossing[i] * impact_budget[i] for i in range(len(variabelen_beginoplossing))) 
        
        doelfunctie = (circulair - beginoplossing)**2
        
        prob1 += doelfunctie

        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
                
#         prob1 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) <= st.session_state.budget
            
        status = prob1.solve()
        st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (circulair): {prob1.objective.value()}")
        Z1_opt = pl.value(prob1.objective)
        
        prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
        
        doelfunctie = (budget - beginoplossing)**2
        
        prob2 += doelfunctie
        
        prob2 += pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair))) <= Z1_opt
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob2 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob2 += lp_variabelen[i][1] <= data.iloc[i, 3]

#         prob2 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) <= st.session_state.budget

        status = prob2.solve()
        st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (budget): {prob2.objective.value()}")

        # Maak een DataFrame van de variabelen en hun waarden
        variabelen_waarden = [(key, var.varValue) for key, var in lp_variabelen]
        df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])
        st.dataframe(df)
        
    if st.session_state.doelstelling == 'Budget':
        prob1 = pl.LpProblem("Eerste doelstelling", pl.LpMinimize)
        
        variabelen_budget = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_budget = [data.iloc[i, 4] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

        budget = pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget)))
        st.markdown(f"Budget doelstelling: {budget}")
         
        variabelen_beginoplossing = [1500, 945, 1400, 5, 250, 800, 93, 157, 5, 1900, 1500, 900, 23, 61, 35]
        beginoplossing = pl.lpSum(variabelen_beginoplossing[i] * impact_budget[i] for i in range(len(variabelen_beginoplossing))) 
        
        doelfunctie = (budget - beginoplossing)**2
        
        prob1 += doelfunctie
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob1 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob1 += lp_variabelen[i][1] <= data.iloc[i, 3]
                
#         prob1 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) == st.session_state.budget

        status = prob1.solve()
        st.markdown(f"Status van de oplossing (budget): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (budget): {prob1.objective.value()}")
        Z1_opt = pl.value(prob1.objective)
        
        prob2 = pl.LpProblem("Tweede doelstelling", pl.LpMinimize)
        
        # Impact themas op productgroepen
        variabelen_circulair = [lp_variabelen[i][1] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]
        impact_circulair = [data.iloc[i, 5] for i in range(len(lp_variabelen)) if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]) and pd.notna(data.iloc[i, 4]) and pd.notna(data.iloc[i, 5])]

        circulair = pl.lpSum(variabelen_circulair[i] * impact_circulair[i] for i in range(len(variabelen_circulair))) 
        st.markdown(f"Circulair doelstelling: {circulair}")
        
        variabelen_beginoplossing = [1500, 945, 1400, 5, 250, 800, 93, 157, 5, 1900, 1500, 900, 23, 61, 35]
        beginoplossing = pl.lpSum(variabelen_beginoplossing[i] * impact_circulair[i] for i in range(len(variabelen_beginoplossing))) 

        doelfunctie = (circulair - beginoplossing)**2
        
        prob2 += doelfunctie
        
        for i in range(len(lp_variabelen)):
            if pd.notna(data.iloc[i, 2]) and pd.notna(data.iloc[i, 3]):
                prob2 += lp_variabelen[i][1] >= data.iloc[i, 2]
                prob2 += lp_variabelen[i][1] <= data.iloc[i, 3]
        
#         prob2 +=  pl.lpSum(variabelen_budget[i] * impact_budget[i] for i in range(len(variabelen_budget))) == st.session_state.budget

        status = prob2.solve()
        st.markdown(f"Status van de oplossing (circulair): {pl.LpStatus[status]}")
        st.markdown(f"Waarde van de doelfunctie (circulair): {prob2.objective.value()}")

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

