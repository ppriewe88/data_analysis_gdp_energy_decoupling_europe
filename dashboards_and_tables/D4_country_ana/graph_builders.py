import plotly.express as px
import plotly.graph_objects as go

' ############################################ scatter builder (right plot)'
def countryanalysis_scatter(dataframe, time_column, energy_color, gdp_color):
    # plot
    fig = px.scatter(dataframe, 
                x="Energieverbrauch (GWh)", y="BIP (Mio €)", 
                hover_data= ["Land", "Energieverbrauch (GWh)", "BIP (Mio €)", time_column],
                trendline= "ols",
                trendline_color_override=energy_color
                )
    # Punktgröße anpassen
    fig.update_traces(marker=dict(size=10, color=gdp_color))

    fig.update_layout(
        
        # Achsen-Skalierung, Tausendertrennzeichen (automatisch durch `tickformat`), Achsenmaxima festlegen
        xaxis=dict(title="Energieverbrauch (GWh)"
                   ),
        yaxis=dict(title="BIP (Mio €)", side="left"
                   ),
        title="Scatterplot Energieverbrauch/BIP (alle Zeitpunkte)",
        template = 'custom_template'
    )  
    return fig


' ############################ build large graphe (triple row) ##############'
def build_graph_countryanalysis(dataframe, value_column, time_column, trace_color):
        if time_column == "Jahr":
            densitity_of_ticks = 1
        else:
            densitity_of_ticks = 4
        
        return{
                'data': [
                    go.Scatter(
                        x=dataframe[time_column],
                        y=dataframe[value_column],
                        mode="lines+markers",
                        line=dict(color= trace_color)
                    ),
                ],
                'layout': 
                go.Layout(
                        title= value_column,
                        template='custom_template',
                        yaxis = dict(
                            title=dict(
                                text=value_column,  # Titeltext
                                font=dict(
                                    size=11  # Schriftgröße festlegen
                                )
                            )
                        ),
                        xaxis=dict(
                            tickvals= dataframe[time_column].iloc[::densitity_of_ticks].tolist(),  # Nur jedes vierte Wert als Tick
                            ticktext= dataframe[time_column].iloc[::densitity_of_ticks].tolist(),  # Behalte dieselben Werte als Ticks
                            type="category"  # Kategorische Achse
                        ),
                        margin=dict(
                            l=50,  # Abstand links
                            r=50,  # Abstand rechts
                            t=40,  # Abstand oben
                            b=20   # Abstand unten
                        )
                )
            }