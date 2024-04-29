#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd


# In[ ]:


df = st.session_state.dataframe
df = df[df["norm / \n'+' optie"] == " '+' optie"]
df = df[['productgroep', 'element', 'specificatie', "norm / \n'+' optie", 
         "impact onderhoud", "impact circulair", "impact kwaliteit", "impact budget", "impact woonbeleving"]]
df = df.reset_index(drop=True)


# In[ ]:


st.markdown(
    """
    <style type="text/css" media="print">
      .page-break {
        page-break-after: always;
      }
      .center {
        text-align: center;
        margin: auto;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


# In[ ]:


st.write("#")
st.write("#")
st.title("Advies")
st.markdown("Dit advies is gebasseerd op de volgende gegevens:")
st.markdown("**Projectbestand**")
st.markdown(f'Het projectbestand met de naam "{st.session_state.name}"')
st.dataframe(st.session_state.dataframe)
st.markdown("**Rank**")
st.markdown('''De ranking van de thema's op de volgende manier:
1. Woonbeleving
2. Onderhoud
3. Budget
4. Kwaliteit
5. Woonbeleving''')


# In[ ]:


onderhoud = df[df['impact onderhoud'] == 'O']

if not onderhoud.empty:
    st.markdown("---")
    st.markdown("**Onderhoud '+' opties**")
    st.markdown('''Hieronder zijn de '+' opties weergegeven die impact hebben op onderhoud, 
                gesorteerd op de productgroepen die het meeste aandeel hebben binnen het project op basis van de optimalisatie. ''')

    productgroepen = onderhoud['productgroep'].unique()

    # Loop door elke productgroep en maak een expander voor elke productgroep
    for productgroep in productgroepen:
        productgroep_data = df[df['productgroep'] == productgroep]
        with st.expander(f"'+' opties voor productgroep {productgroep}"):
            # Print alle elementen en specificaties binnen de expander
            for index, row in productgroep_data.iterrows():
                element = row['element'].strip()
                st.markdown(f"**{element}**")
                st.markdown(f"{row['specificatie']}")


# In[ ]:


circulair = df[df['impact circulair'] == 'CD']

if not circulair.empty:
    st.markdown("---")
    st.markdown("**Circulaire '+' opties**")
    st.markdown('''Hieronder zijn de '+' opties weergegeven die impact hebben op circulair, 
                gesorteerd op de productgroepen die het meeste aandeel hebben binnen het project op basis van de optimalisatie ''')

    productgroepen = circulair['productgroep'].unique()

    # Loop door elke productgroep en maak een expander voor elke productgroep
    for productgroep in productgroepen:
        productgroep_data = df[df['productgroep'] == productgroep]
        with st.expander(f"'+' opties voor productgroep {productgroep}"):
            # Print alle elementen en specificaties binnen de expander
            for index, row in productgroep_data.iterrows():
                element = row['element'].strip()
                st.markdown(f"**{element}**")
                st.markdown(f"{row['specificatie']}")


# In[ ]:


kwaliteit = df[df['impact kwaliteit'] == 'K']

if not kwaliteit.empty:
    st.markdown("---")
    st.markdown("**Kwaliteit '+' opties**")
    st.markdown('''Hieronder zijn de '+' opties weergegeven die impact hebben op kwaliteit, 
                gesorteerd op de productgroepen die het meeste aandeel hebben binnen het project op basis van de optimalisatie. ''')

    productgroepen = kwaliteit['productgroep'].unique()

    # Loop door elke productgroep en maak een expander voor elke productgroep
    for productgroep in productgroepen:
        productgroep_data = df[df['productgroep'] == productgroep]
        with st.expander(f"'+' opties voor productgroep {productgroep}"):
            # Print alle elementen en specificaties binnen de expander
            for index, row in productgroep_data.iterrows():
                element = row['element'].strip()
                st.markdown(f"**{element}**")
                st.markdown(f"{row['specificatie']}")


# In[ ]:


budget = df[df['impact budget'] == 'B']

if not budget.empty:
    st.markdown("---")
    st.markdown("**Budget '+' opties**")
    st.markdown('''Hieronder zijn de '+' opties weergegeven die impact hebben op budget, 
                gesorteerd op de productgroepen die het meeste aandeel hebben binnen het project op basis van de optimalisatie. ''')

    productgroepen = budget['productgroep'].unique()

    # Loop door elke productgroep en maak een expander voor elke productgroep
    for productgroep in productgroepen:
        productgroep_data = df[df['productgroep'] == productgroep]
        with st.expander(f"'+' opties voor productgroep {productgroep}"):
            # Print alle elementen en specificaties binnen de expander
            for index, row in productgroep_data.iterrows():
                element = row['element'].strip()
                st.markdown(f"**{element}**")
                st.markdown(f"{row['specificatie']}")


# In[ ]:


woonbeleving = df[df['impact woonbeleving'] == 'W']

if not woonbeleving.empty:
    st.markdown("---")
    st.markdown("**Woonbeleving '+' opties**")
    st.markdown('''Hieronder zijn de '+' opties weergegeven die impact hebben op woonbeleving, 
                gesorteerd op de productgroepen die het meeste aandeel hebben binnen het project op basis van de optimalisatie. ''')

    productgroepen = woonbeleving['productgroep'].unique()

    # Loop door elke productgroep en maak een expander voor elke productgroep
    for productgroep in productgroepen:
        productgroep_data = df[df['productgroep'] == productgroep]
        with st.expander(f"'+' opties voor productgroep {productgroep}"):
            # Print alle elementen en specificaties binnen de expander
            for index, row in productgroep_data.iterrows():
                element = row['element'].strip()
                st.markdown(f"**{element}**")
                st.markdown(f"{row['specificatie']}")


# In[ ]:


# with st.expander("'+' opties voor productgroep 21. Buitenwanden"):
#     st.markdown('''
#     <u><strong>Impact op circulair</strong></u>
    
#     **ALGEMEEN: isolatie (Isovlas of houtvezel)**
    
#     Isolatie, isovlas of houtvezel:
#     - indien mogelijk Isovlas of houtvezel isolatie (zoals Gutex Thermoflex of gelijkwaardig) toepassen in buitenwanden.
        
#     **BUITENWANDEN, ALGEMEEN: vochtkeringen**
    
#     Kunststof vochtkeringsstrook, loodververvanger:
#     - waar mogelijk: loodvervanger toepassen met recyclaat (zoals bijvoorbeeld Leadax).
      
#     **SPOUWWANDEN: baksteen met mortel** 
    
#     Steen:
#     - duurzaam alternatief: Wienerberger Ecobrick of gelijkwaardig;
#     - dichtheid HD. 
#     - maattolerantie categorie T2. 
#     - maatspreiding categorie R1. 
#     - actieve oplosbare zouten categorie S2.- vorst- en dooiweerstand categorie F2.  
    
#     Mortel:
#     - prefab doorstrijkmortel volgens NEN-EN 998-2-10. 
#     - mortel naar toepassing (klasse): G. 
#     - morteldruksterkte (klasse): M 10. 
#     - bindmiddel: cement CEM I en bouwkalk (NEN-EN 459-1-10). 
#     Toebehoren: - spouwankers, van roestvast staal, 
#     kwaliteit AISI 304, ø 4 mm. - veer-/stripankers vangeperforeerd roestvast staal, kwaliteit AISI 304. Voegvulling: voegvulling op rug.
        
#     **SPOUWWANDEN: isolatie (Isovlas)**
    
#     Kalkzandsteen lijmblok/-elementen:
#     - kalkzandsteen elementen met recyclaat (zoals bijvoorbeeld Caldubo);
#     - druksterkte: volgens opgave constructeur
#     - Oppervlaktegroep overeenkomstig STABU Standaard, hfst. 22, bijlage A: groep 2;
#     - lijmmortel: - volgens advies fabrikant/leverancier van de blokken.  
#     Toebehoren:  - kimblokken. - lijmspouwankers, van roestvast staal, kwaliteit AISI 304, ø 4 mm. - veer-/stripankers van geperforeerd roestvast staal, kwaliteit AISI 304. ''', unsafe_allow_html=True)
    

# with st.expander("'+' opties voor productgroep 31. Buitenkozijnen, -ramen, -deuren en -puien"):
#     st.markdown('''
#     <u><strong>Impact op circulair</strong></u>
    
#     **ALGEMEEN: beglazing**
    
#     Beglazing:
#     - circulaire beglazing (minimun van 50%, waar mogelijk meer);
#     - Meerbladig isolerende beglazing, volgens NEN 2608+a01, minimaal HR++ glas. 
        
#     **BUITENWANDOPENINGEN, HOUT: schilderwerk**
    
#     Schilderwerk: Fabrikant: Sigma, Sikkens of gelijkwaardig. 
    
#     <u><strong>Impact op budget</strong></u>
    
#     **ALGEMEEN: natuursteen buitendorpel met neut**
    
#     Natuursteen buitendorpel met neut: 
#     - van hardsteen. 
#     - geprofileerd met ingelijmde neuten en aan bovenzijde hoeken met facetkant.
#     - onder de buitendeurkozijnen van de algemene ruimten op de begane grond. 
    
#     **ALGEMEEN:  Natuursteen vensterbank van marmercomposiet:**
    
#     Natuursteen vensterbank van marmercomposiet:   
#     - van marmercomposiet (96% natuursteen, 4% kunsthars) - dikte 20 mm.  - zichtzijden fijn gezoet. 
    
#     <u><strong>Impact op kwaliteit</strong></u>
    
#     **ALGEMEEN: natuursteen buitendorpel met neut**
    
#     Natuursteen buitendorpel met neut: 
#     - van hardsteen. 
#     - geprofileerd met ingelijmde neuten en aan bovenzijde hoeken met facetkant.
#     - onder de buitendeurkozijnen van de algemene ruimten op de begane grond. 
    
#     **ALGEMEEN:  Natuursteen vensterbank van marmercomposiet:**
    
#     Natuursteen vensterbank van marmercomposiet:   
#     - van marmercomposiet (96% natuursteen, 4% kunsthars) - dikte 20 mm.  - zichtzijden fijn gezoet.
    
#     ''', unsafe_allow_html=True)


# In[ ]:


st.page_link("simplex.py", label="Homepagina")

