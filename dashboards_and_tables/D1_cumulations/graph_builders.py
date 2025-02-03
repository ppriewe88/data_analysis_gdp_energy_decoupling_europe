import pickle
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.io as pio


#################################### Erzeugungsfunktion Kumulationen oberer graph ###################
def cumulations_build_upper_graph(df, time_col, value_col_BIP, value_col_energy):
    return {
        'data': [
                    go.Scatter(
                        x=df[time_col], 
                        y=df[value_col_BIP], 
                        mode="lines",  
                        fill="tozeroy",
                        fillcolor="rgba(0, 100, 255, 0.1)",  # blau mit Transparenz
                        line=dict(color="rgba(0, 100, 255, 1)"), 
                        name="BIP", 
                        yaxis="y2"  # Sekundäre y-Achse
                    ),
                    go.Scatter(
                        x=df[time_col], 
                        y=df[value_col_energy], 
                        mode="lines",  
                        fill="tozeroy", 
                        fillcolor="rgba(255, 100, 0, 0.7)",  # orange mit Transparenz
                        line=dict(color="rgba(255, 100, 0, 1)"),
                        name="Energieverbrauch"
                    )
                ],
        'layout': go.Layout(
                    title="BIP (Mio €) und Energieverbrauch (GWh) über die Zeit (Summe aller Länder)",
                    yaxis={'title': 'Energieverbrauch (GWh)',
                           'side': 'right',
                           'range': [0, df[value_col_energy].max()*2],
                           'showgrid': False},
                    yaxis2={
                        'title': 'BIP (Mio €)',
                        'overlaying': 'y',
                        'side': 'left',  # Setze die sekundäre Achse nach rechts
                        'range': [0, df[value_col_BIP].max()*1.1],
                        'showgrid': False
                    },
                    template="custom_template",
                    showlegend=True,
                    legend={
                        'orientation': 'h',
                        'x': 0.3,  # Position der Legende auf x-achsen-verhältnis
                        'y': 1,     # Höhe der Legende auf y-achsenverhältnis
                        'xanchor': 'left',  # Position relativ zum Punkt (links vom Punkt)
                        'yanchor': 'top'    # Position relativ zum Punkt (oben vom Punkt)
                        },
                    margin=dict(
                        t=40,  # Abstand oben (Title)
                        b=40,  # Abstand unten (x-Achse)
                        l=50,  # Abstand links (y-Achse)
                        r=30   # Abstand rechts
                    )
                        )
            }

'#################################### Erzeugungsfunktion untere graphen ###################'
def cumulations_build_lower_graph(df, time_col, value_col):

    ######## Erstelle Plot
    traces = [
        go.Scatter(
            x=df[df["Land"] == land][time_col],
            y=df[df["Land"] == land][value_col],
            mode="lines",
            fill="tonexty",
            stackgroup="one",
            name=land
        )
        for land in df["Land"].unique()
    ]
    ######## Layout untere Graphen
    layout = go.Layout(
        title=f"{value_col} über Zeit",
        yaxis={'title': f'{value_col}'},
        showlegend=True,
        template="custom_template",
        margin=dict(
            t=50,  # Abstand oben (Title)
            b=40,  # Abstand unten (x-Achse)
            l=50,  # Abstand links (y-Achse)
            r=30   # Abstand rechts
        )
    )
    return {
            'data': traces,
            'layout': layout}