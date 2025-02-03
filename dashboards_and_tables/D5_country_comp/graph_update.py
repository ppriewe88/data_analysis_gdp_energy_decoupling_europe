from plotly.subplots import make_subplots

def country_comparison_update_graph(selected_sorting, selected_year, remove_top6_bip, click_data,
                 df_Y, width_graph, height_graph, gdp_color, energy_color, prod_color):
    
    ################## Filterung nach Jahr ##################
    df = df_Y.loc[df_Y["Jahr"] == selected_year]
    
    ################# falls button gewählt, entferne top 5 BIP-erzeuger 2023 aus ganzem frame
    if remove_top6_bip == 'remove':
        # Finde die 5 größten BIP-Länder im Jahr 2023
        top6_bip_2023 = df_Y.loc[df_Y["Jahr"] == 2023].nlargest(6, 'BIP (Mio €)')["Land"]
        
        # Entferne diese 5 Länder aus dem DataFrame
        df = df[~df["Land"].isin(top6_bip_2023)]

    ################### Sortierung ########################
    if selected_sorting == "alle":
        sorted_data_bip = df.sort_values(by="BIP (Mio €)", ascending=False).copy()
        sorted_data_en = df.sort_values(by="Energieverbrauch (GWh)", ascending=False).copy()
        sorted_data_prod = df.sort_values(by="Energieproduktivität (Mio€/GWh)", ascending=False).copy()
    else:    
        sorted_data_bip = df.sort_values(by=selected_sorting, ascending=False)
        sorted_data_en = df.sort_values(by=selected_sorting, ascending=False)
        sorted_data_prod = df.sort_values(by=selected_sorting, ascending=False)
    
    ########### Sortierung Dataframe, Liste Spalten
    sorted_data = [sorted_data_bip, sorted_data_en, sorted_data_prod]  
    columns = ["BIP (Mio €)", "Energieverbrauch (GWh)", "Energieproduktivität (Mio€/GWh)"]

    ################# Markiertes Land setzen ##############
    initial_selection = "Germany"

    #################Balkenselektion prüfen ###########
    selected_land = initial_selection
    if click_data and 'points' in click_data:
        selected_land = click_data['points'][0]['x']
    
    ################### Balkenfarben definieren ##########
    def get_colors(column_name, data):
        color_map = {
        "BIP (Mio €)": gdp_color,
        "Energieverbrauch (GWh)": energy_color,
        "Energieproduktivität (Mio€/GWh)": prod_color}
        return [
            "white" if land == selected_land else color_map[column_name]

            for land in data["Land"]]
    ################## Subplot-Rahmen erstellen #############
    fig = make_subplots(rows=3, cols=1, 
                        shared_xaxes=False, 
                        subplot_titles=["BIP (Mio €)","Energieverbrauch (GWh)", "Energieproduktivität (Mio€/GWh)"],
                        row_heights=[0.33, 0.33, 0.33],
                        vertical_spacing= 0.13
                        )
    ################### Subplots erstellen #####################
    columns = ["BIP (Mio €)", "Energieverbrauch (GWh)", "Energieproduktivität (Mio€/GWh)"]
    for i, column in enumerate(columns):
        ############ daten festlegen
        data = sorted_data[i]
        ############ Balken plotten
        fig.add_bar(
            x=data["Land"], 
            y=data[column],
            marker=dict(color= get_colors(column_name = column, data= data)),
            row=i+1,
            col=1,  # Erste Spalte für die Plots
            hovertemplate="<b>%{x}</b><br>" +  f"{column}:" + "%{y}<extra></extra>"
        )        
        ############# Achsen-Labels und Ticks anpassen
        fig.update_xaxes(
            tickmode='array',
            tickvals=data["Land"],
            ticktext=data["Land"],
            row=i+1,
            col=1
        )
    ################ Subplot-Titel (Annotations) anpassen
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size= 16, color='white')  # Schriftgröße und Farbe anpassen

    ############### Durchschnittslinien hinzufügen
    for i, column in enumerate(columns):
        avg_value = data[column].mean()
        fig.add_shape(
            type="line",
            x0=0, x1=len(data["Land"]) - 1,
            y0=avg_value, y1=avg_value,
            line=dict(color="white", dash="dash", width=2),
            row=i+1,
            col=1,
        )
        fig.add_annotation(
            x=len(data["Land"]) - 1,  # X-Position des Textes (am Ende der Linie)
            y=avg_value,  # Y-Position des Textes (auf der Linie)
            text="Durchschnitt",  # Der Text
            showarrow=False,  # Kein Pfeil zur Markierung
            font=dict(color="white", size= 12),  # Schriftfarbe und -größe
            align="right",  # Textausrichtung
            xanchor="left",  # Text verankert an der linken Seite
            yanchor="bottom",  # Text verankert an der unteren Seite
            row=i + 1,
            col=1,
        )

    ################# Layout anpassen ############################
    fig.update_layout(
        width = width_graph,
        height = height_graph,
        showlegend=False,
        template="custom_template",
        margin=dict(
        t=20,  # Abstand des obersten Subplots vom oberen Rand
        b=5,   # Abstand des untersten Subplots vom unteren Rand
        l=50,   # Abstand vom linken Rand
        r=30    # Abstand vom rechten Rand,
        ),
    )

    return fig