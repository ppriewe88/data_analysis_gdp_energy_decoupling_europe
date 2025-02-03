import pandas as pd
import plotly.express as px

def averages_update_figure(selected_column, df, df_avg, energy_color):

    ############### Sortierung
    sorted_lands = (
    df[df["Jahr"] == 2023]
    .sort_values(by= selected_column, ascending=False)["Land"]
    .tolist()
    )
    df["Land"] = pd.Categorical(df["Land"], categories=sorted_lands, ordered=True)
    
    
    ############## Scatterplot für alle Länder
    fig = px.scatter(
                    df, x="Jahr", y=selected_column, color="Land",
                    labels={"Jahr": "Jahr", selected_column: selected_column},
                    title=f"Zeitverlauf: {selected_column}",
                    category_orders={"Land": sorted_lands},
                    template="custom_template"
                    )

    ################ Durchschnittslinie (roter Verlauf)
    fig.add_scatter(x=df_avg['Jahr'], y = df_avg[selected_column], mode='lines+markers', 
                    line=dict(color=energy_color, width=2), name='Durchschnitt')

    ############## Achsen und Layout
    fig.update_layout(
        xaxis_title="Jahr",
        yaxis_title = selected_column,
        height=500,
        margin=dict(
            t=40,  # Abstand oben (Title)
            b=30,  # Abstand unten (x-Achse)
            l=90,  # Abstand links (y-Achse)
            r=110   # Abstand rechts
        )
    )

    return fig
