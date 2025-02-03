from dashboards_and_tables.D1_cumulations.graph_builders import cumulations_build_lower_graph, cumulations_build_upper_graph

def cumulations_update_graphs(selected_aggregation_level, df_Y_cumulated_country_sums, df_Y, df_Q_cumulated_country_sums, df_Q):
    # Wähle den entsprechenden DataFrame basierend auf der Auswahl
    if selected_aggregation_level in ['year_cumul', 'year_single']:
        df_upper_graph = df_Y_cumulated_country_sums  # Beispiel DataFrame für Germany
        df_lower_graph = df_Y  # Beispiel DataFrame für yearly Daten
        chosen_time_step = "Jahr"
    elif selected_aggregation_level == 'quarter_single':
        df_upper_graph = df_Q_cumulated_country_sums  # Beispiel DataFrame für Germany
        df_lower_graph = df_Q  # Beispiel DataFrame für yearly Daten
        chosen_time_step = "Quartal_label"
    else:
        raise Exception("Fehleingabe dropdown")

    if selected_aggregation_level == 'year_cumul':
        chosen_value_column_left = "Kumulatives BIP (Mio €)"
        chosen_value_column_right = "Kumulativer Energieverbrauch (GWh)"
        chosen_value_col_BIP = "Kumulatives BIP (Mio €)" 
        chosen_value_col_energy = "Kumulativer Energieverbrauch (GWh)"
    elif selected_aggregation_level in ['year_single','quarter_single']:
        chosen_value_column_left = "BIP (Mio €)"
        chosen_value_column_right = "Energieverbrauch (GWh)"
        chosen_value_col_BIP = "BIP (Mio €)" 
        chosen_value_col_energy = "Energieverbrauch (GWh)"
    else:
        raise Exception("Fehleingabe dropdown")

    # Erzeuge die Graphen basierend auf den neuen DataFrames
    upper_graph = cumulations_build_upper_graph(df_upper_graph, chosen_time_step, value_col_BIP = chosen_value_col_BIP, value_col_energy = chosen_value_col_energy)
    lower_graph_1 = cumulations_build_lower_graph(df_lower_graph, time_col = chosen_time_step, value_col = chosen_value_column_left)
    lower_graph_2 = cumulations_build_lower_graph(df_lower_graph, time_col = chosen_time_step, value_col = chosen_value_column_right)

    return upper_graph, lower_graph_1, lower_graph_2