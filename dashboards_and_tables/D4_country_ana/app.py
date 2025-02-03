from dash import Dash, html, dcc, callback, Output, Input
from dashboards_and_tables.Styling.global_styling import background_color, html_elements_color, global_border_radius, gdp_color, energy_color, prod_color

def country_analysis_run_app(df_Y, df_Q, df):

    ################### import graph and table builders ###############
    from dashboards_and_tables.T1_corr_tables.table_builders import correlation_coeffs_table
    from dashboards_and_tables.D4_country_ana.graph_builders import countryanalysis_scatter, build_graph_countryanalysis
    from dashboards_and_tables.D4_country_ana.graphs_update import countryanalysis_update_subplots

    ################ Dash App initialisieren #######################
    app = Dash(__name__)

    ################ Layout erstellen ####################################
    app.layout= html.Div(
        style = {
            'height':'1000px',
            'width': '1400px',
            'min-height': '200px',  # Mindestens 200px hoch
            'min-width': '600px',  # Mindestens 200px hoch
            'max-height': '1000px',  # Maximal 600px hoch
            'max-width': '1400px'  # Maximal 600px hoch
        },
        children = [
            ########################## Überschrift #######
            html.H4(
                "Länderanalyse im Detail",
                style={
                    "color": "#e5e5e5",        # Textfarbe
                    "fontSize": "20px",        # Schriftgröße
                    "fontWeight": "bold",      # Fettschrift
                    "marginBottom": "4px",    # Abstand nach unten
                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                    "padding": "10px",         # Innenabstand
                    "borderRadius": global_border_radius,     # Abgerundete Ecken
                    "textAlign": "center",     # Zentrierte Ausrichtung des Textes
                    'font-family': 'Droid Sans, monospace',
                }
            ),
            ######################### Bereich mit zwei Spalten ####
            html.Div(
                style = {
                    "display": "flex",      # Aktiviert Flexbox
                    "flexDirection": "row", # Elemente nebeneinander anordnen
                    "gap": "2px",          # Abstand zwischen den Boxen
                    "height": "600px",
                    "backgroundColor": background_color
                },
                children = [
                    ##################### linker Bereich ############
                    html.Div(
                        style={
                            "backgroundColor": background_color,
                            "flex": "3",
                            'height': '700px',
                            "borderRadius": global_border_radius},
                        children = [
                            ##### Überschrift #####
                            html.H5(
                                "Zeitlicher Verlauf Analysegrößen",
                                style={
                                    "color": "#e5e5e5",        # Textfarbe
                                    "fontSize": "16px",        # Schriftgröße
                                    "fontWeight": "bold",      # Fettschrift
                                    "marginBottom": "5px",    # Abstand nach unten
                                    "marginTop": "2px",
                                    "marginLeft": "5px",
                                    "marginRight": "5px",
                                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                                    "padding": "5px",          # Innenabstand
                                    "borderRadius": global_border_radius,      # Abgerundete Ecken
                                    'font-family': 'Droid Sans, monospace',
                                    "textAlign": "center"
                                }
                            ),
                            ######## Hier: 3-er Subplots (Graph mit subplots)
                            html.Div(
                                style = {
                                        "borderRadius": global_border_radius,
                                        "padding": "10px",
                                        'height': '635px',
                                        "backgroundColor": html_elements_color,
                                        'display': 'flex', 
                                        'marginRight': '5px',
                                        'marginLeft': '5px',
                                        'flexDirection': 'column', 
                                        'gap': '5px'
                                },
                                children = [
                                    #dcc.Graph(id='kumulierter_graph', style={'width': '100%'})]
                                    dcc.Graph(id = 'graph_bip', figure = build_graph_countryanalysis(df_Y, value_column = "BIP (Mio €)", time_column = "Jahr", trace_color = gdp_color),
                                            style = {'height':'33%', 'width': '98%', 'marginLeft': '5px'}),
                                    dcc.Graph(id = 'graph_en', figure = build_graph_countryanalysis(df_Y, value_column = "Energieverbrauch (GWh)", time_column = "Jahr", trace_color = energy_color),
                                            style = {'height':'33%', 'width': '98%', 'marginLeft': '5px'}),
                                    dcc.Graph(id = 'graph_prod', figure = build_graph_countryanalysis(df_Y, value_column = "Energieproduktivität (Mio€/GWh)", time_column = "Jahr", trace_color = prod_color),
                                            style = {'height':'33%', 'width': '98%', 'marginLeft': '5px'})
                                ]
                            )
                        ]
                    ),
                    ######################### rechter Bereich ###########
                    html.Div(
                        style={
                            "backgroundColor": background_color,
                            "flex": "2",
                            'height': '700px',
                            "borderRadius": global_border_radius},
                        children = [
                            ##### Überschrift #####
                            html.H5(
                                "Optionen (für alle abgebildeten Graphen)",
                                style={
                                    "color": "#e5e5e5",        # Textfarbe
                                    "fontSize": "16px",        # Schriftgröße
                                    "fontWeight": "bold",      # Fettschrift
                                    "marginBottom": "5px",    # Abstand nach unten
                                    "marginTop": "2px",
                                    "marginLeft": "5px",
                                    "marginRight": "5px",
                                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                                    "padding": "5px",          # Innenabstand
                                    "borderRadius": global_border_radius,      # Abgerundete Ecken 
                                    'font-family': 'Droid Sans, monospace',
                                    "textAlign": "center"
                                }
                            ),
                            ######## Hier die Optionen #######################
                            html.Div(
                                style={"display": "flex",
                                    "flexDirection":"row",
                                    "gap": "5px",
                                    "marginTop": "5px",
                                    "marginLeft": "5px",
                                    "marginRight": "5px",
                                    "background-color": html_elements_color,
                                    "borderRadius": global_border_radius,
                                    "height":"56px"
                                },
                                children = [
                                    dcc.Dropdown(
                                        id='select_country',
                                        options= sorted(df.Land.unique()),
                                        value='Germany',
                                        style = {
                                            "padding": "5px",
                                            "flex": "1",
                                            "border-radius": global_border_radius,
                                            "height":"20px",
                                            "width":"260px",
                                            'font-family': 'Droid Sans, monospace'
                                        }
                                        ),
                                    dcc.RadioItems(
                                        id='select_aggregation_level',
                                        options=[
                                            {'label': 'Zeiteinheit: Jahre', 'value': 'years'},
                                            {'label': 'Zeiteinheit: Quartale', 'value': 'quarters'}            
                                        ],
                                        value='years',  # Standardwert (Länder behalten)
                                        labelStyle={'margin-left': '20px'}, # 'display': 'inline-block', 
                                        style = {"padding": "5px",
                                                "background-color": "white",  # Weißer Hintergrund
                                                "border-radius": global_border_radius,      # Optional: Abgerundete Ecken
                                                "marginRight" : "5px",
                                                "marginTop" : "5px",
                                                "flex": "1",
                                                "height":"36px",
                                                'font-family': 'Droid Sans, monospace'
                                        }
                                    )
                                ]
                            ),
                            ##### Hier die nächste Überschrift #####
                            html.H5(
                                "Scatterplot und statistische Informationen",
                                style={
                                    "color": "#e5e5e5",        # Textfarbe
                                    "fontSize": "16px",        # Schriftgröße
                                    "fontWeight": "bold",      # Fettschrift
                                    "marginBottom": "0px",    # Abstand nach unten
                                    "marginTop": "5px",
                                    "marginLeft": "5px",
                                    "marginRight": "5px",
                                    "backgroundColor": html_elements_color,  # Hintergrundfarbe
                                    "padding": "5px",          # Innenabstand
                                    "borderRadius": global_border_radius,      # Abgerundete Ecken 
                                    'font-family': 'Droid Sans, monospace',
                                    "textAlign": "center"
                                }
                            ),
                            ################## hier der Scatterplot #######
                            html.Div(
                                style = {
                                        "borderRadius": global_border_radius,
                                        "padding": "10px",
                                        'height': '541px',
                                        "backgroundColor": html_elements_color,
                                        'marginTop': '5px',
                                        'marginRight': '5px',
                                        'marginLeft': '5px',
                                        'display': 'flex', 
                                        'flexDirection': 'column', 
                                        'gap': '5px'
                                },
                                children = [
                                    ####### graph scatter plot ####
                                    dcc.Graph(id = 'graph_scatter', figure = countryanalysis_scatter(df_Y, time_column = "Jahr", energy_color=energy_color, gdp_color=gdp_color),
                                            style = {}),
                                    ####### tabelle korr.koeffizienten
                                    dcc.Graph(id = 'table_korrcoeffs', figure = correlation_coeffs_table("Germany", df_Y, df_Q),
                                            style = {})
                                ]
                            )
                        ],
                    )
                ]
            ),
        ]  
        ),

    ################ Callbacks ####################################
    @app.callback(
        [Output('graph_bip', 'figure'),
        Output('graph_en', 'figure'),
        Output('graph_prod', 'figure'),
        Output('graph_scatter', 'figure'),
        Output('table_korrcoeffs', 'figure')],
        [Input('select_country', 'value'),
        Input('select_aggregation_level', 'value')]
    )
    ############### Ploterstellung
    def call_update_countryanalysis_subplots(selected_country, selected_aggregation_level):
        return countryanalysis_update_subplots(selected_country, selected_aggregation_level, df_Y, df_Q, gdp_color, energy_color, prod_color)

    ########################### run app  ###########################
    app.run(debug=True, port=8053)