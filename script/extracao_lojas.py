import basedosdados as bd    #importa a biblioteca basedosdados para acessar os dados do Google Cloud
import pandas as pd    #importação da biblioteca pandas para manipulação de dados
from pathlib import Path

#Configuração dos diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output' #output é a pasta onde será salvo o resultado final do cruzamento entre a base de lojas e a planilha Fibra, com a coluna de perfil adicionada
PROJECT_ID = "projeto-512217"  #iD do meu projeto


#função principal 
def main():
    caminho_cidades = DATA_DIR / 'cidades_raio_250km.csv'  #nesse caminho está a base de cidades que estão dentro do raio de 250km a partir de Uberlândia-MG, gerada pelo script gerar_base_cidades.py
    
    if not caminho_cidades.exists():  #confirmação de existência do arquivo de cidades
        print(f"Erro: Arquivo {caminho_cidades} não foi encontrado na pasta data.")
        return


    df_cidades = pd.read_csv(caminho_cidades)   #base para cruzamento com a base de dados para achar as lojas que estão nesses municípios
    coluna_ibge = 'codigo_ibge' if 'codigo_ibge' in df_cidades.columns else 'codigo_municipio'  #codigo ibge para o cruzamento com a base de dados e achar o municipio
    df_cidades[coluna_ibge] = pd.to_numeric(df_cidades[coluna_ibge], errors='coerce').fillna(0).astype(int)
    codigos_ibge = [str(cod) for cod in df_cidades[coluna_ibge].tolist() if cod > 0]
    ibge_str = "', '".join(codigos_ibge)   #fazer o cruzamento com a base de dados para achar as lojas que estão nesses municípios

    print(f"Lendo as {len(df_cidades)} cidades do seu arquivo local...")
    print("Conectando à Base dos Dados para buscar AS LOJAS nesses municípios...")


#query da base de dados para buscar as lojas 

    query = f"""
    SELECT 
        e.cnpj,
        e.sigla_uf,
        e.id_municipio,
        e.cnae_fiscal_principal,
        e.nome_fantasia,
        CONCAT(e.ddd_1, e.telefone_1) AS telefone_1,
        CONCAT(e.ddd_2, e.telefone_2) AS telefone_2,
        e.email,
        e.logradouro,
        e.numero,
        e.bairro
    FROM `basedosdados.br_me_cnpj.estabelecimentos` AS e
    WHERE e.id_municipio IN ('{ibge_str}')
      AND e.cnae_fiscal_principal IN ('4744002', '4744099', '4679604', '1610203')
      AND e.situacao_cadastral IN ('2', '02')
    """


    try:
        df_lojas = bd.read_sql(query, billing_project_id=PROJECT_ID)  #dentro do projeto, a função read_sql executa a query e retorna um DataFrame com os resultados
        if not df_lojas.empty:
            df_cidades[coluna_ibge] = df_cidades[coluna_ibge].astype(str)
            df_final = df_lojas.merge(
                df_cidades[[coluna_ibge, 'nome']], 
                left_on='id_municipio',   #df final com a merge das informções da base de dados e a base de cidades que estão dentro do raio de 250km a partir de Uberlândia-MG
                right_on=coluna_ibge, 
                how='left'
            )
            
            df_final.rename(columns={'nome': 'municipio'}, inplace=True)
            df_final.drop(columns=[coluna_ibge], inplace=True)
            caminho_saida = OUTPUT_DIR / 'lojas_encontradas.xlsx'  #leva tudo para o output e nesse arquivo excel
            df_final.to_excel(caminho_saida, index=False)  #final vai para o arquivo excel na pasta output com os nomes, telefones e endereços das lojas encontradas
            
            print(f"\n✅ SUCESSO! O código foi na internet e trouxe {len(df_final)} lojas para você.")
            print(f"📁 A planilha com os nomes, telefones e endereços das lojas foi exitosa e foi salva em: {caminho_saida}")
        else:
            print("\n⚠️ Nenhuma loja encontrada. Verifique realmente se os CNAEs existem nestas cidades")

    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main()