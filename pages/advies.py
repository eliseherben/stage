#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[ ]:


st.title("Advies")
st.markdown("Dit advies is gebasseerd op de volgende gegevens:")
st.markdown(f"* het projectbestand met de naam {st.session_state.name}")

