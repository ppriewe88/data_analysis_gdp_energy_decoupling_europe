from dashboards_and_tables.D4_country_ana.graph_builders import build_graph_countryanalysis, countryanalysis_scatter
from dashboards_and_tables.T1_corr_tables.table_builders import correlation_coeffs_table

def countryanalysis_update_subplots(selected_country, selected_aggregation_level, df_Y, df_Q, gdp_color, energy_color, prod_color):
    
    # Daten auf entsprechende Aggregationsebene filtern
    if selected_aggregation_level == 'years':
        df = df_Y
        chosen_time_step = "Jahr"
    else:
        df = df_Q
        chosen_time_step = "Quartal_label"
    
    # Daten für das ausgewählte Land filtern
    filtered_data = df.loc[df["Land"] == selected_country]

    upper_graph = build_graph_countryanalysis(filtered_data, value_column = "BIP (Mio €)", time_column = chosen_time_step, trace_color = gdp_color)
    middle_graph = build_graph_countryanalysis(filtered_data, value_column = "Energieverbrauch (GWh)", time_column = chosen_time_step, trace_color = energy_color)
    lower_graph = build_graph_countryanalysis(filtered_data, value_column = "Energieproduktivität (Mio€/GWh)", time_column = chosen_time_step, trace_color = prod_color)
    scatter_graph = countryanalysis_scatter(filtered_data, time_column = chosen_time_step, energy_color=energy_color, gdp_color=gdp_color)
    table_corrcoeffs = correlation_coeffs_table(selected_country, df_Y, df_Q)

    return upper_graph, middle_graph, lower_graph, scatter_graph, table_corrcoeffs