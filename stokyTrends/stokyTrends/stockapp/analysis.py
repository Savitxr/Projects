import pandas as pd
import  numpy as np
from yahoo_fin.stock_info import get_data
import plotly.graph_objects as go
def calculate_sma(data, window=20):
    sma = data.rolling(window=window).mean()
    return sma

def plot_stock_with_multiple_moving_averages(df, sma_50=None, sma_100=None, sma_150=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Stock Price'))

    if sma_50 is not None:
        fig.add_trace(go.Scatter(x=df.index, y=sma_50, mode='lines', name='SMA 50'))

    if sma_100 is not None:
        fig.add_trace(go.Scatter(x=df.index, y=sma_100, mode='lines', name='SMA 100'))

    if sma_150 is not None:
        fig.add_trace(go.Scatter(x=df.index, y=sma_150, mode='lines', name='SMA 150'))
    fig.update_layout(title='Stock Price with Multiple Moving Averages', xaxis_title='Date', yaxis_title='Price')
    return fig
def find_support_resistance(data, window=20):
    support_levels = []
    resistance_levels = []
    minima = data.rolling(window=window, min_periods=1).min()
    maxima = data.rolling(window=window, min_periods=1).max()

    for i in range(window, len(data) - window):
        if data[i] <= minima[i] and data[i - 1] > minima[i - 1]:
            support_levels.append((i, minima[i]))
        elif data[i] >= maxima[i] and data[i - 1] < maxima[i - 1]:
            resistance_levels.append((i, maxima[i]))

    return support_levels, resistance_levels

def plot_support_resistance(df, support_levels, resistance_levels):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Stock Price'))
    for level in support_levels:
        fig.add_trace(go.Scatter(x=[df.index[level[0]]], y=[level[1]], mode='markers', marker=dict(color='green'), showlegend=False))

    for level in resistance_levels:
        fig.add_trace(go.Scatter(x=[df.index[level[0]]], y=[level[1]], mode='markers', marker=dict(color='red'), showlegend=False))

    fig.update_layout(title='Stock Price with Support and Resistance Levels', xaxis_title='Date', yaxis_title='Price')

    return fig

def plot_volume_analysis(df):

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.index, y=df['volume'], name='Volume'))

    fig.update_layout(title='Volume Analysis', xaxis_title='Date', yaxis_title='Volume')
    return fig

def plot_fibonacci_retracement(df, high, low):
    fibonacci_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    levels = [low + (ratio * (high - low)) for ratio in fibonacci_levels]

    fig = go.Figure()


    fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Stock Price'))
    colors = ['gray', 'green', 'blue', 'purple', 'orange', 'red', 'black']

    for level, color in zip(levels, colors):
        fig.add_trace(go.Scatter(x=df.index, y=[level] * len(df.index), mode='lines', line=dict(color=color, width=1, dash='dash'), name=f'Fibonacci {level:.3f}'))

    fig.update_layout(title='Fibonacci Retracement Levels', xaxis_title='Date', yaxis_title='Price')

    return fig



