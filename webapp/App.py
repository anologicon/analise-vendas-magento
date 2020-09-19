import pandas as pd
import numpy as np
import io
from io import BytesIO, StringIO
import streamlit as st
from VizSerie import VizSerie
from Model import Model

st.beta_set_page_config(
    page_title="Magento 1 - Analise de relatório de vendas")

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
    try:
        data_viz.plotTrand()
    except:
        st.info("Não a dados suficientes para gerar uma tendência, 20 dias")

def main():

    st.set_option('deprecation.showfileUploaderEncoding', False)

    """
    # Analise de vendas - Magento 1

    Para começar, na página de relatório de vendas, escolha a opção diária, com o status *Fechado*,
    exporte o resultado em formato CSV, e envie aqui.
    """

    file = st.file_uploader("Enviar relatório", type=["csv"])

    show_file = st.empty()

    if not file:
        show_file.info("Precisamos do seu relatório de vendas em formato CSV para começar : " + ", ".join(["csv"]))
        
        st.stop()

    content = file.getvalue()

    if isinstance(file, BytesIO):
        show_file.image(file)
    else:
        try:
            data = pd.read_csv(file, usecols=['Pedidos','Período'],  parse_dates=['Período'])
        except:
            st.error("Erro ao ler o arquivo CSV")

            st.stop()

    file.close()
    
    data = data.iloc[:-1]

    data['Período'] = pd.to_datetime(data['Período'], format='%d/%m/%Y')

    data = data.set_index('Período')
    
    try:
        all_days = pd.date_range(data.index.min(), data.index.max(), freq='D')
    except:
        st.error("Erro ao selecionar inicio e fim do relatório. Verifique o arquivo.")

        st.stop()

    data = data.reindex(all_days, fill_value=0)

    viz(data)
    
    """
    ## Projeção de vendas
    """
    try:
        with st.spinner('Gerando predição'):
            periodo = st.slider('Dias de projeção', value=50, max_value=150)
            md = Model(data)
            md.predict(periodo)
            md.viz()
    except:
        st.error("Erro ao gerar projeção")
    
if __name__ == "__main__":
    main()