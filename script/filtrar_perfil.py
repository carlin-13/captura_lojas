import pandas as pd    #importação da biblioteca pandas para manipulação de dados
import unicodedata     #importação da biblioteca unicodedata para normalizar os strings
from pathlib import Path

#Configuração dos diretórios
BASE_DIR = Path(__file__).resolve().parent.parent  #pega o caminho do diretório base do projeto
DATA_DIR = BASE_DIR / 'data'   #leva para a pasta data 
OUTPUT_DIR = BASE_DIR / 'output'  #leva para a pasta output


#funçao de padronização do nome da cidade para cruzamento congruente 
def padronizar_nome_cidade(texto):
    if pd.isna(texto):  #laço condicional para verificar se o valor é nulo
        return texto
    nfkd = unicodedata.normalize('NFKD', str(texto))   #variavel para normalizar o texto
    texto_limpo = "".join([c for c in nfkd if not unicodedata.combining(c)])   #laço para remover acentos e caracteres especiais do texto
    return texto_limpo.upper().strip()



#função principal para filtrar a base de lojas com base na planilha Fibra e adicionar o perfil correspondente

def main():
    caminho_lojas = OUTPUT_DIR / 'lojas_encontradas.xlsx' #leva para a pasta output o arquivo de lojas encontradas
    caminho_fibra = DATA_DIR / 'Fibra_Territorio_Captacao_Araxa_Uberlandia.xlsx'
    caminho_saida = OUTPUT_DIR / 'lojas_encontradas_150km.xlsx' #resultado final do cruzamento entre a base de lojas e a planilha Fibra, com a coluna de perfil adicionada

    if not caminho_lojas.exists():
        print(f"Erro: Arquivo {caminho_lojas} não encontrado.")
        return
    if not caminho_fibra.exists():
        print(f"Erro: Arquivo {caminho_fibra} não encontrado.")
        return



    print("Carregamento das planilhas...")
    df_lojas = pd.read_excel(caminho_lojas) 

    df_fibra = pd.read_excel(caminho_fibra, header=3) #pelo título da planilha Fibra, a primeira linha de dados começa na linha 4 (índice 3), então usamos header=3 para pular as linhas de cabeçalho

    print("Padronizando os nomes dos municípios para cruzamento...")
    df_fibra['cidade_padrao'] = df_fibra['Cidade'].apply(padronizar_nome_cidade) # padroniza os nomes das cidades na planilha Fibra

    mapa_perfil = dict(zip(df_fibra['cidade_padrao'], df_fibra['Perfil']))  #dicionário para mapear o nome da cidade padronizado para o perfil correspondente na planilha Fibra

    df_lojas['municipio_padrao'] = df_lojas['municipio'].apply(padronizar_nome_cidade)

    print("Filtrando e adicionando o perfil...")
    df_lojas_filtradas = df_lojas[df_lojas['municipio_padrao'].isin(mapa_perfil.keys())].copy()
    
    df_lojas_filtradas['perfil'] = df_lojas_filtradas['municipio_padrao'].map(mapa_perfil)
    df_lojas_filtradas.drop(columns=['municipio_padrao'], inplace=True)   #remove a coluna auxiliar de município padronizado após o mapeamento do perfil

    df_lojas_filtradas.to_excel(caminho_saida, index=False)  #salvamento do resultado final em um arquivo Excel na pasta output
    
    print(f"\n✅ SUCESSO! A base foi filtrada.")
    print(f"De {len(df_lojas)} lojas totais, restaram {len(df_lojas_filtradas)} lojas que estão na planilha Fibra.")
    print(f"Arquivo final salvo em: {caminho_saida}")

if __name__ == "__main__":
    main()