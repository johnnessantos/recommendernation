import os
import pickle
import bz2

import numpy as np
import pandas as pd

from fonte_dados import FonteDados

class Utils:
    def __init__(self):
        """
        Classe responsavel por conter metodos que podem ser executados por qualquer arquivo python
        """
        self.dicionario_variaveis = None
        self.fonte_dados = FonteDados()


    def descrever_variavel(self, variavel=None):
        """
        Função com intenção de obter a descrição de uma coluna especifica dos dados fonte.
        Parâmetros:
        ----------
            variavel: String
        """
        if self.dicionario_variaveis is None:
            self.dicionario_variaveis = self.fonte_dados.carregar_dicionario_dados()

        
        if variavel:
            variavel_descricao = self.dicionario_variaveis[self.dicionario_variaveis.feature == variavel].values
            if variavel_descricao.size > 0:
                return (tuple(variavel_descricao[0]))
            else:
                return ((variavel, 'Variável não encontrada no dicionário'))

    def descrever_dataframe(self, df):
        """
        Função geradora de uma descrição de informações do dataframe, como: colunas, tipos das colunas,
        quantidade de nulos, percentual de nulos.
        Parâmetros:
        ----------
            df: DataFrame
        Retornos:
        --------
            df_novo: DataFrame
        """
        df_novo = pd.DataFrame({
            'coluna': df.columns.values,
            'tipo': df.dtypes.values,
            'quantidade_nulos': df.isna().sum().values
        })
        df_novo['porcentagem_nulos'] = df_novo['quantidade_nulos']/df.shape[0]

        return df_novo


    def salvar_pickle(self, obj, caminho):
        """
        Salvar objeto compresso utilizando pickle
        Parâmetros:
        ----------
            obj: Object
                Objeto a serializar no disco.
            caminho: String
                Caminho do arquivo
        """
        with bz2.BZ2File(caminho, 'wb') as f:
            pickle.dump(obj, f)
        
        #with open(caminho, 'wb') as f:
        #   pickle.dump(obj, f)

    def ler_pickle(self, caminho, compresso=True):
        """
        Carregar objeto compresso utilizando pickle
        Parâmetros:
        ----------
            caminho: String
                Caminho do arquivo
        Retornos:
        --------
            obj: Object
                Objeto deserializado.
        """
        with bz2.BZ2File(caminho, 'rb') as f:
            return pickle.load(f)
