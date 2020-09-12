import pandas as pd
import numpy as np
import io
from io import BytesIO, StringIO
import streamlit as st
from VizSerie import VizSerie

def viz(data):

    data['Período'] = pd.to_datetime(data['Período'], format='%Y-%m-%d')

    df = data.set_index('Período')

    data_viz = VizSerie(df)

    """
    ## Como estão minhas vendas ao longo do tempo?
    
    *Você pode utilizar os filtros abaixo para vizualizar do tempo determinado até o atual*
    """
    data_viz.simplePlotSeries()

    """
    ## Vendas em diferentes series temporais 
    """
    data_viz.plotSubSales()

    """
    ## Qual a minha média de vendas nos dias da semana?    
    """
    data_viz.plotSalesByWeekDays()

    """
    ## Como está minhas vendas: Semana X Fim de semana?    
    """
    data_viz.plotSalesWeekWeekend()

    """
    ## Como esta minha têndencia?
    """
    data_viz.plotTrand()

    """
    ## Eu tenho sasionalidade?
    """
    data_viz.plotSeasionality()

def main():

    st.set_option('deprecation.showfileUploaderEncoding', False)

    """
    # Analise de vendas - Magento 1

    Para começar, na pagina de relaório de vendas, escolha a opção diaria, com o status *Fechado*,
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

    viz(data)

if __name__ == "__main__":
    main()