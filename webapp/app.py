import pandas as pd
import numpy as np
import io
from io import BytesIO, StringIO
import streamlit as st
import matplotlib as plt
import plotly.graph_objects as go

st.set_option('deprecation.showfileUploaderEncoding', False)


def main():
    st.header('Analise de vendas - Magento 1')

    """
    # Analise de vendas - Magento 1
    

    Para começar, na pagina de relaório de vendas, com o status *Fechado*,
    salve o resultado em formato CSV, e envie aqui.
    """

    file = st.file_uploader("Enviar relatório", type=["csv"])

    show_file = st.empty()

    if not file:
        show_file.info("Precisamos do seu relatório de vendas em formato CSV para começar : " + ", ".join(["csv"]))
        return

    content = file.getvalue()

    if isinstance(file, BytesIO):
        show_file.image(file)
    else:
        data = pd.read_csv(file)

    file.close()

    df = data.set_index('Período')

    data = [go.Scatter(x=df.index, y=df['Pedidos'])]

    layout = go.Layout(title='Vendas ao longo do tempo',
                   yaxis={'title':'Quantidade de pedidos'},
                   xaxis={'title':'Data'})

    fig = go.Figure(data=data, layout=layout)

    fig.update_xaxes(rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    ))

    st.plotly_chart(fig)

main()