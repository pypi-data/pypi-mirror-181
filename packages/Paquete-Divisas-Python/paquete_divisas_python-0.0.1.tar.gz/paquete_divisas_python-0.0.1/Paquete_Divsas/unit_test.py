import krakenex
from pykrakenapi import KrakenAPI
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
import pytest
from proyecto_divisas import krakenex_data_import
from proyecto_divisas import Moving_Average
from proyecto_divisas import RSI

####################### KRAKEN DATA IMPORT UNIT TEST #######################
def test_krakenex_data_import_types():
    api, k, data, pairs = krakenex_data_import()
    assert str(type(api)) == "<class 'krakenex.api.API'>","api class should be: <class 'krakenex.api.API'>, instead of " + str(type(api))
    assert str(type(k)) == "<class 'pykrakenapi.pykrakenapi.KrakenAPI'>", "k class should be: <class 'pykrakenapi.pykrakenapi.KrakenAPI'>, instead of " + str(type(k))
    assert str(type(data)) == "<class 'pandas.core.frame.DataFrame'>", "data class should be: <class 'pandas.core.frame.DataFrame'>, instead of " + str(type(data))
    assert str(type(pairs)) == "<class 'list'>", "pairs class should be: <class 'list'>, instead of " + str(type(pairs))

####################### MOVING AVERAGE UNIT TEST #######################
def test_Moving_Average_calculate():
    df_test_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    df_test_colums = ["close"]
    df_input = pd.DataFrame(df_test_values, columns = df_test_colums)
    df_test = Moving_Average(2, df_input).calculate()
    assert list(df_test.moving_average_2) == [1.0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5], "Moving_Average.calculate() is not calculating the moving average correctly"

####################### RSI UNIT TEST #######################
def test_RSI():
    df_test_values = {"open":[1, 2, 8, 5, 6, 31, 2, 8, 5, 6, 31, 2, 8, 5, 6, 3, 2, 8, 5, 6, 31, 2, 8, 5, 6, 31, 2, 8, 5, 6, 31, 2, 8, 5, 6, 3],
                 "close":[2, 8, 5, 6, 3, 12, 8, 5, 6, 3, 12, 8, 5, 6, 3, 1, 8, 5, 6, 3, 12, 8, 5, 6, 3, 12, 8, 5, 6, 3, 12, 8, 5, 6, 3, 1]}
    df_input = pd.DataFrame(df_test_values)
    df_test = RSI(df_input).calculate()
    solution = [29.33333333333333,27.272727272727266,20.54794520547945,27.631578947368425,25.641025641025635,27.631578947368425,
    35.0,20.54794520547945,27.631578947368425,25.641025641025635,27.631578947368425,35.0,20.54794520547945,27.631578947368425,
    25.641025641025635,27.631578947368425,27.272727272727266,16.666666666666657,22.58064516129032,21.05263157894737,22.58064516129032,
    27.272727272727266,20.54794520547945]
    assert list(df_test.RSI) == solution, "RSI.calculate() is not calculating the RSI column correctly"
