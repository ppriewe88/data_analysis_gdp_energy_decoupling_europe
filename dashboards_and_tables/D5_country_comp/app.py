from dash import Dash, html, dcc, callback, Output, Input
from dashboards_and_tables.Styling.global_styling import background_color, html_elements_color, global_border_radius, gdp_color, energy_color, prod_color


def country_comparison_run_app(df_Y):

    width_graph = 1200
    height_graph = 600
    padding_graph = 5

    ########################### import graph builder / update ###########
    from dashboards_and_tables.D5_country_comp.graph_update import country_comparison_update_graph

    ################ Dash App initialisieren #######################
    app = Dash(__name__)

    ################ Layout erstellen ####################################
    app.layout = html.Div(
        style = {
                "width": f'{width_graph + padding_graph * 2}px',
                "background-color": background_color
                },
        children = 
            [
            ###################Überschrift ##################
            html.H4("Länder im Vergleich - Rankings",
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
            ######################### slider #################
            html.Div([
                    dcc.Slider(
                            id='time-slider',
                            min=df_Y["Jahr"].min(),
                            max=df_Y["Jahr"].max(),
                            value=2023,
                            marks={str(year): {'label': str(year), 'style': {'color': 'white'}} for year in df_Y["Jahr"].unique()},
                            step=1,
                            )
                ], style={'margin-bottom': '3px', "padding-top":"3px", 'font-family': 'Droid Sans, monospace', "border-radius": global_border_radius, "background-color": html_elements_color}),

            html.Div([
            ######################### Radiobutton Top 6 entfernen
                    dcc.RadioItems(
                        id='remove-top6-bip',
                        options=[
                            {'label': 'Alle Länder', 'value': 'keep'},
                            {'label': 'Ohne 6 größte BIP-Erzeuger aus 2023 (DEU, FRA, ITA, ESP, NLD, TUR)', 'value': 'remove'}            
                        ],
                        value='keep',  # Standardwert (Länder behalten)
                        labelStyle={'display': 'inline-block', 'color': 'white', 'margin-left': '40px'},
                        style = {'font-family': 'Droid Sans, monospace'}),
                ], style={'margin-bottom': '3px', 'font-family': 'Droid Sans, monospace', "height":"28px", "border-radius": global_border_radius, "background-color": html_elements_color}),

            ########################## dropdown sortierung
                html.Div([
                        dcc.Dropdown(
                            id='dropdown',
                            options=[
                                {'label': 'BIP absteigend', 'value': 'BIP (Mio €)'},
                                {'label': 'Energieverbrauch absteigend', 'value': 'Energieverbrauch (GWh)'},
                                {'label': 'Energieproduktivität absteigend', 'value': 'Energieproduktivität (Mio€/GWh)'},
                                {'label': 'Alle Kategorien absteigend', 'value': 'alle'},
                            ],
                            value='alle',
                            style = {'font-family': 'Droid Sans, monospace', "margin-left":"80px", "width":"800px"})
                    ], style = {"padding":"3px",'margin-bottom': '5px', "border-radius": global_border_radius, "background-color": html_elements_color}
                ),
            ########################## eigentlicher graph als multi-graph
            html.Div([
                    dcc.Graph(id='sortierter_graph', clickData=None,
                            style = {"padding":f"{padding_graph}px", "border-radius": global_border_radius, "background-color": html_elements_color}),
                ], style = {'margin-bottom': '5px', "border-radius": global_border_radius, "background-color": html_elements_color}
            ),
            ]
    )

    ############### callback  und subploterstellung ##########################################################################
    @app.callback(
        Output('sortierter_graph', 'figure'),
        [Input('dropdown', 'value'),
        Input('time-slider', 'value'),
        Input('remove-top6-bip', 'value'),  # RadioButton Input
        Input('sortierter_graph', 'clickData')]
    )
    def update_graph(selected_sorting, selected_year, remove_top6_bip, click_data):
        return country_comparison_update_graph(selected_sorting, selected_year, remove_top6_bip, click_data,
                    df_Y, width_graph, height_graph, gdp_color, energy_color, prod_color)

    ########################### run app  ###########################
    app.run(debug=True, port=8054)