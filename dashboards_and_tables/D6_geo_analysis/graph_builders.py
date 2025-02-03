import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def build_choropleth(dataframe, value_column, html_elements_color):
    # anzahl ticks colorbar
    nr_of_ticks = 8
    # skalierung colorbar
    color_minimum = dataframe[value_column].min()
    color_maximum = dataframe[value_column].max()
    # standardwert Graphenhöhe
    graph_height = 400
    # erstelle figure
    if value_column == "BIP_logarithmiert":   
        text_colorbar = "Mio €"
        title_map = "BIP (Mio €) 2023"
        ticktexts = [f'{np.expm1(val):,.0f}' for val in np.linspace(color_minimum, color_maximum, nr_of_ticks)]
        color_scheme = [
            [0.0, '#bcecff'], # weissblau
            [0.35, '#bcecff'], # weissblau
            [0.4, '#0098ff'], # hellblau
            [0.65, '#0098ff'], # hellblau
            [0.75, '#0016ff'], # blau
            [0.9, '#0016ff'], # blau
            [0.95, '#000077'], # tiefblau
            [1.0, '#000077'] # tiefblau
        ]
        custom_hovertemplate=("<b>%{location}</b><br>" + "<extra></extra>")
        
    elif value_column == "Energieverbrauch_logarithmiert":
        text_colorbar = "GWh"
        title_map = "Energieverbrauch (GWh) 2023"
        ticktexts = [f'{np.expm1(val):,.0f}' for val in np.linspace(color_minimum, color_maximum, nr_of_ticks)]
        color_scheme = [
            [0.0, '#ffffd3'], # weissgelb
            [0.35, '#ffffd3'], # weissgelb
            [0.4, '#ffbf00'], # gelborange
            [0.65, '#ffbf00'], # gelborange
            [0.75, '#ff3a00'], # rot
            [0.9, '#ff3a00'], # rot
            [0.95, '#9d0000'], # tiefrot
            [1.0, '#9d0000'] # tiefrot
        ]
        custom_hovertemplate=("<b>%{location}</b><br>" + "<extra></extra>")
        
    elif value_column == "BIP (Mio €)_Diff zu 2008 (%)":
        text_colorbar = "% Änderung"
        title_map = "BIP - prozentuale Änderung zu Referenzjahr 2008"
        ticktexts = [f'{val:,.0f}' for val in np.linspace(color_minimum, color_maximum, nr_of_ticks)]
        color_scheme = [
            [0.0, '#d83123'], # rot
            [0.043, '#ffffff'], # weiss
            [0.15, '#ffffff'], # weiss
            [0.2, '#88e385'], # helles grün
            [0.35, '#88e385'], # helles grün
            [0.4, '#1cc31c'], # mittleres grün
            [0.6, '#1cc31c'], # mittleres grün
            [0.7, '#006900'], # dunkles grün
            [1.0, '#006900'] # dunkles grün
        ]
        custom_hovertemplate=("<b>%{location}</b><br>" + f"{value_column}: " + "%{z}<br>" + "<extra></extra>")
        
    elif value_column == "Energieverbrauch (GWh)_Diff zu 2008 (%)":
        text_colorbar = "% Änderung"
        title_map = "Energieverbrauch - prozentuale Änderung zu Referenzjahr 2008"
        ticktexts = [f'{val:,.0f}' for val in np.linspace(color_minimum, color_maximum, nr_of_ticks)]
        color_scheme = [
            [0.0, '#006900'], # dunkles grün
            [0.07, '#006900'], # dunkles grün
            [0.125, '#1cc31c'], # mittleres grün
            [0.2, '#1cc31c'], # mittleres grün
            [0.25, '#ffffff'], # weiss
            [0.35, '#ffffff'], # weiss
            [0.4, '#ffaf3a'], # rotorange
            [0.6, '#ffaf3a'], # rotorange
            [0.7, '#d83123'], # rot
            [1.0, '#d83123'] # rot
        ]
        custom_hovertemplate=("<b>%{location}</b><br>" + f"{value_column}: " + "%{z}<br>" + "<extra></extra>")
        
    elif value_column == "Energieproduktivität (Mio€/GWh)":
        text_colorbar = "Mio€/GWh"
        title_map = ""
        ticktexts = [f'{val:,.0f}' for val in np.linspace(color_minimum, color_maximum, nr_of_ticks)]
        color_scheme = [
            [0.0, '#ffaf3a'], # rotorange
            [0.07, '#ffaf3a'], # rotorange
            [0.125, '#ffffd3'], # gelborange
            [0.2, '#ffffd3'], # gelborange
            [0.25, '#88e385'], # helles grün
            [0.35, '#88e385'], # helles grün
            [0.4, '#1cc31c'], # mittleres grün
            [0.6, '#1cc31c'], # mittleres grün
            [0.7, '#006900'], # dunkles grün
            [1.0, '#006900'] # dunkles grün
        ]
        custom_hovertemplate=("<b>%{location}</b><br>" + f"{value_column}: " + "%{z}<br>" + "<extra></extra>")
        graph_height = 500
    else:
        raise Exception("Falscher Input build_chloropleth-Funktion!!")

    # Erstelle die Choropleth-Karte
    figure = go.Figure(
        data=go.Choropleth(
            locations=dataframe["iso_code"],  # ISO-Codes der Länder
            z= dataframe[value_column],   # BIP-Werte (Farbenbasis)
            zmin= color_minimum,
            zmax = color_maximum,
            colorscale= color_scheme,               # Farbschema
            colorbar=dict(
                title=dict(
                    text=text_colorbar,  # Farbskalenüberschrift
                    font=dict(size=12),    # Schriftgröße der Farbskalenüberschrift
                ),
                title_side="top",          # Position der Überschrift oben
                title_font=dict(size=12),  # Schriftgröße der Farbskalenüberschrift
                tickvals=np.linspace(color_minimum, color_maximum, nr_of_ticks),
                ticktext= ticktexts
            ),
            hovertemplate= custom_hovertemplate
        ),
        layout=go.Layout(
            geo=dict(
                visible=False, resolution=50, #scope="europe",  # Zonen und Auflösung der Karte
                showcountries=False, countrycolor="Black",    # Zeigt Länder an und färbt die Ränder schwarz
                showsubunits=False,                          # Subnationale Einheiten ausblenden
                center={"lat": 52.0, "lon": 14.0},          # Karte auf Europa zentrieren
                projection=dict(
                    scale=4.4,  # Zoom-Stufe (größer als 1 zoomt stärker rein)
                    rotation={"lon": 55}  # Rotation um 15 Grad
                ),
                bgcolor=html_elements_color  # Hintergrundfarbe der Karte
            ),
            title= title_map,
            height= graph_height,
            margin={"r": 120, "t": 28, "l": 20, "b": 0},
            template='custom_template'
        )
    )

    return figure


