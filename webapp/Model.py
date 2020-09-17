from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import pandas as pd
import streamlit as st
import holidays
br_holidays = holidays.Brazil()

class Model:

    def __init__(self, df):
        self.df = df

    def predict(self):
        df = self.df

        series = pd.DataFrame({'ds': df.index,'y':df['Pedidos']})

        series['y'] = series['y'].fillna(0)

        holidays = pd.DataFrame({
            'holiday': 'feriados',
            'ds': br_holidays,
            'lower_window': 0,
            'upper_window': 1,
        })
        
        m = Prophet(holidays=holidays, daily_seasonality=True)

        m.fit(series)

        future = m.make_future_dataframe(periods=30)

        forecast = m.predict(future)

        st.plotly_chart(plot_plotly(m, forecast))
