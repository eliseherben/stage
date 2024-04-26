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
    st.markdown('''
    **Impact op circulair**  
    
    **ALGEMEEN: isolatie (Isovlas of houtvezel)**  
    Isolatie, isovlas of houtvezel:
    - indien mogelijk Isovlas of houtvezel isolatie (zoals Gutex Thermoflex of gelijkwaardig) toepassen in buitenwanden.
        
    **BUITENWANDEN, ALGEMEEN: vochtkeringen**  
    Kunststof vochtkeringsstrook, loodververvanger:
    - waar mogelijk: loodvervanger toepassen met recyclaat (zoals bijvoorbeeld Leadax).
      
    **SPOUWWANDEN: baksteen met mortel**
    Steen: 
    - duurzaam alternatief: Wienerberger Ecobrick of gelijkwaardig;
    - dichtheid HD. 
    - maattolerantie categorie T2. 
    - maatspreiding categorie R1. 
    - actieve oplosbare zouten categorie S2.- vorst- en dooiweerstand categorie F2.  
    Mortel:  
    - prefab doorstrijkmortel volgens NEN-EN 998-2-10. 
    - mortel naar toepassing (klasse): G. 
    - morteldruksterkte (klasse): M 10. 
    - bindmiddel: cement CEM I en bouwkalk (NEN-EN 459-1-10). 
    Toebehoren: - spouwankers, van roestvast staal, 
    kwaliteit AISI 304, ø 4 mm. - veer-/stripankers vangeperforeerd roestvast staal, kwaliteit AISI 304. Voegvulling: voegvulling op rug.
        
    **SPOUWWANDEN: isolatie (Isovlas)**  
    Kalkzandsteen lijmblok/-elementen:
    - kalkzandsteen elementen met recyclaat (zoals bijvoorbeeld Caldubo);
    - druksterkte: volgens opgave constructeur
    - Oppervlaktegroep overeenkomstig STABU Standaard, hfst. 22, bijlage A: groep 2;
    - lijmmortel: - volgens advies fabrikant/leverancier van de blokken.  
    Toebehoren:  - kimblokken. - lijmspouwankers, van roestvast staal, kwaliteit AISI 304, ø 4 mm. - veer-/stripankers van geperforeerd roestvast staal, kwaliteit AISI 304. ''')


# In[ ]:


st.page_link("simplex.py", label="Homepagina")

