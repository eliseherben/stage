#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import timedelta


# In[ ]:


st.markdown("**Visualisatie oplossingen**")
st.page_link("simplex.py", label="Homepagina")
st.page_link("pages/optimalisatie3.py", label="Terug naar optimalisatie")
st.page_link("pages/input.py", label="Terug naar input")


# In[ ]:


df = st.session_state.oplossingen
st.markdown(df)

kolommen_te_uitsluiten = ['productgroep', 'code', 'minimaal', 'maximaal']
kolommen_te_selecteren = [kolom for kolom in df.columns if kolom not in kolommen_te_uitsluiten]
geselecteerde_kolommen = st.multiselect('Selecteer oplossingen', kolommen_te_selecteren)


for productgroep in df['productgroep']:
    # Selecteer de data voor de huidige productgroep
    df_productgroep = df[df['productgroep'] == productgroep]
    
    # Selecteer alle kolommen behalve de uitgesloten kolommen
    df_geselecteerd = df_productgroep.drop(columns=kolommen_te_uitsluiten)


    df_productgroep['length'] = df_productgroep['maximaal'] - df_productgroep['minimaal']
    
    fig = px.bar(df_productgroep, x='length', y='code', base = 'minimaal', 
                 color_discrete_sequence=['rgba(119, 118, 121, 0.1)'], title=f'{productgroep} ')
    
    if df_productgroep.columns[1] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[1], y='code', 
                                 color_discrete_sequence=['rgba(147, 16, 126, 1.0)'], labels={'x': ''}, 
                                 size=[10], symbol = ['oplossing 1']).data[0])
    
    if df_productgroep.columns[2] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[2], y='code', 
                             color_discrete_sequence=['rgba(0, 158, 224, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 2']).data[0])
    
    if df_productgroep.columns[3] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[3], y='code', 
                             color_discrete_sequence=['rgba(241, 142, 47, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 3']).data[0])
    
    if df_productgroep.columns[4] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[4], y='code', 
                             color_discrete_sequence=['rgba(151, 191, 13, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 4']).data[0])
   
    if df_productgroep.columns[5] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x=df_productgroep.columns[5], y='code', 
                             color_discrete_sequence=['rgba(255, 211, 0, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['oplossing 4']).data[0])
    
        
    if df_productgroep.columns[-2] in geselecteerde_kolommen:
        fig.add_trace(px.scatter(df_productgroep, x='huidige_waarden', y='code', 
                             color_discrete_sequence=['rgba(212, 0, 60, 1.0)'], labels={'x': ''}, 
                             size=[10], symbol = ['huidig']).data[0])
        
    fig.update_layout(height=250)

    fig.update_yaxes(visible=False, showticklabels=False)

    st.plotly_chart(fig)

