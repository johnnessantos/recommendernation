import os
import sys
import pickle
import bz2

import pandas as pd


class FonteDados():
    def __init__(self):
        """
        Classe responsavel pela leitura dos dados.
        
        """
        self.diretorio_raiz = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..')))
        self.diretorio_dados = os.path.join(self.diretorio_raiz, 'data')
        self.diretorio_saida = os.path.join(self.diretorio_raiz, 'output')

    def carregar_dados(self):
        """
        Carrega os dados de e os retorna em um DataFrame
        Parâmetros:
        ----------
            None
        Retornos:
        --------
            X: DataFrame
        """
        with bz2.BZ2File(os.path.join(self.diretorio_dados, 'dados.pkl'), 'rb') as f:
            return pickle.load(f)

        #return pd.read_csv(os.path.join(self.diretorio_dados, 'estaticos_market.csv'), index_col=0)

    def carregar_portifolio(self, portifolio=1):
        """
        Metodo para retornar o dataframe do portifolio de acordo com o numero
        Parâmetros:
        ----------
            portifolio: int (padrão 1)
        Retornos:
        --------
            X: DataFrame
        """

        return pd.read_csv(os.path.join(self.diretorio_dados, f'estaticos_portfolio{portifolio}.csv'), index_col=0)


    def carregar_dicionario_dados(self):
        """
        Metodo que carrega os dados do dicionario dos dados
        Parâmetros:
        ----------
            None
        Retornos:
        --------
            X: DataFrame
        """

        return pd.read_csv(os.path.join(self.diretorio_dados, 'features_dictionary.csv'), sep=';')

    def gerar_portifolio(self, dados_fonte, portifolio_ids):
        """
        Metodo responsável por gerar um portifolio realizando o join com os dados fonte `market`
        Parâmetros:
        ----------
            dados_fonte: DataFrame
                Dados de `market` que serão utilizados como fonte.
            portifolio_ids: DataFrame
                DataFrame com os `ids` das empresas.

        Retornos:
        --------
            df_novo: DataFrame
                DataFrame com os dodos de `dados_fonte` de acordo com os ids de `portifolio_ids`
        """
        return dados_fonte[dados_fonte.id.isin(portifolio_ids)].copy()


    def carregar_dados_localizacao(self):
        """
        Carrega dos dados de latitute e longitude por microrregião se baseando na média dos múnicipios
        que fazem parte da microrregião.
        Parâmetros:
        ----------
            None
        Retornos:
        --------
            df: DataFrame
                Dataframe com as microrregiões e sua latitude e longitude
        """
        return pd.read_csv(os.path.join(self.diretorio_saida, 'localizacao-microrregiao-brasil.csv'))
        