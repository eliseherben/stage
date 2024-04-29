#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd


# In[ ]:


st.write("#")
st.write("#")
st.title("Advies")
st.markdown("Dit advies is gebasseerd op de volgende gegevens:")
st.markdown("**Projectbestand**")
st.markdown(f"Het projectbestand met de naam {st.session_state.name}")
st.dataframe(st.session_state.dataframe)
st.markdown('''De ranking van de thema's op de volgende manier:
1. Woonbeleving
2. Onderhoud
3. Budget
4. Kwaliteit
5. Woonbeleving''')

st.markdown("**'+' opties**")
st.markdown("Hieronder zijn de '+' opties weergegeven van de productgroepen waarbij het aandeel in het project het grootst is. ")

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
    

with st.expander("'+' opties voor productgroep 31. Buitenkozijnen, -ramen, -deuren en -puien"):
    st.markdown('''
    ###Impact op circulair
    
    **ALGEMEEN: beglazing**
    
    Beglazing:
    - circulaire beglazing (minimun van 50%, waar mogelijk meer);
    - Meerbladig isolerende beglazing, volgens NEN 2608+a01, minimaal HR++ glas. 
        
    **BUITENWANDOPENINGEN, HOUT: schilderwerk**
    
    Schilderwerk: Fabrikant: Sigma, Sikkens of gelijkwaardig. 
    
    ##Impact op budget
    
    **ALGEMEEN: natuursteen buitendorpel met neut**
    
    Natuursteen buitendorpel met neut: 
    - van hardsteen. 
    - geprofileerd met ingelijmde neuten en aan bovenzijde hoeken met facetkant.
    - onder de buitendeurkozijnen van de algemene ruimten op de begane grond. 
    
    **ALGEMEEN:  Natuursteen vensterbank van marmercomposiet:**
    
    Natuursteen vensterbank van marmercomposiet:   
    - van marmercomposiet (96% natuursteen, 4% kunsthars) - dikte 20 mm.  - zichtzijden fijn gezoet. 
    
    **Impact op kwaliteit**
    
    **ALGEMEEN: natuursteen buitendorpel met neut**
    
    Natuursteen buitendorpel met neut: 
    - van hardsteen. 
    - geprofileerd met ingelijmde neuten en aan bovenzijde hoeken met facetkant.
    - onder de buitendeurkozijnen van de algemene ruimten op de begane grond. 
    
    **ALGEMEEN:  Natuursteen vensterbank van marmercomposiet:**
    
    Natuursteen vensterbank van marmercomposiet:   
    - van marmercomposiet (96% natuursteen, 4% kunsthars) - dikte 20 mm.  - zichtzijden fijn gezoet.
    
    ''')


# In[ ]:


st.page_link("simplex.py", label="Homepagina")

