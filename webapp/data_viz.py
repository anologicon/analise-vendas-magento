import matplotlib as plt
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

def simplePlotSeries(df):
    data = [go.Scatter(x=df.index, y=df['Pedidos'])]

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

def plotSalesByWeekDays(df):
    
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

    dfGroupByWeek = dfByWeek.groupby(['DiaDaSemana'])['Pedidos'].mean().reset_index()

    dfGroupByWeekIndex = dfGroupByWeek.set_index('DiaDaSemana')

    dfGroupByWeekIndex = dfGroupByWeekIndex.reindex(dias)

    trace1 = go.Bar(x = dfGroupByWeekIndex.index,
               y = dfGroupByWeekIndex['Pedidos'],
               name = 'Média de pedidos / dia da semana')     

    dfMaxGroupByWeek = dfGroupByWeekIndex.groupby(['DiaDaSemana'])['Pedidos'].max().reset_index()

    dfMaxGroupByWeek = dfMaxGroupByWeek.set_index('DiaDaSemana')

    dfMaxGroupByWeek = dfMaxGroupByWeek.reindex(dias)

    trace2 = go.Scatter(x=dfMaxGroupByWeek.index, 
                y=dfMaxGroupByWeek['Pedidos'],
                name = 'Médias de vendas em linha', line = {'color': '#341f97','dash': 'dot'})

    data = [trace1, trace2]

    layout = go.Layout(yaxis={'title':'Quantidade de pedidos'},
                xaxis={'title':'Dias da semana'})

    fig = go.Figure(data=data, layout=layout)

    st.plotly_chart(fig)

    maxDiaSemana = dfGroupByWeekIndex.idxmax(axis = 0)[0]

    maxPedidos = round(dfGroupByWeekIndex['Pedidos'].max(), 3)

    st.write("Parece que **"+maxDiaSemana+"** tem a melhor média de vendas, com **"+str(maxPedidos)+"** pedidos.")

def plotSalesWeekWeekend(df):
    dfSetWeekend = df.copy()

    dfSetWeekend['DiaDaSemana'] = df.index.dayofweek

    dfSetWeekend['FimDeSemana'] = dfSetWeekend['DiaDaSemana'].apply(lambda x: x == 5 or x == 6)

    trace1 = go.Box(y = dfSetWeekend.loc[dfSetWeekend['FimDeSemana'] == 1, 'Pedidos'], 
                name='Fim de semana',marker = {'color': '#488f31'})


    trace2 = go.Box(y = dfSetWeekend.loc[dfSetWeekend['FimDeSemana'] == 0, 'Pedidos'], 
                name='Semana',marker = {'color': '#89b050'})

    data = [trace1, trace2]
    
    layout = go.Layout(yaxis={'title':'Pedidos'},
                xaxis={'title':'Dia da semana x Fim de semana'})

    fig = go.Figure(data=data, layout=layout)

    st.plotly_chart(fig)

def plotSubSales(df):
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
                y=daily['Pedidos'],
                name = 'Vendas Diarias', mode="lines",row=1,col=1)

    fig.add_scatter(x=Weekly.index, 
                y=Weekly['Pedidos'],
                name = 'Vendas Semanais', mode="lines",row=2,col=1)

    fig.add_scatter(x=month.index, 
                y=month['Pedidos'],
                name = 'Vendas Mensais', mode="lines",row=3,col=1)
    
    fig.add_scatter(x=yearly.index, 
                y=yearly['Pedidos'],
                name = 'Vendas Anuais', mode="lines",row=4,col=1)

    st.plotly_chart(fig)

def plotTrand(df):

    decomposition = seasonal_decompose(df, model="additive")

    trace1 = go.Scatter(x=df.index, 
            y=decomposition.trend,
            name = 'Tendência', mode="lines")

    data = [trace1]

    layout = go.Layout(yaxis={'title':'Quantidade de pedidos'},
                xaxis={'title':'Data'})

    fig = go.Figure(data=data, layout=layout)

    st.plotly_chart(fig)