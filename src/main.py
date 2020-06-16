import os
import time
from json import dump

from utils import Utils
from fonte_dados import FonteDados
from metricas import Metricas
from preprocessamento import Preprocessamento
from modelo import Modelo

ARQUIVO_DADOS_PROCESSADOS = 'dados_processados.pkl'
ARQUIVO_MODELO = 'modelo.pkl'

def etapa_preprocessamento(com_verificacao=True, com_persistencia=False):
    utils = Utils()
    fonte_dados = FonteDados()
    preprocessamento = Preprocessamento()

    # Caminho dos dados processados
    arq_dados_processados = os.path.join(fonte_dados.diretorio_saida, ARQUIVO_DADOS_PROCESSADOS)
    
    # Caso não exista o arquivo de dados processados gera o preprocessamento
    if com_verificacao and os.path.isfile(arq_dados_processados):
        dados_processados = utils.ler_pickle(arq_dados_processados)
    else:
        dados_processados = preprocessamento.executar()

    # Persistencia de dados consiste em salvar o arquivo em disco
    if com_persistencia:
        utils.salvar_pickle(dados_processados, arq_dados_processados)
        
    
    return dados_processados
    
def etapa_modelagem(X=None, com_verificacao=True, com_persistencia=False):
    fonte_dados = FonteDados()
    utils = Utils()
    
    # Os dados podem ser passados por parâmetro, nesses casos não é necessario o preprocessamento
    if X is None:
        X = etapa_preprocessamento(com_verificacao=com_verificacao, com_persistencia=com_persistencia)
    
    # Caminho do modelo treinado
    arq_modelo_treinado = os.path.join(fonte_dados.diretorio_saida, ARQUIVO_MODELO)

    if com_verificacao and os.path.isfile(arq_modelo_treinado):
        modelo = utils.ler_pickle(arq_modelo_treinado)
    else:
        modelo = Modelo()
        modelo.treinar(X.drop(columns=['id']))

    # Opção de salvar o modelo em disco
    if com_persistencia:
        utils.salvar_pickle(modelo, arq_modelo_treinado)
        
    return modelo
    
def etapa_avaliacao(com_verificacao=True, com_persistencia=False):
    fonte_dados = FonteDados()
    metricas = Metricas()

    # Realiza as etapas de preprocessamento e modelagem com a opcao de salvar em disco
    X = etapa_preprocessamento(com_verificacao=com_verificacao, com_persistencia=com_persistencia)
    modelo = etapa_modelagem(X, com_verificacao=com_verificacao, com_persistencia=com_persistencia)

    resultados = []
    for p in range(1, 4):
        portifolio = fonte_dados.carregar_portifolio(p)
        portifolio = fonte_dados.gerar_portifolio(X, portifolio.id)

        rec = modelo.recomendar(portifolio.drop(columns=['id']))

        resultados.append({
            'caso': f'portifolio{p}',
            'quantidade_original': len(portifolio.index.values),
            'quantidade_recomendados': len(rec),
            'pontuacao': metricas.pontuacao(portifolio.index.values, rec)
        })

    if com_persistencia:
        with open(os.path.join(fonte_dados.diretorio_saida, 'resultados.json'), 'w') as f:
            dump(resultados, f)

    return resultados

if __name__ == "__main__":
    inicio_execucao = time.time()
    try:
        #etapa_preprocessamento(com_persistencia=True)
        #etapa_modelagem(com_persistencia=True)
        print(etapa_avaliacao(com_verificacao=True, com_persistencia=True))
        fim_execucao = time.time()
        tempo_executacao = fim_execucao - inicio_execucao
        print(f'tempo de execução: {tempo_executacao} segundos')
    except KeyboardInterrupt:
        fim_execucao = time.time()
        tempo_executacao = fim_execucao - inicio_execucao
        print(f'tempo de execução: {tempo_executacao} segundos')
    