#################################### update first choropleth dashboard #################
def geo_update_graph(selected_mode, df_Y_2023, html_elements_color):
    if selected_mode == "static_2023":
        graph_bip = build_choropleth(dataframe = df_Y_2023, value_column= "BIP_logarithmiert", html_elements_color=html_elements_color)
        graph_en = build_choropleth(dataframe = df_Y_2023, value_column= "Energieverbrauch_logarithmiert", html_elements_color=html_elements_color)
    else:
        graph_bip = build_choropleth(dataframe = df_Y_2023, value_column= "BIP (Mio €)_Diff zu 2008 (%)", html_elements_color=html_elements_color)
        graph_en = build_choropleth(dataframe = df_Y_2023, value_column= "Energieverbrauch (GWh)_Diff zu 2008 (%)", html_elements_color=html_elements_color)

    return graph_bip, graph_en


######################################### build animated choropeth figure ##########
def build_animated_choropeth(df_Q, html_elements_color):
    ###################################### vorübergehende Änderung Spaltenname für Anzeige ##########
    df_Q = df_Q.copy()
    df_Q = df_Q.rename(columns={"Quartal_label": "Jahr & Quartal"})

    print("OK")
    ###################################### Erstelle Choropleth-Animation ################
    figure1 = px.choropleth(
        df_Q, 
        locations="iso_code", 
        color="Erreichungsgrad_Jahresmaximalproduktivität", 
        hover_name="Land", 
        animation_frame="Jahr & Quartal", 
        color_continuous_scale= [
                [0.0, '#cc3c3e'], # rot
                [0.25, '#cc3c3e'], # rot
                [0.26, '#ffff00'], # gelb
                [0.74, '#ffff00'], # gelb
                [0.75, '#00bc00'], # grün
                [1.0, '#00bc00'], # grün
                ],
        hover_data={
            "Erreichungsgrad_Jahresmaximalproduktivität": True,  # Zeigt den BIP-Wert
            "Land": True,  # Zeigt den Ländernamen
            "Jahr & Quartal": True,  # Zeigt Jahr & Quartal
            "iso_code": False
        }
    )

    ###################################### Custom-Optionen für Colorbar #########################
    color_minimum = df_Q["Erreichungsgrad_Jahresmaximalproduktivität"].min()  # Setze den minimalen Wert
    color_maximum = df_Q["Erreichungsgrad_Jahresmaximalproduktivität"].max()  # Setze den maximalen Wert
    nr_of_ticks = 5  # Anzahl der Ticks

    ######################################## Tick-Werte und Tick-Labels #####################################
    tickvals = np.linspace(color_minimum, color_maximum, nr_of_ticks)
    ticktexts = [f'{val:.2f}' for val in tickvals]  # Formatierung der Tick-Werte

    ################################### figure definieren ############################################
    figure1.update_layout(
        geo=dict(
            visible=False, 
            resolution=50,  # Zonen und Auflösung der Karte
            showcountries=False, 
            countrycolor="Black",  # Zeigt Länder an und färbt die Ränder schwarz
            showsubunits=False,  # Subnationale Einheiten ausblenden
            center={"lat": 52.0, "lon": 12.0},  # Karte auf Europa zentrieren
            projection=dict(
                scale=5,  # Zoom-Stufe (größer als 1 zoomt stärker rein)
                rotation={"lon": 55}  # Rotation um 15 Grad
            ),
            bgcolor=html_elements_color
        ),
        margin={"r": 0, "t": 35, "l": 20, "b": 0},
        template='custom_template',
        title= "",
        height = 500,
        coloraxis_colorbar=dict(
            title="Erreichungsgrad",  # Farbskalenüberschrift
            tickvals=tickvals,  # Setzt die Position der Ticks auf der Farbskala
            ticktext=ticktexts,  # Setzt die Beschriftung der Ticks
            tickfont=dict(size=12),  # Schriftgröße der Ticks
            title_font=dict(size=14),  # Schriftgröße der Farbskalenüberschrift
            title_side="top",  # Position der Farbskalenüberschrift
            tickmode='array'  # Damit die Ticks wie gewünscht angezeigt werden
        ),
        coloraxis=dict(
            cmin=color_minimum,  # Fixiere den minimalen Wert der Farbskala
            cmax=color_maximum   # Fixiere den maximalen Wert der Farbskala
        ),
    )

    figure1.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 350
    figure1.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10

    return figure1


