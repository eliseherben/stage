#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[ ]:


st.write("#")
st.write("#")
st.title("Advies")
st.markdown("Dit advies is gebasseerd op de volgende gegevens:")
st.markdown(f"* het projectbestand met de naam {st.session_state.name}")

with st.expander("'+' opties voor productgroep 21. Buitenwanden"):
    st.write('''**Kalkzandsteen lijmblok/-elementen:** 
- kalkzandsteen elementen met recyclaat (zoals bijvoorbeeld Caldubo);
- druksterkte: volgens opgave constructeur
- Oppervlaktegroep overeenkomstig STABU Standaard, hfst. 22, bijlage A: groep 2;
- lijmmortel: - volgens advies fabrikant/leverancier van de blokken. 
\nToebehoren:  - kimblokken. - lijmspouwankers, van roestvast staal, kwaliteit AISI 304, ø 4 mm. - veer-/stripankers van geperforeerd roestvast staal, kwaliteit AISI 304. ''')


# In[ ]:


st.page_link("simplex.py", label="Homepagina")

