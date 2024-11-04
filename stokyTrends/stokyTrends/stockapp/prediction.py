import pandas as pd
import numpy as np
from yahoo_fin.stock_info import get_data
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import load_model
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
# load model
savedModel=load_model("lstm_model.h5")
def get_the_data(symbol):
    df =get_data(symbol, start_date='2023-01-01')
    return df
scaler = MinMaxScaler(feature_range=(0,1))
def predictt(df):
    data = df.filter(['close'])
    dataset = data.values
    scaled_data = scaler.fit_transform(dataset)
    test_data = scaled_data[:]
    x_test = []
    y_test = dataset[60:,:]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))
    x_test.shape,y_test.shape
    predictions = savedModel.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
    return predictions,y_test,scaled_data
def predicted_price(scaled_data):
    last_60_days = scaled_data[-60:]
    input_data = np.array(last_60_days).reshape(1, -1, 1)
    predicted_scaled_price = savedModel.predict(input_data)
    predicted_price = scaler.inverse_transform(predicted_scaled_price)
    return predicted_price[0][0]
def predicted_graph(df,predictions,y_test):
    dates = df.index[-len(y_test):]
    trace_actual = go.Scatter(x=dates, y=y_test.flatten(), mode='lines', name='Actual Stock Price', line=dict(color='blue'))
    trace_predicted = go.Scatter(x=dates, y=predictions.flatten(), mode='lines', name='Predicted Stock Price', line=dict(color='red'))
    layout = go.Layout(xaxis=dict(title='Date'), yaxis=dict(title='Stock Price'))
    fig = go.Figure(data=[trace_actual, trace_predicted], layout=layout)
    return fig
