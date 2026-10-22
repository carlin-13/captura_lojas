import pandas as pd
import requests  #importação da biblioteca requests para fazer requisições HTTP
import time
from pathlib import Path
from tqdm import tqdm   #importação da biblioteca tqdm para mostrar uma barra de progresso durante a execução do loop


#Configuração dos diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / 'output'


#Função para verificar o status cadastral de um CNPJ usando a Brasil API

def verificar_cnpj(cnpj):
    cnpj_limpo = str(cnpj).replace('.', '').replace('/', '').replace('-', '').strip()  #consulta na API
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"  #url da API para consultar o CNPJ
    
   #fluxo de retirada de informações da API, com tratamento de erros e limites de requisições
    try:
        time.sleep(1.5) #Pausa
        resposta = requests.get(url, timeout=10)   #faz a requisição GET para a API com um tempo limite de 10 segundos
        if resposta.status_code == 200:
            return resposta.json().get('descricao_situacao_cadastral', '')
        elif resposta.status_code == 429:
            time.sleep(15) #Se atingir o limite, aguarda e tenta novamente
            return verificar_cnpj(cnpj)
    except Exception:   #ao ocorrer qualquer exceção durante a requisição, retorna "ERRO"
        pass
    return "ERRO"

#Função principal para ler a base de lojas filtradas, verificar o status cadastral de cada CNPJ e salvar apenas as lojas ativas em um novo arquivo Excel

def main():
    caminho_entrada = OUTPUT_DIR / 'lojas_filtradas_150km.xlsx'   #caminhos
    caminho_saida = OUTPUT_DIR / 'lojas_confirmadas_ativas.xlsx'



    if not caminho_entrada.exists():
        print(f"Arquivo não encontrado: {caminho_entrada}")
        return
    print("Carregando a planilha de lojas...")
    df_lojas = pd.read_excel(caminho_entrada)    #Lê a planilha de lojas
    print(f"Iniciando verificação de {len(df_lojas)} lojas na Brasil API...")


    status_lista = []  #vetor para armazenar os status cadastrais de cada CNPJ


    for cnpj in tqdm(df_lojas['cnpj'], desc="Consultando API"):  #barra de progresso para mostrar o andamento da verificação dos CNPJs
        status_lista.append(verificar_cnpj(cnpj))
        
    df_lojas['status_brasil_api'] = status_lista  #dentro do vetor criado para armazenar os status ele transfere para o status lista(todos os status, ou seja, ATIVO OU INATIVO)
    
    df_ativas = df_lojas[df_lojas['status_brasil_api'] == 'ATIVA'].copy()   #pega somente os "ATIVA"
    df_ativas.to_excel(caminho_saida, index=False)
    
    print(f"\nFinalizado! Das {len(df_lojas)} lojas originais, {len(df_ativas)} foram confirmadas como ATIVAS hoje.")
    print(f"Arquivo salvo em: {caminho_saida}")

if __name__ == "__main__":
    main()

