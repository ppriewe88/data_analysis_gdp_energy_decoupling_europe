from dash import Dash, html, dcc, callback, Output, Input
from dashboards_and_tables.Styling.global_styling import background_color, html_elements_color, global_border_radius, energy_color

def run_averages_app(df):

    ###################### Durchschnitt BIP für jedes Jahr ###########
    df_avg = df.groupby('Jahr')[['BIP (Mio €)', 'Energieverbrauch (GWh)', 'Energieproduktivität (Mio€/GWh)', 
                                'Kumulativer Energieverbrauch (GWh)', 'Kumulatives BIP (Mio €)']].mean().reset_index()
    ########################## graph builder/update importieren ############
    from dashboards_and_tables.D3_averages.graph_update import averages_update_figure

    ################################# App ########################
    app = Dash(__name__)

    ##################################### Layout ##################
    app.layout = html.Div(
        style = {
            'width': '1200px',
            "backgroundColor": background_color
        },
        children = [
        ###################Überschrift ##################
            html.H4("Europäische Durchschnittswerte",
                    style={
                        "color": "#e5e5e5",        # Textfarbe
                        "fontSize": "20px",        # Schriftgröße
                        "fontWeight": "bold",      # Fettschrift
                        "marginBottom": "4px",    # Abstand nach unten
                        "backgroundColor": html_elements_color,  # Hintergrundfarbe
                        "padding": "10px",         # Innenabstand
                        "borderRadius": global_border_radius,     # Abgerundete Ecken
                        "textAlign": "center",     # Zentrierte Ausrichtung des Textes
                        'font-family': 'Droid Sans, monospace' # Schriftart
                    }
            ),
        ######################### Bereich Radiobutton ################
            html.Div(
                style={
                        "backgroundColor": html_elements_color,
                        "borderRadius": global_border_radius,
                        'display': 'flex',        # Flexbox für Zentrierung
                        'flexDirection': 'column',  # Elemente untereinander anordnen
                        'alignItems': 'center',   # Zentriere Kinder horizontal
                        "marginBottom": "4px"
                    },
                children =[
                    ######################## Radiobutton ################
                    dcc.RadioItems(
                            id='y-axis-selector',
                            options=[
                                {'label': "BIP (Mio €)", 'value': "BIP (Mio €)"},
                                {'label': "Energieverbrauch (GWh)", 'value': "Energieverbrauch (GWh)"},
                                {'label': "Energieproduktivität (Mio€/GWh)", 'value': "Energieproduktivität (Mio€/GWh)"},
                                ],
                            value="BIP (Mio €)",  # Standardauswahl
                            inline=False,
                            labelStyle={
                                'display': 'inline-block', 
                                'marginRight': '5px',  # Abstand zwischen den Optionen
                                'margin-left': '40px',
                                'color': '#e5e5e5',  # Label-Farbe
                                'fontSize': '16px',  # Label-Größe
                                'font-family': 'Droid Sans, monospace' # Schriftart
                                },
                            style={
                                "backgroundColor": html_elements_color,  # Hintergrund für den Radiobutton-Bereich
                                "padding": "10px",  # Innenabstand
                                "borderRadius": global_border_radius,  # Abgerundete Ecken
                                'marginRight': '400px',
                                "marginBottom": "0px",  # Abstand unterhalb des Containers 
                                }
                    )
                ], 
            ),
        ################################## Bereich Graph #######################
        html.Div(
            style = {"padding":"5px", "borderRadius": global_border_radius, "backgroundColor": html_elements_color},
            children = [
                ############################## Graph ##############################
                    dcc.Graph(id='scatter-plot'),
            ]
        )
    ])


    # Callback für die Aktualisierung des Diagramms
    @app.callback(
        Output('scatter-plot', 'figure'),
        Input('y-axis-selector', 'value')
    )
    def call_update_figure(selected_column):
        return averages_update_figure(selected_column, df, df_avg, energy_color)

    # App starten
    ########################### run app  ###########################
    app.run(debug=True, port=8052)