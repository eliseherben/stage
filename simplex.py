#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pulp as pl
#from menu import menu_with_redirect
#menu_with_redirect()


# als de impact cijfers integers zijn dan kunnen de weighted dingen niet integers zijn, om te voorkomen dat er 0 uit komt bij een van de opties
# 

# In[ ]:


st.title("Eigen Haard")
tab1, tab2, tab3 = st.tabs(["Input", "Optimalisatie", "Aanpassingen"])


# **input tab**

# In[ ]:


with tab1:
    st.markdown("**Afdeling**")
    st.selectbox(
        "Welke afdeling?", 
        ['Nieuwbouw ontwikkeling', 'Nieuwbouw realisatie', 'Renovatie ontwikkeling', 'Renovatie realisatie', 'Planmatig onderhoud ontwikkeling', 
         'Planmatig onderhoud realisatie', 'Mutatie onderhoud', 'Dagelijks onderhoud'],
        index=None,
        placeholder="Selecteer een afdeling"
    )
    
    st.markdown("**Projectfase**")
    st.selectbox(
        "Wat is de fase van het project?",
        ['Projectdefinitie', 'Structuurontwerp', 'Voorontwerp', 'Definitief ontwerp', 'Technisch ontwerp bestek', 'Uitvoeringsgereed ontwerp', 'Gebruik'],
        index = None,
        placeholder = "Selecteer de fase van het project"
    )

    st.markdown("**Projectbestand**")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
    
    if uploaded_file is not None:
        dataframe = dataframe.drop(dataframe.columns[[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 29]], axis = 1)
        dataframe.rename(columns={dataframe.columns[12]: "impact onderhoud"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[13]: "impact circulair"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[14]: "impact kwaliteit"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[15]: "impact budget"}, inplace=True)
        dataframe.rename(columns={dataframe.columns[16]: "impact woonbeleving"}, inplace=True)
        dataframe = dataframe.dropna(how='all')
        dataframe = dataframe.drop(0)
        dataframe = dataframe.reset_index(drop=True)
        dataframe['totaal'] = dataframe.groupby(['PRODUCTGROEP'])['PRODUCTGROEP'].transform('count')
        dataframe['onderhoud'] = dataframe.groupby(['PRODUCTGROEP'])['impact onderhoud'].transform('count')
        dataframe['circulair'] = dataframe.groupby(['PRODUCTGROEP'])['impact circulair'].transform('count')
        dataframe['kwaliteit'] = dataframe.groupby(['PRODUCTGROEP'])['impact kwaliteit'].transform('count')
        dataframe['budget'] = dataframe.groupby(['PRODUCTGROEP'])['impact budget'].transform('count')
        dataframe['woonbeleving'] = dataframe.groupby(['PRODUCTGROEP'])['impact woonbeleving'].transform('count')
        dataframe['impact O'] = dataframe['onderhoud']/dataframe['totaal']
        dataframe['impact CD'] = dataframe['circulair']/dataframe['totaal']
        dataframe['impact K'] = dataframe['kwaliteit']/dataframe['totaal']
        dataframe['impact B'] = dataframe['budget']/dataframe['totaal']
        dataframe['impact W'] = dataframe['woonbeleving']/dataframe['totaal']
        impact = dataframe[['PRODUCTGROEP', 'impact O', 'impact CD', 'impact K', 'impact B', 'impact W']]
        impact = impact.groupby('PRODUCTGROEP')[['impact O', 'impact CD', 'impact K', 'impact B', 'impact W']].first()
        impact = impact.reset_index()
        
        productgroepen = pd.DataFrame({
        "PRODUCTGROEP": ['21. Buitenwanden', '22. Binnenwanden', '23. Vloeren', '24. Trappen en hellingen', '27. Daken', '28. Hoofddraag- constructie', 
                         '31. Buitenkozijnen, -ramen, -deuren en -puien.', '32. Binnenkozijnen en - deuren', '33. Luiken en vensters', 
                         '34. Balustrades en leuningen', '42. Binnenwand- afwerkingen', '43. Vloer- afwerkingen', '45 Plafonds', '48. Na-isolatie', 
                         '52. Riolering en HWA', '53. Warm- en koud water installaties', '56. Verwarming en koeling', '57. Lucht- behandeling', 
                         '61. Elektrische installaties', '64. Vaste gebouw- voorzieningen', '65. Beveiliging', '66. Lift', '73. Keuken', '74. Sanitair', 
                         '90.Terrein'],
        "impact O": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "impact CD": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "impact K": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "impact B": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "impact W": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
        
        for i, row in productgroepen.iterrows():
            if row['PRODUCTGROEP'] not in impact['PRODUCTGROEP'].values:
                impact = pd.concat([impact, row.to_frame().T], ignore_index=True)
        impact = impact.sort_values(by='PRODUCTGROEP', ascending=True)
        impact = impact.reset_index(drop=True)

        st.dataframe(impact)
    
        data = {
        "productgroep": ['21 Buitenwanden', '22 Binnenwanden', '23 Vloeren', '24 Trappen en hellingen', '27 Daken', '28 Hoofddraagconstructie', 
                         '31 Buitenkozijnen, -ramen, -deuren, en -puien', '32 Binnenkozijnen en -deuren', '33 Luiken en vensters', 
                         '34 Balustrades en leuningen', '42 Binnenwandafwerkingen', '43 Vloerafwerkingen', '45 Plafonds', '48 Na-isolatie', 
                         '52 Riolering en HWA', '53 Warm- en koud water installaties', '56 Verwarming en koeling', '57 Luchtbehandeling', 
                         '61 Elektrische installaties', '64 Vaste gebouwvoorziening', '65 Beveiliging', '66 Lift', '73 Keuken', '74 Sanitair', 
                         '90 Terreininrichting'],
        "impact onderhoud": [impact.iloc[i, 1] for i in range(len(impact))],
        "impact circulair": [impact.iloc[i, 2] for i in range(len(impact))],
        "impact kwaliteit": [impact.iloc[i, 3] for i in range(len(impact))],
        "impact budget": [impact.iloc[i, 4] for i in range(len(impact))], 
        "impact woonbeleving": [impact.iloc[i, 5] for i in range(len(impact))]
        }
        
        df = pd.DataFrame(data)
    
        onderhoud = df[['productgroep', 'impact onderhoud']]
        onderhoud = onderhoud.sort_values(by='impact onderhoud', ascending=False)
        onderhoud = onderhoud.reset_index(drop=True)
        
        circulair = df[['productgroep', 'impact circulair']]
        circulair = circulair.sort_values(by='impact circulair', ascending=False)
        circulair = circulair.reset_index(drop=True)
    
        kwaliteit = df[['productgroep', 'impact kwaliteit']]
        kwaliteit = kwaliteit.sort_values(by='impact kwaliteit', ascending=False)
        kwaliteit = kwaliteit.reset_index(drop=True)
        
        budget = df[['productgroep', 'impact budget']]
        budget = budget.sort_values(by='impact budget', ascending=False)
        budget = budget.reset_index(drop=True)
        
        woonbeleving = df[['productgroep', 'impact woonbeleving']]
        woonbeleving = woonbeleving.sort_values(by='impact woonbeleving', ascending=False)
        woonbeleving = woonbeleving.reset_index(drop=True)
    
    st.markdown("**Budget**")
    st.number_input("Vul het budget in voor het huidige project", value=None, placeholder="Typ een bedrag")
    
    st.markdown("**Wegingen**")
    st.markdown("Hieronder kan er per thema aangegeven worden of deze zwaarder of minder zwaar meeweegt tijdens dit project. "
    "Als een thema neutraal is kan deze op '0' blijven staan. Als een thema zwaarder meeweegt kan deze op +1 of +2 staan, "
    "als een thema minder zwaar meeweegt kan deze op -1 of -2 gezet worden. ")
    weging_woonbeleving = st.number_input("De weging in voor het thema 'Woonbeleving' in dit project", value=0, min_value = -2, max_value = 2)
    weging_circulair = st.number_input("De weging in voor het thema 'Duurzaam' in dit project", value=0, min_value = -2, max_value = 2)
    weging_budget = st.number_input("De weging in voor het thema 'Kosten' in dit project", value=0, min_value = -2, max_value = 2)
    weging_onderhoud = st.number_input("De weging in voor het thema 'Onderhoud' in dit project", value=0, min_value = -2, max_value = 2)
    weging_kwaliteit = st.number_input("De weging in voor het thema 'Kwaliteit' in dit project", value=0, min_value = -2, max_value = 2)
    
    st.markdown("**Productgroepen**")
    st.markdown("Hierbij kan er aangegeven worden wat het aandeel van de productgroepen momenteel in het project is. Dit is uitgedrukt in percentages. ")
    st.number_input("Het aandeel van de productgroep 'Keuken' in dit project", value=0, min_value = 0, max_value = 100)
    st.number_input("Het aandeel van de productgroep 'Sanitair' in dit project", value=0, min_value = 0, max_value = 100)
    st.number_input("Het aandeel van de productgroep 'Na-isolatie' in dit project", value=0, min_value = 0, max_value = 100)


# **optimalisatie op basis van impact waardes van materialenlijst**

# opsomming themas met meeste impact

# In[ ]:


with tab2: 
    if uploaded_file is not None:
        if (onderhoud['impact onderhoud'].iloc[0] and onderhoud['impact onderhoud'].iloc[1] and onderhoud['impact onderhoud'].iloc[2]) > 0:
            st.markdown('**Onderhoud**')
            st.markdown(
            f"""
            De productgroepen die het meeste impact maken op het thema 'Onderhoud':
            - {onderhoud['productgroep'].iloc[0]}
            - {onderhoud['productgroep'].iloc[1]}
            - {onderhoud['productgroep'].iloc[2]}
            """
            )
        if (circulair['impact circulair'].iloc[0] and circulair['impact circulair'].iloc[1] and circulair['impact circulair'].iloc[2]) > 0:
            st.markdown('**Circulair**')
            st.markdown(
            f"""
            De productgroepen die het meeste impact maken op het thema 'Duurzaam':
            - {circulair['productgroep'].iloc[0]}
            - {circulair['productgroep'].iloc[1]}
            - {circulair['productgroep'].iloc[2]}
            """
            )    
        if (kwaliteit['impact kwaliteit'].iloc[0] and kwaliteit['impact kwaliteit'].iloc[1] and kwaliteit['impact kwaliteit'].iloc[2]) > 0:
            st.markdown('**Kwaliteit**')
            st.markdown(
            f"""
            De productgroepen die het meeste impact maken op het thema 'Kwaliteit':
            - {kwaliteit['productgroep'].iloc[0]}
            - {kwaliteit['productgroep'].iloc[1]}
            - {kwaliteit['productgroep'].iloc[2]}
            """
            )
        if (budget['impact budget'].iloc[0] and budget['impact budget'].iloc[1] and budget['impact budget'].iloc[2]) > 0:
            st.markdown('**Budget**')
            st.markdown(
            f"""
            De productgroepen die het meeste impact maken op het thema 'Budget':
            - {budget['productgroep'].iloc[0]}
            - {budget['productgroep'].iloc[1]}
            - {budget['productgroep'].iloc[2]}
            """
            )
        if (woonbeleving['impact woonbeleving'].iloc[0] and woonbeleving['impact woonbeleving'].iloc[1] and woonbeleving['impact woonbeleving'].iloc[2]) > 0:
            st.markdown('**Woonbeleving**')
            st.markdown(
            f"""
            De productgroepen die het meeste impact maken op het thema 'Woonbeleving':
            - {woonbeleving['productgroep'].iloc[0]}
            - {woonbeleving['productgroep'].iloc[1]}
            - {woonbeleving['productgroep'].iloc[2]}
            """
            )
    else:
        st.markdown("Upload een bestand om de optimalisatie te starten")


# pulp lp model

# In[ ]:


with tab2: 
    if uploaded_file is not None:
        # Creëer een LP probleem
        prob = pl.LpProblem("Eigen Haard", pl.LpMaximize)
        
        # Definieer de variabelen
        buitenwanden = pl.LpVariable("buitenwanden", lowBound=0)
        binnenwanden = pl.LpVariable("binnenwanden", lowBound=0)
        vloeren = pl.LpVariable("vloeren", lowBound=0)
        trappen_hellingen = pl.LpVariable("trappen_hellingen", lowBound=0)
        daken = pl.LpVariable("daken", lowBound=0)
        hoofddraagconstructie = pl.LpVariable("hoofddraagconstructie", lowBound=0)
        buitenkozijnen = pl.LpVariable("buitenkozijnen", lowBound=0)
        binnenkozijnen = pl.LpVariable("binnenkozijnen", lowBound=0)
        luiken_vensters = pl.LpVariable("luiken_vensters", lowBound=0)
        balustrades_leuningen = pl.LpVariable("balustrades_leuningen", lowBound=0)
        binnenwandafwerkingen = pl.LpVariable("binnenwandafwerkingen", lowBound=0)
        vloerafwerkingen = pl.LpVariable("vloerafwerkingen", lowBound=0)
        plafonds = pl.LpVariable("plafonds", lowBound=0)
        na_isolatie = pl.LpVariable("na_isolatie", lowBound=0)
        riolering_hwa = pl.LpVariable("riolering_hwa", lowBound=0)
        water_installaties = pl.LpVariable("water_installaties", lowBound=0)
        verwarming_koeling = pl.LpVariable("verwarming_koeling", lowBound=0)
        luchtbehandeling = pl.LpVariable("luchtbehandeling", lowBound=0)
        elektrische_installaties = pl.LpVariable("elektrische_installaties", lowBound=0)
        gebouwvoorzieningen = pl.LpVariable("gebouwvoorzieningen", lowBound=0)
        beveiliging = pl.LpVariable("beveiliging", lowBound=0)
        lift = pl.LpVariable("lift", lowBound=0)
        keuken = pl.LpVariable("keuken", lowBound=0)
        sanitair = pl.LpVariable("sanitair", lowBound=0)
        terreininrichting = pl.LpVariable("terreininrichting", lowBound=0)
        
        variabelen = [buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, binnenkozijnen, luiken_vensters, 
                      balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, riolering_hwa, water_installaties, 
                      verwarming_koeling, luchtbehandeling, elektrische_installaties, gebouwvoorzieningen, beveiliging, lift, keuken, sanitair, terreininrichting]
        
        #Impact themas op productgroepen

        impact_onderhoud = [impact.iloc[a, 1] for a in range(len(impact))]
        onderhoud = pl.lpSum(variabelen[i] * impact_onderhoud[i] for i in range(25))
        
        impact_circulair = [impact.iloc[a, 2] for a in range(len(impact))]
        circulair = pl.lpSum(variabelen[i] * impact_circulair[i] for i in range(25))
        
        impact_kwaliteit = [impact.iloc[a, 3] for a in range(len(impact))]
        kwaliteit = pl.lpSum(variabelen[i] * impact_kwaliteit[i] for i in range(25))
        
        impact_budget = [impact.iloc[a, 4] for a in range(len(impact))]
        budget = pl.lpSum(variabelen[i] * impact_budget[i] for i in range(25))
        
        impact_woonbeleving = [impact.iloc[a, 5] for a in range(len(impact))]
        woonbeleving = pl.lpSum(variabelen[i] * impact_woonbeleving[i] for i in range(25))
    
        prob += weging_circulair * circulair - weging_budget * budget + weging_woonbeleving * woonbeleving + weging_kwaliteit * kwaliteit + weging_onderhoud * onderhoud
        
        # Voeg beperkingen toe (voorbeeldbeperkingen)
        prob += buitenkozijnen + lift + binnenkozijnen + binnenwandafwerkingen + vloerafwerkingen + plafonds + sanitair + keuken + buitenwanden + vloeren + daken + hoofddraagconstructie + na_isolatie + riolering_hwa + terreininrichting + verwarming_koeling + luchtbehandeling + gebouwvoorzieningen + binnenwanden + trappen_hellingen + luiken_vensters + balustrades_leuningen+ water_installaties + elektrische_installaties + beveiliging == 100
        
        prob += buitenkozijnen >= 6.8
        prob += lift >= 0.4
        prob += binnenkozijnen >= 3.4
        prob += binnenwandafwerkingen >= 2.6
        prob += vloerafwerkingen >= 3.8
        prob += plafonds >= 1.1
        prob += sanitair >= 2.3
        prob += keuken >= 0.4
        prob += buitenwanden >= 6.0 
        prob += vloeren >= 1.5
        prob += daken >= 2.3
        prob += hoofddraagconstructie >= 0.8
        prob += na_isolatie >= 0.8
        prob += riolering_hwa >= 3.4 
        prob += terreininrichting >= 2.6
        prob += verwarming_koeling >= 3.0
        prob += luchtbehandeling >= 1.9
        prob += gebouwvoorzieningen >= 1.5
        prob += binnenwanden >= 3.0
        prob += trappen_hellingen >= 2.3
        prob += luiken_vensters >= 1.9
        prob += balustrades_leuningen >= 0.4
        prob += water_installaties  >= 2.3
        prob += elektrische_installaties >= 0.4
        prob += beveiliging >= 1.1
        
        prob += buitenkozijnen <= 12.8
        prob += lift <= 1.4
        prob += binnenkozijnen <= 6.4
        prob += binnenwandafwerkingen <= 4.5
        prob += vloerafwerkingen <= 7.5
        prob += plafonds <= 1.5
        prob += sanitair <= 3.4
        prob += keuken <= 1.9
        prob += buitenwanden <= 9.8 
        prob += vloeren <= 1.5
        prob += daken <= 5.3
        prob += hoofddraagconstructie <= 0.8
        prob += na_isolatie <= 2.3
        prob += riolering_hwa <= 7.1 
        prob += terreininrichting <= 3.0
        prob += verwarming_koeling <= 4.5
        prob += luchtbehandeling <= 4.5
        prob += gebouwvoorzieningen <= 4.1
        prob += binnenwanden <= 3.8
        prob += trappen_hellingen <= 3.4
        prob += luiken_vensters <= 1.9
        prob += balustrades_leuningen <= 1.4
        prob += water_installaties  <= 3.4
        prob += elektrische_installaties <= 2.3
        prob += beveiliging <= 1.9
        
        # Los het probleem op
        status = prob.solve()
        
        # Maak een lege lijst om de variabelen en hun waarden op te slaan
        variabelen_waarden = []
        
        # Voeg de variabelen en hun waarden toe aan de lijst
        for var in variabelen:
            variabelen_waarden.append((var.name, var.varValue))
        
        # Maak een DataFrame van de lijst
        df = pd.DataFrame(variabelen_waarden, columns=['Productgroep', 'Waarde'])
        
        # Toon de DataFrame
        print(df)
        
        # Toon de resultaten
        print("Optimale oplossing:")
        
        print(pl.LpStatus[status])
        st.markdown(f"Status van de oplossing: {pl.LpStatus[status]}")
        print("buitenkozijnen = ", buitenkozijnen.varValue)
        print("lift = ", lift.varValue)
        print("binnenkozijnen = ", binnenkozijnen.varValue)
        print("binnenwandafwerkingen = ", binnenwandafwerkingen.varValue)
        print("vloerafwerkingen = ", vloerafwerkingen.varValue)
        print("plafonds = ", plafonds.varValue)
        print("sanitair = ", sanitair.varValue)
        print("keuken = ", keuken.varValue)
        print("buitenwanden = ", buitenwanden.varValue)
        print("daken = ", daken.varValue)
        print("vloeren = ", vloeren.varValue)
        print("hoofddraagconstructie = ", hoofddraagconstructie.varValue)
        print("na_isolatie = ", na_isolatie.varValue)
        print("riolering_hwa = ", riolering_hwa.varValue)
        print("terreininrichting = ", terreininrichting.varValue)
        print("verwarming_koeling = ", verwarming_koeling.varValue)
        print("luchtbehandeling = ", luchtbehandeling.varValue)
        print("gebouwvoorzieningen =", gebouwvoorzieningen.varValue)
        print("binnenwanden =", binnenwanden.varValue)
        print("trappen_hellingen =", trappen_hellingen.varValue)
        print("luiken_vensters =", luiken_vensters.varValue)
        print("balustrades_leuningen =", balustrades_leuningen.varValue)
        print("water_installaties =", water_installaties.varValue)
        print("elektrische_installaties =", elektrische_installaties.varValue)
        print("beveiliging =", beveiliging.varValue)
        
        print("Maximale waarde van de doelfunctie:", prob.objective.value())
        st.markdown(f"Waarde van de doelfunctie: {prob.objective.value()}")


# uitkomst optimalisatie

# In[ ]:


with tab2:
    if uploaded_file is not None:
        st.markdown("**In dit project, is het optimaal om het aandeel van de productgroepen als volgt in te delen:**")
        
        for index, row in df.iterrows():
            st.markdown(f"- De productgroep {row['Productgroep']} is {row['Waarde']}% van het totale project")
        
        fig1 = px.pie(values=df['Waarde'], names=df['Productgroep'], color_discrete_sequence=px.colors.sequential.RdBu)
        
        st.plotly_chart(fig1)


# **aanpassingen**

# In[ ]:


with tab3:
    if uploaded_file is not None:
        st.markdown("Hieronder kunnen de verschillende aandelen van productgroepen aangepast worden, om daarvan de invloed te zien op de verschillende thema's")
    
        def max_sliders(waardes):
            max_waarde = 100 - sum(waardes)
            return max_waarde
        
        waardes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
        buitenwanden_max = max_sliders(waardes)
        buitenwanden = st.number_input('Het aandeel van de productgroep Buitenwanden', value = 0.0, min_value = 0.0, max_value = buitenwanden_max, step = 0.1)
        
        binnenwanden_max = max_sliders([buitenwanden, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                        0.0, 0.0, 0.0, 0.0, 0.0])
        binnenwanden = st.number_input('Het aandeel van de productgroep Binnenwanden', value = 0.0, min_value = 0.0, max_value = binnenwanden_max,step = 0.1)
    
        vloeren_max = max_sliders([buitenwanden, binnenwanden, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        vloeren = st.number_input('Het aandeel van de productgroep Vloeren', value = 0.0, min_value = 0.0, max_value = vloeren_max, step = 0.1)
    
        trappen_hellingen_max = max_sliders([buitenwanden, binnenwanden, vloeren, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        trappen_hellingen = st.number_input('Het aandeel van de productgroep Trappen en hellingen', value = 0.0, min_value = 0.0, max_value = trappen_hellingen_max,step = 0.1)
    
        daken_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        daken = st.number_input('Het aandeel van de productgroep Daken', value = 0.0, min_value = 0.0, max_value = daken_max, step = 0.1)
    
        hoofddraagconstructie_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, 
                                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        hoofddraagconstructie = st.number_input('Het aandeel van de productgroep Hoofddraagconstructie', value = 0.0, min_value = 0.0, max_value = hoofddraagconstructie_max,step = 0.1)
    
        buitenkozijnen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, 
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        buitenkozijnen = st.number_input('Het aandeel van de productgroep Buitenkozijnen', value = 0.0, min_value = 0.0, max_value = buitenkozijnen_max, step = 0.1)
    
        binnenkozijnen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        binnenkozijnen = st.number_input('Het aandeel van de productgroep Binnenkozijnen', value = 0.0, min_value = 0.0, max_value = binnenkozijnen_max,step = 0.1)
    
        luiken_vensters_max =  max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        luiken_vensters = st.number_input('Het aandeel van de productgroep Luiken en vensters', value = 0.0, min_value = 0.0, max_value = luiken_vensters_max,step = 0.1)
        
        balustrades_leuningen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                                 binnenkozijnen, luiken_vensters, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        balustrades_leuningen = st.number_input('Het aandeel van de productgroep Balustrades', value = 0.0, min_value = 0.0, max_value = balustrades_leuningen_max, step = 0.1)
        
        binnenwandafwerkingen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                                 binnenkozijnen, luiken_vensters, balustrades_leuningen, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        binnenwandafwerkingen = st.number_input('Het aandeel van de productgroep Binnenwandafwerkingen', value = 0.0, min_value = 0.0, max_value = binnenwandafwerkingen_max, step = 0.1)
        
        vloerafwerkingen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        vloerafwerkingen = st.number_input('Het aandeel van de productgroep Vloerafwerkingen', value = 0.0, min_value = 0.0, max_value = vloerafwerkingen_max, step = 0.1)
        
        plafonds_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, 
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        plafonds = st.number_input('Het aandeel van de productgroep Plafonds', value = 0.0, min_value = 0.0, max_value = plafonds_max, step = 0.1)
        
        na_isolatie_max =  max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        na_isolatie = st.number_input('Het aandeel van de productgroep Na-isolatie', value = 0.0, min_value = 0.0, max_value = na_isolatie_max, step = 0.1)
        
        riolering_hwa_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                        binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                         na_isolatie, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        riolering_hwa = st.number_input('Het aandeel van de productgroep Riolering en HWA', value = 0.0, min_value = 0.0, max_value = riolering_hwa_max, step = 0.1)
        
        water_installaties_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        water_installaties = st.number_input('Het aandeel van de productgroep Warm- en koud water installaties', value = 0.0, min_value = 0.0, max_value = water_installaties_max, step = 0.1)
        
        verwarming_koeling_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        verwarming_koeling = st.number_input('Het aandeel van de productgroep Verwarming en koeling', value = 0.0, min_value = 0.0, max_value = verwarming_koeling_max, step = 0.1)
    
        luchtbehandeling_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                            0.0, 0.0])
        luchtbehandeling = st.number_input('Het aandeel van de productgroep Luchtbehandeling', value = 0.0, min_value = 0.0, max_value = luchtbehandeling_max, step = 0.1)
        
        elektrische_installaties_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, 0.0, 0.0, 0.0, 0.0, 
                                            0.0, 0.0, 0.0])
        elektrische_installaties = st.number_input('Het aandeel van de productgroep Elektrische installaties', value = 0.0, min_value = 0.0, max_value = elektrische_installaties_max, step = 0.1)
        
        gebouwvoorzieningen_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                            na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties,
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        gebouwvoorzieningen = st.number_input('Het aandeel van de productgroep Gebouwvoorzieningen', value = 0.0, min_value = 0.0, max_value = gebouwvoorzieningen_max, step = 0.1)
        
        beveiliging_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                        binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds,
                                       na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                        gebouwvoorzieningen, 0.0, 0.0, 0.0, 0.0, 0.0])
        beveiliging = st.number_input('Het aandeel van de productgroep Beveiliging', value = 0.0, min_value = 0.0, max_value = beveiliging_max, step = 0.1)
        
        lift_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, 
                                riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                gebouwvoorzieningen, beveiliging, 0.0, 0.0, 0.0, 0.0])
        lift = st.number_input('Het aandeel van de productgroep Lift', value = 0.0, min_value = 0.0, max_value = lift_max, step = 0.1)
        
        keuken_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                    binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, 
                                    riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                    gebouwvoorzieningen, beveiliging, lift, 0.0, 0.0, 0.0])
        keuken = st.number_input('Het aandeel van de productgroep Keuken', value = 0.0, min_value = 0.0, max_value = keuken_max, step = 0.1)
        
        sanitair_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                    binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, 
                                    riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                    gebouwvoorzieningen, beveiliging, lift, keuken, 0.0, 0.0])
        sanitair = st.number_input('Het aandeel van de productgroep Sanitair', value = 0.0, min_value = 0.0, max_value = sanitair_max, step = 0.1)
        
        terreininrichting_max = max_sliders([buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, 
                                            binnenkozijnen, luiken_vensters, balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, 
                                             na_isolatie, riolering_hwa, water_installaties, verwarming_koeling, luchtbehandeling, elektrische_installaties, 
                                               gebouwvoorzieningen, beveiliging, lift, keuken, sanitair, 0.0])
        terreininrichting = st.number_input('Het aandeel van de productgroep Terreininrichting', value = 0.0, min_value = 0.0, max_value = terreininrichting_max+0.05, step = 0.1)
        


