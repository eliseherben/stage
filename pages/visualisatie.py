#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import timedelta


# In[ ]:


st.page_link("simplex.py", label="Homepagina")
st.page_link("pages/optimalisatie3.py", label="Terug naar optimalisatie")
st.page_link("pages/input.py", label="Terug naar input")
st.title("**Visualisatie oplossingen**")


# In[ ]:


df = st.session_state.oplossingen
st.markdown(st.session_state.doelwaardes)

kolommen_te_uitsluiten = ['eenheid', 'kosten', 'circulair', 'optimalisatie', 
                          'constant', 'productgroep', 'code', 'minimaal', 'maximaal']
kolommen_te_selecteren = [kolom for kolom in df.columns if kolom not in kolommen_te_uitsluiten]
geselecteerde_kolommen = st.multiselect('Selecteer oplossingen', kolommen_te_selecteren)

for productgroep in df['productgroep']:
    # Selecteer de data voor de huidige productgroep
    df_productgroep = df[df['productgroep'] == productgroep]
    
    st.dataframe(df_productgroep)
    
    # Selecteer alle kolommen behalve de uitgesloten kolommen
    df_geselecteerd = df_productgroep.drop(columns=kolommen_te_uitsluiten)

    df_productgroep['aantal'] = df_productgroep['maximaal'] - df_productgroep['minimaal']
    
    fig = px.bar(df_productgroep, x='aantal', y='code', base = 'minimaal', 
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title=f'{productgroep} ')
    
    if df_productgroep.columns[11] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[11], y='code', 
                                 color_discrete_sequence=['rgba(147, 16, 126, 1.0)'], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 1']).data[0])
    
    if df_productgroep.columns[12] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[12], y='code', 
                             color_discrete_sequence=['rgba(0, 158, 224, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 2']).data[0])
    
    if df_productgroep.columns[13] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[13], y='code', 
                             color_discrete_sequence=['rgba(241, 142, 47, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 3']).data[0])
    
    if df_productgroep.columns[14] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[14], y='code', 
                             color_discrete_sequence=['rgba(151, 191, 13, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 4']).data[0])
   
    if df_productgroep.columns[15] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[15], y='code', 
                             color_discrete_sequence=['rgba(255, 211, 0, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 4']).data[0])
        
    if df_productgroep.columns[9] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x='huidige_waarden', y='code', 
                             color_discrete_sequence=['rgba(212, 0, 60, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['huidig']).data[0])
        
    fig.update_layout(height=250)

    fig.update_yaxes(visible=False, showticklabels=False)

    st.plotly_chart(fig)



# In[ ]:


df2 = pd.DataFrame(st.session_state.doelwaardes, columns=['oplossing', 'kosten', 'milieukosten'])

df_k = df2[['oplossing', 'kosten']]
st.dataframe(df_k)
df_k[df_k.iloc[5, 0]] = df_k.iloc[5, 0]
st.dataframe(df_k)

st.dataframe(df2)
# st.dataframe(df_t)

df_t.columns = df_t.iloc[0]
df_t = df_t[1:]

df_t['aantal'] = df_t['maximaal'] - df_t['minimaal']
fig = px.bar(df_t, x='aantal', y='kosten', base = 'minimaal', 
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'])

# Maak de bar plot voor kosten
fig_kosten = px.bar(df2, x='oplossing', y='kosten', title='Kosten')

# Maak de bar plot voor milieukosten
fig_milieukosten = px.bar(df2, x='oplossing', y='milieukosten', title='Milieukosten')

# Toon de grafieken
st.plotly_chart(fig_kosten)
st.plotly_chart(fig_milieukosten)

