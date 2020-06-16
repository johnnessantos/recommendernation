import os
import sys

from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import davies_bouldin_score

class Metricas():
    def __init__(self):
        """
        Classe responsável pela metrica aplicada para se basear na escolha do método
        """

    def calcular_pontuacao(self, X, categorias, metrica='euclidean', tam_amostra=1000):
        """
        Metrica para calcula a silhueta do cluster com o método `silhouette`, `calinski_harabasz`
        e `davies_bouldin`.
        A metrica silhouette com distancia euclidiana o melhor valor é 1 e o pior é -1. Em caso
        onde o valor for 0 significa que os agrupametos estão sobrepostos.
        A metrica calinski_harabasz quanto maior mais denso e mais bem separados está o cluster.
        A metrica davies_bouldin quanto mais próximo de zero melhor, ele se baseia em similaridade
        entre agrupamentos se baseando na média das distancias do próprio agrupamento.
        Parâmetros:
        ----------
            X: List
                Resultado do cluster
            tam_amostra: List
                Resposta para os dados
        """

        return {
            f'silhouette_score_{metrica}': silhouette_score(X, categorias, 
                                            metric=metrica, sample_size=tam_amostra, random_state=42),
            'calinski_harabasz_score': calinski_harabasz_score(X, categorias),
            'davies_bouldin_score': davies_bouldin_score(X, categorias)
        }

    def pontuacao(self, y, rec):
        """
        Função responstável por calcular os acertos, que se basea em contar a quantidade de itens de `y` em `rec`.
        Parâmetros:
        ----------
            y: Array
                Indices das empresas do portifolio
            rec: Array
                Indices recomendadas
        """
        y_conjunto = set(y)
        r = y_conjunto.intersection(set(rec))
        
        return len(r)/len(y)