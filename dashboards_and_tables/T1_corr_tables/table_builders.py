import pandas as pd
import plotly.graph_objects as go

' ######################## correlation table ###########'
def correlation_table(df, mode, html_elements_color):
    
    # auslesen, ob Korr.koeff. für Länder oder Jahre berechnet werden sollen
    if mode == "Jahre":
        selected_entity = "Jahr"
    elif mode == "Land":
        selected_entity = "Land"
    else:
        raise Exception("error in show_correlation_table: wrong input for 'mode'")

    # hilfsvariablen
    correlation_dict = {} # container für korr.koeffizienten
    entities = df[selected_entity].unique() # liste Länder/Jahre (je nachdem was an Funktion übergeben wird)
    cell_colors = ['#555555']  # Liste für Zellfarben

    # Korrelationskoeffizienten für jedes Jahr berechnen
    for entity in entities:
        df_entities = df.loc[df[selected_entity] == entity]
        correlation = df_entities["Energieverbrauch (GWh)"].corr(df_entities["BIP (Mio €)"]).round(3)
        correlation_dict[entity] = correlation
        # Zellfarbe basierend auf Korrelationswert bestimmen
        if correlation < -0.2:
            cell_colors.append('#2e5618')
        elif -0.2 <= correlation <= 0.2:
            cell_colors.append("#4e4d4c") 
        else:
            cell_colors.append('#b14831')

    # DataFrame mit Korrelationskoeffizienten
    correlations = pd.DataFrame(correlation_dict, index=["Korrelationskoeffizient BIP/Energieverbrauch"])

    # Tabelle
    fig = go.Figure(data=[go.Table(
        header=dict(values=[mode] + [str(entity) for entity in entities],
                    fill_color=html_elements_color,  # Hintergrundfarbe der Zellen
                    font=dict(color='white', size=12),  # Schriftfarbe und Größe
                    ),
        cells=dict(values=[["Korrelationskoeffizient<br>BIP/Energieverbrauch"]] + [correlations[entity] for entity in entities],
                    fill=dict(color=cell_colors),
                    font=dict(color='white', size=12),  # Schriftfarbe und Größe
                ),
        columnwidth = [190] + [90]*len(entities)
    )])

    # Spaltenbreite anpassen (hier nur die erste Spalte verbreitern)
    fig.update_layout(
        margin=dict(t=5, b=5, l=5, r=5),
        height=80,
        width=1200
        )
    # Zeige die Tabelle
    return fig


' ######################## correlation coefficients table ###########'
def correlation_coeffs_table(country, df_Y, df_Q):
    # filtern
    df_Y_filtered = df_Y.loc[df_Y["Land"]==country]
    df_Q_filtered = df_Q.loc[df_Q["Land"]==country]

    corr_Y = df_Y_filtered["Energieverbrauch (GWh)"].corr(df_Y_filtered["BIP (Mio €)"]).round(3)
    corr_Q = df_Q_filtered["Energieverbrauch (GWh)"].corr(df_Q_filtered["BIP (Mio €)"]).round(3)

    if corr_Y < -0.2:
        cell_color_Y = '#2e5618'
    elif -0.2 <= corr_Y <= 0.2:
        cell_color_Y  = "#4e4d4c"
    else:
        cell_color_Y = '#b14831'

    if corr_Q < -0.2:
        cell_color_Q = '#2e5618'
    elif -0.2 <= corr_Q <= 0.2:
        cell_color_Q  = "#4e4d4c"
    else:
        cell_color_Q = '#b14831'

    # Erstellen der Plotly-Tabelle
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["Korr.koeff. BIP/Energie <b>Jahresverlauf","Korr.koeff. BIP/Energie <b>Quartalsverlauf"],
                    fill_color= '#555555',
                    align='center',
                    font=dict(size=12, color = "white")
                ),
                cells=dict(
                    values=[corr_Y, corr_Q],
                    fill=dict(color=[cell_color_Y, cell_color_Q]),
                    align='center',
                    font=dict(size=14, color = "white"),
                    height = 30))])
    
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=90,
        template = 'custom_template'
        )

    return fig