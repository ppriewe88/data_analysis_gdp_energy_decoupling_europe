from dash import Dash, html, dcc, callback, Output, Input
from dashboards_and_tables.Styling.global_styling import background_color, html_elements_color, global_border_radius


def run_cumulations_app(df_Y, df_Q):
    #################################### zu verwendende Hilfs-Dataframes ###################
    df_Y_cumulated_country_sums = df_Y.groupby("Jahr")[["Energieverbrauch (GWh)", "Kumulativer Energieverbrauch (GWh)", "BIP (Mio €)", "Kumulatives BIP (Mio €)"]].sum().reset_index()
    df_Q_cumulated_country_sums = df_Q.groupby(["Jahr", "Quartal", "Quartal_label"])[["Energieverbrauch (GWh)", "Kumulativer Energieverbrauch (GWh)", "BIP (Mio €)", "Kumulatives BIP (Mio €)"]].sum().reset_index()

    ################################### graph builders und update importieren #############
    from dashboards_and_tables.D1_cumulations.graph_builders import cumulations_build_upper_graph, cumulations_build_lower_graph
    from dashboards_and_tables.D1_cumulations.graphs_update import cumulations_update_graphs
    #################################### App ###################

    app = Dash(__name__)

    #################################### Layout ###########
    width_html_frame = 1400
    app.layout = html.Div(
        style = {
            'width': f'{width_html_frame}px',
            "backgroundColor": background_color
        },
        children =[ 
            ###################Überschrift ##################
            html.H4("Summenbetrachtung der europäischen Länder",
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
            ########### Bereich für Dropdown #########################
            html.Div(
                style={
                    "backgroundColor": html_elements_color,
                    "padding": "2px",         # Innenabstand
                    "borderRadius": global_border_radius,
                    'display': 'flex',        # Flexbox für Zentrierung
                    'flexDirection': 'column',  # Elemente untereinander anordnen
                    'alignItems': 'center',   # Zentriere Kinder horizontal
                    "marginBottom": "4px"
                },
                children = [
                    ##################### Dropdown #######################
                    html.Div(
                        style={
                            "backgroundColor": html_elements_color,
                            "borderRadius": global_border_radius,
                            "height":"35px",
                            "width": "50%"  # Begrenze die Breite relativ zum Elterncontainer
                        },
                        children=[
                            dcc.Dropdown(
                                id='dataframe_selector',
                                options=[
                                    {'label': 'Kumulierte Summen (alle Länder; über Zeit aufsummiert)', 'value': 'year_cumul'},
                                    {'label': 'Jahresbeträge', 'value': 'year_single'},
                                    {'label': 'Quartalsbeträge', 'value': 'quarter_single'}   
                                ],
                                value='year_cumul',
                                style = {
                                    "width": "100%",  # Dropdown füllt Container aus
                                    "height":"15px",
                                    'font-family': 'Droid Sans, monospace',
                                })
                        ]
                    )
                ]
            ),
            ################# Bereich: Oberer Graph
            html.Div(
                [dcc.Graph(
                    id='upper_graph',
                    figure= cumulations_build_upper_graph(df_Y_cumulated_country_sums, time_col = "Jahr", value_col_BIP = "Kumulatives BIP (Mio €)", value_col_energy = "Kumulativer Energieverbrauch (GWh)"),
                    style = {'margin-bottom': '0px', 'width':'100%', "height":"400px"})
                ], 
                style = {"padding":"5px", "borderRadius": global_border_radius, "backgroundColor": html_elements_color}
            ), 
            ################# Bereich: Untere Graphen
            html.Div([
                # linker graph
                dcc.Graph(id='lower_left_graph', figure = cumulations_build_lower_graph(df_Y, time_col = "Jahr", value_col = "Kumulatives BIP (Mio €)"),
                        style={'display': 'inline-block', 'width': '50%', "height":"300px"}), 
                # rechter graph
                dcc.Graph(id='lower_right_graph', figure = cumulations_build_lower_graph(df_Y, time_col = "Jahr", value_col = "Kumulativer Energieverbrauch (GWh)"),
                        style={'display': 'inline-block', 'width': '50%', "height":"300px"})
                    ], 
            style={'margin-top': '0px', "borderRadius": global_border_radius,"padding":"5px", 'width': f'{width_html_frame-10}px', "backgroundColor": html_elements_color})
        ]
    )

    #################################### Callback für Aggregationsauswahl ###################
    @app.callback(
        [Output('upper_graph', 'figure'),
        Output('lower_left_graph', 'figure'),
        Output('lower_right_graph', 'figure')],
        [Input('dataframe_selector', 'value')]
    )
    def call_update_graphs(selected_aggregation_level):
        return cumulations_update_graphs(selected_aggregation_level, df_Y_cumulated_country_sums, df_Y, df_Q_cumulated_country_sums, df_Q)

    #################################### Start der App ##################################
    app.run(debug=True, port=8051)