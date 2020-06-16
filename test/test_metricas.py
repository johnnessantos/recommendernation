import os
import sys

import numpy as np
import pandas as pd
import pytest

# Adicionando o diretorio raiz no ambiente para possibilitar realizar importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'src')))

from src.utils import Utils
from src.metricas import Metricas

class TestMetricas():
    @pytest.fixture(scope='module')
    def instancia_metricas(self):
        return Metricas()

    def test_pontuacao_100_porcento(self, instancia_metricas):
        a = np.arange(100000)
        b = np.arange(100000)
        assert instancia_metricas.pontuacao(a,b) == 1.0

    def test_calcular_pontuacao(self, instancia_metricas):
        X  = [[ 0.6749994 ,  0.32689971,  1.15461469,  5.19933758, -5.19933758,
            -5.19933758, -5.19933758, -5.19933758, -5.19933758,  5.19933758,
            5.19933758,  5.19933758, -5.19933758,  2.15550892,  1.26806948,
            -5.19933758, -5.19933758,  5.19933758, -5.19933758, -5.19933758,
            -5.19933758, -5.19933758, -5.19933758,  5.19933758, -5.19933758,
            -5.19933758, -5.19933758, -5.19933758],
        [-1.0663039 , -1.6252744 , -0.21363612,  5.19933758, -5.19933758,
            -5.19933758,  5.19933758, -5.19933758, -5.19933758,  5.19933758,
            5.19933758,  5.19933758, -5.19933758,  0.06528392, -0.00627288,
            -5.19933758, -5.19933758, -5.19933758, -5.19933758, -5.19933758,
            5.19933758, -5.19933758, -5.19933758, -5.19933758, -5.19933758,
            -5.19933758,  5.19933758, -5.19933758],
        [ 0.05246503, -0.83689206, -0.21363612,  5.19933758, -5.19933758,
            -5.19933758,  5.19933758, -5.19933758, -5.19933758, -5.19933758,
            5.19933758,  5.19933758, -5.19933758, -1.23127984, -1.25298763,
            -5.19933758, -5.19933758, -5.19933758, -5.19933758, -5.19933758,
            5.19933758, -5.19933758, -5.19933758, -5.19933758, -5.19933758,
            -5.19933758,  5.19933758, -5.19933758]]

        resp = instancia_metricas.calcular_pontuacao(X, [0, 1, 1])
        assert type(resp) == dict
        assert pytest.approx(resp.get('silhouette_score_euclidean'), 0.1) == 0.379

