#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from menu2 import menu_with_redirect
menu_with_redirect()


# In[ ]:


st.markdown("optimalisatie")


# In[ ]:


st.dataframe(st.session_state.file)


# In[ ]:


# if (onderhoud['impact onderhoud'].iloc[0] and onderhoud['impact onderhoud'].iloc[1] and onderhoud['impact onderhoud'].iloc[2]) > 0:
#     st.markdown('**Onderhoud**')
#     st.markdown(
#     f"""
#     De productgroepen die het meeste impact maken op het thema 'Onderhoud':
#     - {onderhoud['productgroep'].iloc[0]}
#     - {onderhoud['productgroep'].iloc[1]}
#     - {onderhoud['productgroep'].iloc[2]}
#     """
#     )
# if (circulair['impact circulair'].iloc[0] and circulair['impact circulair'].iloc[1] and circulair['impact circulair'].iloc[2]) > 0:
#     st.markdown('**Circulair**')
#     st.markdown(
#     f"""
#     De productgroepen die het meeste impact maken op het thema 'Duurzaam':
#     - {circulair['productgroep'].iloc[0]}
#     - {circulair['productgroep'].iloc[1]}
#     - {circulair['productgroep'].iloc[2]}
#     """
#     )    
# if (kwaliteit['impact kwaliteit'].iloc[0] and kwaliteit['impact kwaliteit'].iloc[1] and kwaliteit['impact kwaliteit'].iloc[2]) > 0:
#     st.markdown('**Kwaliteit**')
#     st.markdown(
#     f"""
#     De productgroepen die het meeste impact maken op het thema 'Kwaliteit':
#     - {kwaliteit['productgroep'].iloc[0]}
#     - {kwaliteit['productgroep'].iloc[1]}
#     - {kwaliteit['productgroep'].iloc[2]}
#     """
#     )
# if (budget['impact budget'].iloc[0] and budget['impact budget'].iloc[1] and budget['impact budget'].iloc[2]) > 0:
#     st.markdown('**Budget**')
#     st.markdown(
#     f"""
#     De productgroepen die het meeste impact maken op het thema 'Budget':
#     - {budget['productgroep'].iloc[0]}
#     - {budget['productgroep'].iloc[1]}
#     - {budget['productgroep'].iloc[2]}
#     """
#     )
# if (woonbeleving['impact woonbeleving'].iloc[0] and woonbeleving['impact woonbeleving'].iloc[1] and woonbeleving['impact woonbeleving'].iloc[2]) > 0:
#     st.markdown('**Woonbeleving**')
#     st.markdown(
#     f"""
#     De productgroepen die het meeste impact maken op het thema 'Woonbeleving':
#     - {woonbeleving['productgroep'].iloc[0]}
#     - {woonbeleving['productgroep'].iloc[1]}
#     - {woonbeleving['productgroep'].iloc[2]}
#     """
#     )

