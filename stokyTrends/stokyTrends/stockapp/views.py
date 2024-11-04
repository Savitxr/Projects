from django.shortcuts import render
from . import graph_generator,prediction,analysis
from yahoo_fin.stock_info import get_data
def graph_view(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        data = graph_generator.gettingdata(symbol)
        traindata = graph_generator.preprocess(data)
        current_price=traindata['price'].tail(1)
        current_price="%.2f" % round(current_price,2)
        fig = graph_generator.graph(traindata)
        graph_html = fig.to_html(full_html=False)
        description = graph_generator.describe(data)
        description_html = description.to_html()
        context = {'graph_html': graph_html, 'symbol': symbol, 'description_html': description_html, 'current_price':current_price}
        return render(request, 'trends.html', context)
    return render(request, 'trends.html')
def Analysis(request):
    if request.method=='POST':
        symbol=request.POST['symbol']
        df=get_data(symbol,start_date='2023-01-01')
        sma_50 = analysis.calculate_sma(df['close'], window=50)
        sma_100 = analysis.calculate_sma(df['close'], window=100)
        sma_150 = analysis.calculate_sma(df['close'], window=150)
        moving_averages_fig=analysis.plot_stock_with_multiple_moving_averages(df, sma_50=sma_50, sma_100=sma_100, sma_150=sma_150)

        support_levels, resistance_levels = analysis.find_support_resistance(df['close'])
        support_resistance_fig=analysis.plot_support_resistance(df, support_levels, resistance_levels)

        volume_fig=analysis.plot_volume_analysis(df)

        fibonacci_fig=analysis.plot_fibonacci_retracement(df, high=df['close'].max(), low=df['close'].min())


        moving_averages_graph=moving_averages_fig.to_html(full_html=False)
        support_resistance_graph=support_resistance_fig.to_html(full_html=False)
        volume_graph=volume_fig.to_html(full_html=False)
        fibonacci_graph=fibonacci_fig.to_html(full_html=False)
        context= {'Moving_Averages_Graph':moving_averages_graph,'support_resistance_graph':support_resistance_graph,'volume_graph':volume_graph,'fibonacci_graph':fibonacci_graph,'symbol':symbol}
        return render(request,'analysis.html',context)
    return render(request,'analysis.html')

def stock_prediction(request):
    if request.method=='POST':
        symbol=request.POST['symbol']
        data = prediction.get_the_data(symbol)
        predictions = prediction.predictt(data)[0]
        y_test=prediction.predictt(data)[1]
        scaled_data=prediction.predictt(data)[2]
        prediction_fig= prediction.predicted_graph(data,predictions,y_test)
        predictedd_price=prediction.predicted_price(scaled_data)
        prediction_fig_html=prediction_fig.to_html(full_html=False)
        context = {'prediction_fig_html': prediction_fig_html,'predicted_price':predictedd_price,'symbol':symbol}
        return render(request, 'prediction.html', context)
    return render(request,'prediction.html')


