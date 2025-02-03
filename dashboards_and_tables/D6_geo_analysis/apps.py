from dash import Dash, html, dcc, callback, Output, Input
from dashboards_and_tables.Styling.global_styling import background_color, html_elements_color, global_border_radius, energy_color, gdp_color, prod_color

def run_app1(df_Y):

    df_Y_2023 = df_Y.loc[df_Y['Jahr'] == 2023].copy()

    #################################### Dash App initialisieren #########
    app = Dash(__name__)

    ##################################### import graph builders ###########
    from dashboards_and_tables.D6_geo_analysis.graph_builders import build_choropleth, geo_update_graph

    # Layout der App
    ################ Layout erstellen ####################################
    app.layout= html.Div(
        style = {
            'width': '1200px'
        },
        children = [
            ########################## Überschrift #######
            html.H4(
                "BIP und Energieverbrauch im geografischen Vergleich - Jahr 2023 und Entkopplung seit 2008",
                style={
                    "color": "#e5e5e5",        # Textfarbe
                    "fontSize": "20px",        # Schriftgröße
                    "fontWeight": "bold",      # Fettschrift
                    "marginBottom": "4px",    # Abstand nach unten
                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                    "padding": "10px",         # Innenabstand
                    "borderRadius": global_border_radius,     # Abgerundete Ecken
                    "textAlign": "center",     # Zentrierte Ausrichtung des Textes
                    'font-family': 'Droid Sans, monospace'
                }
            ),
            ########################## Radiobutton zum Modus wechseln #######
            html.Div([
                    dcc.RadioItems(
                        id='selected_view',
                        options=[
                            {'label': 'BIP und Energieverbrauch 2023', 'value': 'static_2023'},
                            {'label': 'BIP-Wachstum und Energieentkopplung', 'value': 'growth_and_decoupling'}            
                        ],
                        value='static_2023',  # Standardwert (Länder behalten)
                        labelStyle={'display': 'inline-block', "color":"white", 'font-size': '14px', 'margin-left': '230px'},
                        style = {'font-family': 'Droid Sans, monospace'}),
                ], style={'margin-bottom': '4px', "margin-top":"4px", "border-radius": global_border_radius, "height":"26px","background-color": html_elements_color}),
            ######################## Bereich mit Graphen nebeneinander ####
            html.Div(
                style = {
                    "display": "flex",      # Aktiviert Flexbox
                    "flexDirection": "row", # Elemente nebeneinander anordnen
                    "gap": "4px",          # Abstand zwischen den Boxen
                    "backgroundColor": background_color,
                    "height": "406px",
                    "borderRadius": "10px",     # Abgerundete Ecken
                },
                children = [    
                    html.Div(
                        style = {
                            "flex": "1",      # Aktiviert Flexbox
                            "backgroundColor": html_elements_color,
                            "borderRadius": global_border_radius,
                        },
                        # Graph BIP
                        children = [
                            dcc.Graph(id="choropleth_bip", figure = build_choropleth(dataframe = df_Y_2023, value_column= "BIP_logarithmiert", html_elements_color=html_elements_color),
                                        style = {"padding":"3px"})
                        ]
                    ),
                    html.Div(
                        style = {
                            "flex": "1",      # Aktiviert Flexbox
                            "backgroundColor": html_elements_color,
                            "borderRadius": global_border_radius
                        },
                        # Graph Energie
                        children = [
                            dcc.Graph(id="choropleth_en", figure = build_choropleth(dataframe = df_Y_2023, value_column= "Energieverbrauch_logarithmiert", html_elements_color=html_elements_color),
                                    style = {"padding":"3px"})
                        ]
                    ),
                    
                ]
                )
        ])
    ############### callback  und subploterstellung ##########################################################################
    @app.callback(
        [Output('choropleth_bip', 'figure'),
        Output('choropleth_en', 'figure')],
        Input('selected_view', 'value')
    )
    def update_graph(selected_mode):
        return geo_update_graph(selected_mode, df_Y_2023, html_elements_color)

    ########################### run app  ###########################
    app.run(debug=True, port=8055)



