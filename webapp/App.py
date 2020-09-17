import pandas as pd
import numpy as np
import io
from io import BytesIO, StringIO
import streamlit as st
from VizSerie import VizSerie
from Model import Model

st.beta_set_page_config(
    page_title="Magento 1 - Analise de relatorio de vendas")

def viz(data):

    data_viz = VizSerie(data)

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
    ## Médias de vendas ao longo das semanas do mês?
    """
    data_viz.plotMonthWeekSales()

    """
    ## Fim de semana X Feriado X Dias da semana?    
    """
    data_viz.plotSalesWeekEspecialsDays()

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
        data = pd.read_csv(file, usecols=['Pedidos','Período'],  parse_dates=['Período'])

    file.close()
    
    data = data.iloc[:-1]

    data['Período'] = pd.to_datetime(data['Período'], format='%d/%m/%Y')

    data = data.set_index('Período')

    all_days = pd.date_range(data.index.min(), data.index.max(), freq='D')

    data = data.reindex(all_days, fill_value=0)

    viz(data)
    
    md = Model(data)

    """
    # Projeção de vendas
    """

    md.predict()

if __name__ == "__main__":
    main()