################################## build graph numerical analysis seasonal peaks ####
def build_seasonal_peaks_numerical(selected_country, formatted_df, gdp_color, energy_color, prod_color):
    
    ################## Filterung nach Jahr ##################
    if selected_country == "Alle":
        df = formatted_df
    else:
        df = formatted_df.loc[formatted_df["Land"] == selected_country]
    
    ################### Figure erstellen
    figure = make_subplots(
    rows=1, cols=3,  # 1 Zeile, 3 Spalten
    subplot_titles=["BIP", "Energieverbrauch", "Energieproduktivität"],
    shared_yaxes=False  # Gemeinsame Y-Achse für alle Subplots
    )

    # Histogramm 1
    figure.add_trace(
        go.Histogram(
            x=df['Max_Quartal_BIP'], nbinsx=4,
            marker=dict(color=gdp_color),
            hovertemplate=(
                    "Quartal: %{x}<br>"  # Zeigt das Quartal an
                    "Häufigkeit: %{y} mal Jahresmaximum<extra></extra>"  # Gibt die Häufigkeit an
            )),
        row=1, col=1
    )
    # Histogramm 2
    figure.add_trace(
        go.Histogram(
            x=df['Max_Quartal_Energieverbrauch'], nbinsx=4,
            marker=dict(color=energy_color), 
            hovertemplate=(
                    "Quartal: %{x}<br>"  # Zeigt das Quartal an
                    "Häufigkeit: %{y} mal Jahresmaximum<extra></extra>"  # Gibt die Häufigkeit an
            )),
        row=1, col=2
    )
    # Histogramm 3
    figure.add_trace(
        go.Histogram(
            x=df['Max_Quartal_Energieproduktivität'], nbinsx=4,
            marker=dict(color=prod_color),
            hovertemplate=(
                    "Quartal: %{x}<br>"  # Zeigt das Quartal an
                    "Häufigkeit: %{y} mal Jahresmaximum<extra></extra>"  # Gibt die Häufigkeit an
            )),
        row=1, col=3
    )
    # Layout und Achsen
    figure.update_layout(
        title_text="Häufigkeiten: Wie oft war welches Quartal das Jahresmaximum?",
        showlegend=False,  # Keine Legende anzeigen
        height= 400,  # Höhe der Subplots
        width= 1180,  # Breite der Subplots
        xaxis_title="Quartal",
        yaxis_title="Häufigkeit",
        template = "custom_template",
        bargap=0.3
    )

    # Achsentitel und Kategoriensortierung in Subplots
    quartal_order = ["Q1", "Q2", "Q3", "Q4"]
    figure.update_xaxes(title_text="Quartal", categoryorder="array", categoryarray=quartal_order, row=1, col=1)
    figure.update_xaxes(title_text="Quartal", categoryorder="array", categoryarray=quartal_order, row=1, col=2)
    figure.update_xaxes(title_text="Quartal", categoryorder="array", categoryarray=quartal_order, row=1, col=3)
    figure.update_yaxes(title_text="Häufigkeit", row=1, col=1)
    figure.update_yaxes(title_text="Häufigkeit", row=1, col=2)
    figure.update_yaxes(title_text="Häufigkeit", row=1, col=3)


    return figure