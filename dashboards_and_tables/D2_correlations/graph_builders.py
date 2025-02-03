import plotly.express as px

def correlations_moving_regression(df, gdp_color, energy_color):

    # Achsen-Maxima
    x_max = df["Energieverbrauch (GWh)"].max()
    y_max = df["BIP (Mio €)"].max()

    # Bedingte Formatierung für Deutschland und Türkei
    df['marker_size'] = df['Land'].apply(lambda x: 14 if x == x in ['Germany', 'Türkiye'] else 10)
    # Textspalte hinzufügen, die den Namen anzeigt
    df['text'] = df['Land']

    # plot
    fig = px.scatter(df, 
                    x="Energieverbrauch (GWh)", y="BIP (Mio €)", 
                    hover_data=["Land", "Energieverbrauch (GWh)", "BIP (Mio €)"] 
                    , trendline= "ols"
                    , trendline_color_override=energy_color
                    ,animation_frame="Jahr",
                    template="custom_template"
                    )


    fig.update_layout(
        
        # Achsen-Skalierung, Tausendertrennzeichen (automatisch durch `tickformat`), Achsenmaxima festlegen
        xaxis=dict(tickformat=",", title="Energieverbrauch (GWh)", range=[0, x_max + 1000]),
        yaxis=dict(tickformat=",", title="BIP (Mio €)", side="left", range=[0, y_max + 10]),
        
        # Größe des Plots festlegen
        height=500,  # Höhe in Pixel
        width=1000,    # Breite in Pixel

        # Diagrammtitel hinzufügen
        title="Zusammenhang zwischen Energieverbrauch und BIP"
    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10



    # Hover-Template für Punkt als Tausender-Trennzeichen; Größe der marker
    fig.update_traces(
        hovertemplate=(
            "Land: %{customdata[0]}<br>"
            "Energieverbrauch: %{x:,.0f} GWh<br>"
            "BIP: %{y:,.0f} Mio €"
        ),
        customdata=df[["Land"]],
        marker=dict(
            color= gdp_color,  # Markerfarbe abhängig vom Land
            size= 10)   # Markergroße abhängig vom Land
    )
    return fig