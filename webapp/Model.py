from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import pandas as pd
import streamlit as st
import holidays
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objects as go
br_holidays = holidays.Brazil()

class Model:

    def __init__(self, df):
        self.df = df

    def viz(self):

        dfs = self.dfs

        df = self.df

        trace1 = go.Scatter(x=dfs.index, 
                y=dfs.pedidos,
                name = 'Predição', mode="lines", marker={'color': '#ff322b'})

        trace2 = go.Scatter(x=df.index, 
                y=df['Pedidos'],
                name = 'Atual', mode="lines", marker={'color': '#3d2bff'})

        yhat_lower = go.Scatter(
            x = dfs.index,
            y = dfs['pedidos_lower'],
            marker = {
                'color': 'rgba(0, 0, 0, 0)'
            },
            showlegend = False,
            hoverinfo = 'none',
        )

        yhat_upper = go.Scatter(
            x = dfs.index,
            y = dfs['pedidos_max'],
            fill='tonexty',
            fillcolor = 'rgba(255, 127, 14, 0.3)',
            name = 'Confiança',
            hoverinfo = 'none',
            mode = 'none'
        )

        data = [trace2, trace1, yhat_lower, yhat_upper]

        layout = go.Layout(yaxis={'title':'Quantidade de pedidos'},
                    xaxis={'title':'Data'}, height=600, width=800)

        fig = go.Figure(data=data, layout=layout)

        st.plotly_chart(fig)

    def predict(self, periods):
        df = self.df

        series = pd.DataFrame({'ds': df.index,'y':df['Pedidos']})

        series['y'] = series['y'].fillna(0)

        holidays = pd.DataFrame({
            'holiday': 'feriados',
            'ds': br_holidays,
            'lower_window': 0,
            'upper_window': 1,
        })
        
        m = Prophet(holidays=holidays, growth='linear')

        m.fit(series)

        future = m.make_future_dataframe(periods=periods, freq='D')

        forecast = m.predict(future)

        forecast['yhat'] = forecast['yhat'].apply(lambda x: round(x, 0))
        forecast['yhat_upper'] = forecast['yhat_upper'].apply(lambda x: round(x, 0))
        forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x: round(x, 0))

        decomposition = seasonal_decompose(df)

        dfs = pd.DataFrame({'index': forecast['ds'], 'pedidos': forecast['yhat'],
            'pedidos_max': forecast['yhat_upper'], 'pedidos_lower':forecast['yhat_lower']})

        dfs['index'] = pd.to_datetime(dfs['index'])

        dfs = dfs.set_index('index')
        
        self.dfs = dfs