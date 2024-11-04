# stockapp/graph_generator.py
import pandas as pd
import plotly.express as px
from yahoo_fin.stock_info import get_data

def gettingdata(symbol):
    data = get_data(symbol,interval='1wk')
    return data

def preprocess(data):
    data=data.reset_index()
    data=data.rename(columns={'index':'Date','close':'price'})
    traindata=data.loc[:,['Date','price']]
    if traindata['Date'].dtype==object:
        traindata['Date']=pd.to_datetime(traindata['Date'])
    traindata.dropna(axis=0, inplace=True)
    return traindata


def graph(traindata):
    fig = px.line(traindata,x='Date',y='price')
    return fig

def describe(data):
    return data.describe()

def generate_graph(traindata,start_date,end_date):
    filtered_data=traindata[(traindata['Date']>=start_date) & (traindata['Date']<=end_date)]
    fig=px.line(filtered_data,x='Date',y='price')
    return fig