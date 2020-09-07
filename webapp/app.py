import pandas as pd
import numpy as np
import io
from io import BytesIO, StringIO
import streamlit as st
import data_viz


st.set_option('deprecation.showfileUploaderEncoding', False)

"""
# Analise de vendas - Magento 1

Para começar, na pagina de relaório de vendas, com o status *Fechado*,
salve o resultado em formato CSV, e envie aqui.
"""

def main():

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

    data['Período'] = pd.to_datetime(data['Período'], format='%Y-%m-%d')

    df = data.set_index('Período')

    """
    ## Como estão minhas vendas ao longo do tempo?
    
    *Você pode utilizar os filtros abaixo para vizualizar do tempo determinado até o atual*
    """
    data_viz.simplePlotSeries(df)

    """
    ## Vendas em diferentes series temporais 
    """
    data_viz.plotSubSales(df)

    """
    ## Qual a minha média de vendas nos dias da semana?    
    """
    data_viz.plotSalesByWeekDays(df)

    """
    ## Como está minhas vendas: Semana X Fim de semana?    
    """
    data_viz.plotSalesWeekWeekend(df)

main()