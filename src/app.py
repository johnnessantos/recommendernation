import os
from datetime import datetime
import base64

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from fonte_dados import FonteDados
from utils import Utils

# https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/app.py

ARQUIVO_DADOS_PROCESSADOS = 'dados_processados.pkl'
ARQUIVO_MODELO = 'modelo.pkl'

@st.cache
def carregar_dados():
    fonte_dados = FonteDados()
    return fonte_dados.carregar_dados()

@st.cache
def carregar_dados_processados():
    utils = Utils()
    fonte_dados = FonteDados()
    return utils.ler_pickle(os.path.join(fonte_dados.diretorio_saida, ARQUIVO_DADOS_PROCESSADOS))

@st.cache(allow_output_mutation=True)
def carregar_modelo():
    fonte_dados = FonteDados()
    with open(os.path.join(fonte_dados.diretorio_saida, ARQUIVO_MODELO), 'rb') as f:
        return Utils().ler_pickle(f)

def bar_plot(x, y, titulo, x_titulo, y_titulo):
    return go.Figure(
        data = go.Bar(x = x, y = y)
    ).update_layout(
        autosize=True,
        width=800,
        height=500,
        
        xaxis = dict(
            title_text=x_titulo,
            titlefont = dict(size=14),
        ),
        yaxis = dict(
            title_text=y_titulo,
            titlefont = dict(size=14),
        ),
        title = dict(
            text = titulo,
            font = dict(size=18),
            y = 0.9,
            x = 0.5,
            xanchor = 'center',
            yanchor = 'top'
        )
    )

def baixar_recomendacoes(rec):
    df = pd.DataFrame(rec, columns=['id'])
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="recomendacoes.csv">Baixar recomendação</a>'

def menu_lateral(st):
    st.sidebar.title('Selecione uma opção:')

    acao = st.sidebar.selectbox('Ações disponíveis', ['Selecione','Análise do mercado', 'Sistema de recomendação'])

    if acao == 'Sistema de recomendação':
        manter_empresas = st.sidebar.checkbox("Manter as empresas do seu portifolio", False)
    else:
        manter_empresas = None

    st.sidebar.subheader('Código fonte')
    st.sidebar.info('''As tecnologias utilizadas na solução são python 3+, sklearn, pandas, numpy e streamlit, 
    podendo ser acessado em [codigo fonte](https://github.com/johnnessantos/codenation/) ''')

    st.sidebar.subheader('Autor')
    st.sidebar.info('Johnnes Santos')

    return dict(acao=acao, manter_empresas=manter_empresas)
    
def analisar_mercado(st):
    st.subheader('Analise do mercado')

    # Grafico de barras para contar empresas por estado
    empresas_por_uf = dados.sg_uf.value_counts()
    st.plotly_chart(bar_plot(empresas_por_uf.index, 
                            empresas_por_uf.values, 
                            'Quantidade de empresas por estado',
                            'Estados',
                            'Quantidade de empresas'))
    
    st.write('O mercado de empresas conta com segmentação das empresas como demonstra a figura abaixo: ')

    # Grafica de barras para contar empresas por setor
    empresas_por_setor = dados.setor.value_counts()
    st.plotly_chart(bar_plot(empresas_por_setor.index, 
                            empresas_por_setor.values, 
                            'Quantidade de empresas por setor',
                            'Setores',
                            'Quantidade de empresas'))

    # Grafico de barras para contagem de empresas por idade categorica
    empresas_por_idade = dados.idade_emp_cat.value_counts()
    st.plotly_chart(bar_plot(empresas_por_idade.index, 
                            empresas_por_idade.values/1000, 
                            'Quantidade de empresas por idade',
                            'Idade',
                            'Quantidade de empresas'))



def recomendador(st, manter_empresas):
    fonte_dados = FonteDados()
    # Modelo treinado
    modelo = carregar_modelo()
    
    st.subheader('Passo 1:')
    st.write('''O sistema de recomendação se basea nas empresas mais semelhantes as que já estão no 
                teu portifolio carregue seus dados abaixo:''')
    updaload_arquivo = st.file_uploader("Selecione seu arquivo .csv", type="csv")
    if updaload_arquivo is not None:
        portifolio = pd.read_csv(updaload_arquivo)
        
        st.subheader('Passo 2:')
        st.write('''Deseja realizar analise sobre o seu portifolio?''')

        opcao = st.selectbox('O que deseja fazer com o seu portifolio?', 
            ['Selecione','Análise sobre o seu portifolio', 'Realizar recomendação de leads'])

        if opcao == 'Análise sobre o seu portifolio':
            analisar_mercado(st)
        elif opcao == 'Realizar recomendação de leads':
            dados_processados = carregar_dados_processados()
            portifolio = fonte_dados.gerar_portifolio(dados_processados, portifolio.id.values)
            rec = modelo.recomendar(portifolio.drop(columns=['id']))
            
            # Removendo as empresas que ele já tem no portifolio
            if not manter_empresas:
                rec = list(set(rec).difference(portifolio.index.values))

            st.success(f'Número de empresas recomendadas: {len(rec)}')
            
            rec_empresas = dados[dados.index.isin(rec)]
            st.write(rec_empresas[['id', 'setor', 'idade_empresa_anos']].head())
            st.markdown(baixar_recomendacoes(rec_empresas.id.values), unsafe_allow_html=True)
            
            
            #map_data = pd.DataFrame(
            #    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            #    columns=['lat', 'lon'])
            #st.map(map_data)
            

    if updaload_arquivo is not None and opcao != 'Selecione':
        st.subheader('Passo 3:')
        st.write('Nos avalie: De 0 a 10 o quanto a solução foi útil para você?')
        avaliacao = st.slider('Ajuda: A nota 0 significa inútil e 10 sendo extremamente útil', 0, 10, 0)
        if st.button('Avaliar'):
            st.success('Obrigado por nos avaliar!')
            
            with open(os.path.join(fonte_dados.diretorio_saida, 'avaliacoes.txt'), 'a') as f:
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                f.write(f'{data_hora}, {avaliacao}')


# Inicio da aplicação
st.title('RecommenderNation')
st.subheader('Sistema de recomendação de leads que conta com mais de 400 mil empresas.')

dados = carregar_dados()

# Fluxo de seleção
opcoes_menu = menu_lateral(st)
acao = opcoes_menu.get('acao')
if acao == 'Análise do mercado':
    analisar_mercado(st)
elif acao == 'Sistema de recomendação':
    manter_empresas = opcoes_menu.get('manter_empresas')
    recomendador(st, manter_empresas)
    
