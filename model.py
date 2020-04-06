import pandas as pd

import plotly.graph_objs as go
from plotly.offline import plot




df = pd.read_csv('./data/GOOG.csv')

def plotData():

    # Plot candlestick chart
    candle = go.Candlestick(
        x = df['Time'],
        open = df['Open'],
        close = df['Close'],
        high = df['High'],
        low = df['Low'],
        name = 'Candlesticks'
    )

    # Plotting moving averages 
    data = [candle]

    layout = go.Layout(title = 'No Name Yet')
    fig = go.Figure(data = data, layout = layout)

    plot(fig, filename='No-name.html')

plotData()