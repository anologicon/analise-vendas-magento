import matplotlib as plt
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose
import holidays
br_holidays = holidays.Brazil()

class VizSerie:

    def __init__(self, df):
        self.df = df

    def simplePlotSeries(self):

        df = self.df.copy()

        df['date'] = df.index.date

        df['feriado'] = df['date'].apply(lambda x: x in br_holidays)
        
        df['DiaDaSemana'] = df.index.dayofweek

        df['fimDeSemana'] = df['DiaDaSemana'].apply(lambda x: x == 5 or x == 6)

        dfDiaSemana = df[(df['fimDeSemana'] == 0) & (df['feriado'] == 0)]

        trace1 = go.Scatter(x=dfDiaSemana.index, y=dfDiaSemana['y'], mode='markers', name="Dia da semana")

        dfFeriados = df[(df['fimDeSemana'] == 0) & (df['feriado'] == 1)]

        trace2 = go.Scatter(x=dfFeriados.index, y=dfFeriados['y'], mode='markers', name="Feriado")

        dfFimDeSemana = df[(df['fimDeSemana'] == 1) & (df['feriado'] == 0)]

        trace3 = go.Scatter(x=dfFimDeSemana.index, y=dfFimDeSemana['y'], mode='markers', name="Fim de semana")

        data = [trace1, trace2, trace3]

        layout = go.Layout(yaxis={'title':'Quantidade de pedidos'},
                    xaxis={'title':'Tempo'})

        fig = go.Figure(data=data, layout=layout)

        fig.update_xaxes(rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="Último 1 mês", step="month", stepmode="backward"),
                dict(count=6, label="Últimos 6 meses", step="month", stepmode="backward"),
                dict(count=1, label="Último 1 ano", step="year", stepmode="backward"),
                dict(count=1, label="Início do ano até aqui", step="year", stepmode="todate"),
                dict(step="all")
            ])
        ))

        st.plotly_chart(fig)

    def plotSalesByWeekDays(self):
        
        df = self.df.copy()

        dias = [
            'Segunda-feira',
            'Terça-feira',
            'Quarta-feira',
            'Quinta-Feira',
            'Sexta-feira',
            'Sábado',
            'Domingo'
        ]

        dfByWeek = df.copy()

        dfByWeek['DiaDaSemana'] = df.index.dayofweek

        dfByWeek['DiaDaSemana'] = dfByWeek['DiaDaSemana'].apply(lambda x: dias[x])

        dfGroupByWeek = dfByWeek.groupby(['DiaDaSemana'])['y'].mean().reset_index()

        dfGroupByWeekIndex = dfGroupByWeek.set_index('DiaDaSemana')

        dfGroupByWeekIndex = dfGroupByWeekIndex.reindex(dias)

        dfGroupByWeekIndex['y'] = dfGroupByWeekIndex['y'].apply(lambda x: round(x,0))

        trace1 = go.Bar(x = dfGroupByWeekIndex.index,
                y = dfGroupByWeekIndex['y'],
                name = 'Média de pedidos / dia da semana')     

        dfMaxGroupByWeek = dfGroupByWeekIndex.groupby(['DiaDaSemana'])['y'].max().reset_index()

        dfMaxGroupByWeek = dfMaxGroupByWeek.set_index('DiaDaSemana')

        dfMaxGroupByWeek = dfMaxGroupByWeek.reindex(dias)

        trace2 = go.Scatter(x=dfMaxGroupByWeek.index, 
                    y=dfMaxGroupByWeek['y'],
                    name = 'Médias de vendas em linha', line = {'color': '#341f97','dash': 'dot'})

        data = [trace1, trace2]

        layout = go.Layout(yaxis={'title':'Quantidade de pedidos'},
                    xaxis={'title':'Dias da semana'}, width=800)

        fig = go.Figure(data=data, layout=layout)

        maxDiaSemana = dfGroupByWeekIndex.idxmax(axis = 0)[0]

        maxPedidos = round(dfGroupByWeekIndex['y'].max(), 3)

        st.write("Parece que **"+maxDiaSemana+"** tem a melhor média de vendas, com **"+str(maxPedidos)+"** pedidos.")

        st.plotly_chart(fig)

    def plotSalesWeekEspecialsDays(self):

        df = self.df.copy()

        dfSetWeekend = df.copy()

        dfSetWeekend['DiaDaSemana'] = df.index.dayofweek

        dfSetWeekend['FimDeSemana'] = dfSetWeekend['DiaDaSemana'].apply(lambda x: x == 5 or x == 6)

        trace1 = go.Box(y = dfSetWeekend.loc[dfSetWeekend['FimDeSemana'] == 1, 'y'], 
                    name='Fim de semana',marker = {'color': '#ff2256'})

        trace2 = go.Box(y = dfSetWeekend.loc[dfSetWeekend['FimDeSemana'] == 0, 'y'], 
                    name='Semana',marker = {'color': '#2289ff'})

        dfSetWeekend['date'] = dfSetWeekend.index

        dfSetWeekend['Feriado'] = dfSetWeekend['date'].apply(lambda x: x in br_holidays)

        trace3 = go.Box(y = dfSetWeekend.loc[dfSetWeekend['Feriado'] == 1, 'y'], 
                    name='Feriado',marker = {'color': '#ffe522'})

        data = [trace1, trace2, trace3]
        
        layout = go.Layout(yaxis={'title':'Pedidos'},
                    xaxis={'title':'Dia da semana x Fim de semana'})

        fig = go.Figure(data=data, layout=layout)

        st.plotly_chart(fig)

    def plotSubSales(self):

        df = self.df.copy()

        # Daily Mean
        daily = df.resample('D').mean()
        # Weekly Mean
        Weekly = df.resample('W').mean()
        # Monthly Mean
        month = df.resample('M').mean()
        # Year Mean
        yearly = df.resample('Y').mean()

        fig = make_subplots(rows=4)

        fig.add_scatter(x=daily.index, 
                    y=daily['y'].apply(lambda x: round(x,0)),
                    name = 'Vendas Diarias', mode="lines",row=1,col=1)

        fig.add_scatter(x=Weekly.index, 
                    y=Weekly['y'].apply(lambda x: round(x,0)),
                    name = 'Vendas Semanais', mode="lines",row=2,col=1)

        fig.add_scatter(x=month.index, 
                    y=month['y'].apply(lambda x: round(x,0)),
                    name = 'Vendas Mensais', mode="lines",row=3,col=1)
        
        fig.add_scatter(x=yearly.index, 
                    y=yearly['y'].apply(lambda x: round(x,0)),
                    name = 'Vendas Anuais', mode="lines",row=4,col=1)
                
        fig.update_layout(height=800, width=800)

        st.plotly_chart(fig)

    def plotTrand(self):

        df = self.df.copy()

        decomposition = seasonal_decompose(df)

        dft = pd.DataFrame({'index':df.index, 'trend': decomposition.trend})

        dft['trend'] = dft['trend'].apply(lambda x: round(x, 0))

        trace1 = go.Scatter(x=df.index, 
                y=dft.trend,
                name = 'Tendência', mode="lines", marker={'color': '#ff322b'})

        trace2 = go.Scatter(x=df.index, 
                y=df['y'],
                name = 'Pedidos', mode="markers", marker={'color': '#3d2bff'})

        data = [trace2, trace1]

        layout = go.Layout(yaxis={'title':'Quantidade de pedidos'},
                    xaxis={'title':'Data'},  width=800)

        fig = go.Figure(data=data, layout=layout)

        dft['index'] = pd.to_datetime(dft['index'])

        dfw = dft.resample('m').sum()

        dfpct = dfw.pct_change()
        
        dfpct['trend_format'] = dfpct['trend'].map(lambda n: '{:,.2%}'.format(n))

        ultimoTrand = dfpct[-1:]['trend'][0]
        ultimoTrandFormat = dfpct[-1:]['trend_format'][0]

        message = "um aumento"

        if ultimoTrand < 0:
            message = "uma queda"

        st.write("Parece que  a tendência teve **"+message+"** de **"+str(ultimoTrandFormat)+"** comparado com o último mês.")

        st.plotly_chart(fig)
    
    def plotMonthWeekSales(self):

        dfWeekMonth = self.df.copy()

        dfWeekMonth['year'] = dfWeekMonth.index.year
        dfWeekMonth['month'] = dfWeekMonth.index.month
        dfWeekMonth['week'] = dfWeekMonth.index.week

        dfgp = dfWeekMonth.groupby(['year','month','week']).mean().reset_index()

        dfgp['weekMonth'] = dfgp.groupby(['year','month']).cumcount()+1

        dfWeekMonthSelected = dfSemanaMesa = dfgp[['y','weekMonth']]

        dfWeekMonthgp = dfWeekMonthSelected.groupby('weekMonth')['y'].mean().reset_index()

        trace1 = go.Bar(x = dfWeekMonthgp['weekMonth'],
            y = dfWeekMonthgp['y'],
            name = 'Média de pedidos / semana do mẽs')

        data = [trace1]

        layout = go.Layout(yaxis={'title':'Quantidade média de pedidos'},
                    xaxis={'title':'Semana do mês'})

        fig = go.Figure(data=data, layout=layout)

        st.plotly_chart(fig)