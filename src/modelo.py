import os

import numpy as np

from sklearn.neighbors import NearestNeighbors

class Modelo():
    def __init__(self):
        """
        Classe responsável pela lógica para a realizaçao de recomendação de novas empresas
        """
        self.recomendador = None

    def recomendar(self, portifolio):
        """
        Função responsável pela recomendação de leads mais aderetentes de acordo com o portifolio
        Parâmetros:
        ----------
            portifolio: Array ou list
                Ids das empresas do portifolio
        Retornos:
        --------
            x_indices: Array
                indices das empresas recomendadas
        """
        indices = self.recomendador.kneighbors(portifolio, return_distance=False)
        return np.unique(indices[:, np.arange(1, self.n_neighbors)].reshape(1, -1))

    def treinar(self, X):
        """
        Metodo responsável por treinar o algoritmo de recomendacao
        Parâmetros:
        ----------
            X: DataFrame
                Dados processados
        Retornos:
        --------
            None
        """
        self.n_neighbors = 20
        self.recomendador = NearestNeighbors(n_neighbors=self.n_neighbors, algorithm='auto').fit(X)
        return self
