#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pulp as pl


# In[ ]:


st.write("#")
st.title("Optimalisatie")
st.page_link("pages/advies.py", label="Naar advies")
st.page_link("simplex.py", label="Homepagina")


# In[ ]:


data = pd.read_csv("dataframe.csv", sep=';')
data.head()


# In[ ]:


if st.session_state.projectbestand is None:
    st.markdown("upload een bestand")
else: 
    budget = data.sort_values(by='kosten', ascending=False)
    
    st.markdown(
        f"""
        De productgroepen die het meeste impact maken op het thema 'budget':
        - {budget['productgroep'].iloc[0]}
        - {budget['productgroep'].iloc[0]}
        - {budget['productgroep'].iloc[0]}
        """
        )
    
    circulair = data.sort_values(by='circulair', ascending=False)
    
    st.markdown(
        f"""
        De productgroepen die het meeste impact maken op het thema 'budget':
        - {circulair['productgroep'].iloc[0]}
        - {circulair['productgroep'].iloc[0]}
        - {circulair['productgroep'].iloc[0]}
        """
        )

