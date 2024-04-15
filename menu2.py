#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[ ]:


def authenticated_menu():
    st.sidebar.page_link("simplex.py", label = "Input")
        
    if st.session_state.projectbestand is not None:
        st.sidebar.page_link("pages/optimalisatie2.py", label = "Optimalisatie")
        
def unauthenticated_menu():
    st.sidebar.page_link("simplex.py", label = "Input")
        
def menu():
    if "projectbestand" not in st.session_state or st.session_state.projectbestand is None:
        unauthenticated_menu()
        return
    authenticated_menu()
    
def menu_with_redirect():
    if "projectbestand" not in st.session_state or st.session_state.projectbestand is None:
        st.switch_page("simplex.py")
    menu()