def run_app2(df_Y):

    from dashboards_and_tables.D6_geo_analysis.graph_builders import build_choropleth
    df_Y_2023 = df_Y.loc[df_Y['Jahr'] == 2023].copy()

    # Dash App initialisieren
    app = Dash(__name__)

    # Layout der App
    ################ Layout erstellen ####################################
    app.layout= html.Div(
        style = {
            'width': '1200px'
        },
        children = [
            ########################## Überschrift #######
            html.H4(
                "Energieproduktivität im geografischen Vergleich (Jahr 2023)",
                style={
                    "color": "#e5e5e5",        # Textfarbe
                    "fontSize": "20px",        # Schriftgröße
                    "fontWeight": "bold",      # Fettschrift
                    "marginBottom": "5px",    # Abstand nach unten
                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                    "padding": "10px",         # Innenabstand
                    "borderRadius": global_border_radius,     # Abgerundete Ecken
                    "textAlign": "center",     # Zentrierte Ausrichtung des Textes
                    'font-family': 'Droid Sans, monospace'
                }
            ),
            ######################## Bereich mit Graph ###################
            html.Div(
                style = {
                    "backgroundColor": html_elements_color,
                    "borderRadius": global_border_radius,     # Abgerundete Ecken
                },
                children = [
                            dcc.Graph(id="choropleth_en", figure = build_choropleth(dataframe = df_Y_2023, value_column= "Energieproduktivität (Mio€/GWh)", html_elements_color=html_elements_color),
                                    style = {"padding":"10px"})
                    ]
            )
        ]
    )


    ########################### run app  ###########################
    app.run(debug=True, port=8056)


def run_app3(df_Q):

    from dashboards_and_tables.D6_geo_analysis.graph_builders import build_animated_choropeth

    ######################################## initialisiere app ####################
    app = Dash(__name__)

    ###################################### Layout ##################
    app.layout = html.Div(
        style = {
            'width': '1200px'
        },
        children = [
            ########################## Überschrift #######
            html.H4(
                "Erreichungsgrad Jahresmaximalproduktivität europäischer Länder im zeitlichen Verlauf",
                style={
                    "color": "#e5e5e5",        # Textfarbe
                    "fontSize": "20px",        # Schriftgröße
                    "fontWeight": "bold",      # Fettschrift
                    "marginBottom": "5px",    # Abstand nach unten
                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                    "padding": "10px",         # Innenabstand
                    "borderRadius": global_border_radius,     # Abgerundete Ecken
                    "textAlign": "center",     # Zentrierte Ausrichtung des Textes
                    'font-family': 'Droid Sans, monospace' # Schriftart
                }
            ),
            ######################## Bereich mit Graph ###################
            html.Div(
                style = {
                    "backgroundColor": html_elements_color,
                    "borderRadius": global_border_radius,     # Abgerundete Ecken
                },
                children = [
                    dcc.Graph(id='choropleth_prod', figure = build_animated_choropeth(df_Q, html_elements_color), style = {"padding":"10px"}),
                ]
            )
        ]
    )


    app.run(debug=True, port=8057)


def run_app4(df, formatted_df):

    options_countries = [{'label': 'Alle Länder (kumuliert)', 'value': 'Alle'}] + [{'label': country, 'value': country} for country in sorted(df.Land.unique())]

    ####################### import graph builder ##############
    from dashboards_and_tables.D6_geo_analysis.graph_builders import build_seasonal_peaks_numerical

    ################ Dash App initialisieren #######################
    app = Dash(__name__)

    ################ Layout erstellen ####################################
    app.layout = html.Div(
        style = {
                "width": '1200px',
                "background-color": background_color
                },
        children = 
        [
            ########################## Überschrift #######
            html.H4(
                "Häufigkeit Jahresmaxima In Quartalen ",
                style={
                    "color": "#e5e5e5",        # Textfarbe
                    "fontSize": "20px",        # Schriftgröße
                    "fontWeight": "bold",      # Fettschrift
                    "marginBottom": "5px",    # Abstand nach unten
                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                    "padding": "10px",         # Innenabstand
                    "borderRadius": global_border_radius,     # Abgerundete Ecken
                    "textAlign": "center",     # Zentrierte Ausrichtung des Textes
                    'font-family': 'Droid Sans, monospace',
                }
            ),
            ########################## Bereich mit Dropdown Länderauswahl
                html.Div([
                        dcc.Dropdown(
                            id='dropdown_countries',
                            options= options_countries,
                            value='Alle',
                            style = {'font-family': 'Droid Sans, monospace', "margin-left":"60px", "width":"870px"})
                    ], style = {'margin-bottom': '4px', "padding":"3px", "border-radius": global_border_radius, "background-color": html_elements_color}
                ),
            ########################## Bereich mit Graph #############
            html.Div([
                    dcc.Graph(id='graph_hist'),
                ], style = {'margin-bottom': '5px', "border-radius": global_border_radius, "padding":"6px", "background-color": html_elements_color}
            ),
        ]
    )

    ############### callback  und subploterstellung ##########################################################################
    @app.callback(
        Output('graph_hist', 'figure'),
        Input('dropdown_countries', 'value')
    )
    def update_graph(selected_country):
        return build_seasonal_peaks_numerical(selected_country, formatted_df, gdp_color, energy_color, prod_color)

    ########################### run app  ###########################
    app.run(debug=True, port=8058)