# In[ ]:


with tab3:
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
    
        with col2:
            st.markdown("**aanpassing**")
            variabelen = [buitenwanden, binnenwanden, vloeren, trappen_hellingen, daken, hoofddraagconstructie, buitenkozijnen, binnenkozijnen, luiken_vensters, 
                          balustrades_leuningen, binnenwandafwerkingen, vloerafwerkingen, plafonds, na_isolatie, riolering_hwa, water_installaties, 
                          verwarming_koeling, luchtbehandeling, elektrische_installaties, gebouwvoorzieningen, beveiliging, lift, keuken, sanitair, terreininrichting]
            productgroep = ['buitenwanden', 'binnenwanden', 'vloeren', 'trappen_hellingen', 'daken', 'hoofddraagconstructie', 'buitenkozijnen', 
                            'binnenkozijnen', 'luiken_vensters', 'balustrades_leuningen', 'binnenwandafwerkingen', 'vloerafwerkingen', 'plafonds', 
                            'na_isolatie', 'riolering_hwa', 'water_installaties', 'verwarming_koeling', 'luchtbehandeling', 
                            'elektrische_installaties', 'gebouwvoorzieningen', 'beveiliging', 'lift', 'keuken', 'sanitair', 'terreininrichting']
            for i in range(25):
                st.markdown(f"- {productgroep[i]}: {variabelen[i]}%")
            
            #Impact themas op productgroepen
            impact_duurzaamheid = [impact.iloc[a, 2] for a in range(len(impact))]
            duurzaamheid = sum([variabelen[i] * impact_duurzaamheid[i] for i in range(25)])
            st.markdown(f"score duurzaamheid: {duurzaamheid}")
            
            impact_prijs = [impact.iloc[a, 4] for a in range(len(impact))]
            prijs = sum([variabelen[i] * impact_prijs[i] for i in range(25)])
            st.markdown(f"score prijs: {prijs}")  
        
            impact_woonbeleving = [impact.iloc[a, 5] for a in range(len(impact))]
            woonbeleving = sum([variabelen[i] * impact_woonbeleving[i] for i in range(25)])
            st.markdown(f"score woonbeleving: {woonbeleving}")  
            
            impact_kwaliteit = [impact.iloc[a, 3] for a in range(len(impact))]
            kwaliteit = sum([variabelen[i] * impact_kwaliteit[i] for i in range(25)])
            st.markdown(f"score kwaliteit: {kwaliteit}")  
            
            impact_onderhoud = [impact.iloc[a, 1] for a in range(len(impact))]
            onderhoud = sum([variabelen[i] * impact_onderhoud[i] for i in range(25)])
            st.markdown(f"score onderhoud: {onderhoud}")  
    
        with col1:
            st.markdown("**optimalisatie**")
            for index, row in df.iterrows():
                st.markdown(f"- {row['Productgroep']}: {row['Waarde']}%")
            duurzaam2 = sum([df['Waarde'][i] * impact_duurzaamheid[i] for i in range(25)])
            prijs2 = sum([df['Waarde'][i] * impact_prijs[i] for i in range(25)])
            woonbeleving2 = sum([df['Waarde'][i] * impact_woonbeleving[i] for i in range(25)])
            kwaliteit2 = sum([df['Waarde'][i] * impact_kwaliteit[i] for i in range(25)])
            onderhoud2 = sum([df['Waarde'][i] * impact_onderhoud[i] for i in range(25)])
            st.markdown(f"score duurzaamheid: {duurzaam2/sum(impact_duurzaamheid)}")
            st.markdown(f"score prijs: {prijs2/sum(impact_prijs)}")
            st.markdown(f"score woonbeleving: {woonbeleving2/sum(impact_woonbeleving)}")
            st.markdown(f"score kwaliteit: {kwaliteit2/sum(impact_kwaliteit)}")
            st.markdown(f"score onderhoud: {onderhoud2/sum(impact_onderhoud)}")


# In[ ]:


productgroepen = pd.DataFrame({'productgroep': ['21', '22', '23', '24'], 
                              'impact': [0, 0, 0, 0]})
impacten = pd.DataFrame({'productgroep': ['21', '23', '24'], 
                         'impact': [2, 4, 1]})

for i, row in productgroepen.iterrows():
    if row['productgroep'] not in impacten['productgroep'].values:
        print(row['productgroep'] + ' can be added to dfOld')
        impacten = pd.concat([impacten, row.to_frame().T], ignore_index=True)
impacten.head()


# In[ ]:





# In[ ]:





# In[ ]:




