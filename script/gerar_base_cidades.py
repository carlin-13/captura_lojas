import pandas as pd
import numpy as np
from pathlib import Path  #caminho para pegar do caminho .resolve



BASE_DIR =Path(__file__).resolve().parent.parent        # caminho para pegar do caminho
DATA_DIR =  BASE_DIR / 'data'  #ajuste para pegar a pasta data


#Função referente ao cálculo da distância


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 #raio médio do planeta Terra em quilometros
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)  #os valores de latitude e longitude do primeiro elemento
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2) #os valores de latitude e longitude do segundo elemento
    dlon = lon2_rad - lon1_rad   #faz a subtração das longitudes
    dlat = lat2_rad - lat1_rad   #faz a subtração das latitudes
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2  #cálculo da fórmula de Haversine(a distância mais curta ao longo da superfície de uma esfera) - REF: Heavenly Mathematics: The Forgotten Art of Spherical Trigonometry - 2012
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))  #cálculo do ângulo central
    return R * c  #retorna a distância em quilômetros entre os dois pontos geográficos

#Função de geração da base de munícipios referentes ao raio de 250km a partir de Uberlândia-MG

def gerar_base_municipios():
    print("Captando a base oficial de municipios e calculando a distância a partir de Uberlândia...")

    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv"   #municipios.csv é a base oficial de municípios do Brasil, com os códigos IBGE, nomes, estados e coordenadas geográficas (latitude e longitude)
    df = pd.read_csv(url)    #salva a base oficial de municípios do Brasil em um DataFrame do Pandas
    uberlandia_lat, uberlandia_lon = -18.918804, -48.276784  #dados de latitude e longitude de Uberlândia-MG, que é o ponto central do raio de 250km
    
    df['distancia_km'] = calcular_distancia_haversine( 
        uberlandia_lat, uberlandia_lon, df['latitude'], df['longitude'])   #aplicando as variaveis para o cálculo da distância entre Uberlândia-MG e os demais municípios do Brasil
  
    df_alvo = df[df['distancia_km'] <= 250].copy()
    df_alvo = df_alvo.sort_values('distancia_km')  #ordena os municípios por distância
    df_alvo = df_alvo[['codigo_ibge', 'nome', 'codigo_uf', 'latitude', 'longitude', 'distancia_km']]   #organiza as colunas do DataFrame final
    
    caminho_saida = DATA_DIR / 'cidades_raio_250km.csv' 
    df_alvo.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
    print("Sucesso! Base de cidades atualizada com o código IBGE.")
if __name__ == "__main__":
    gerar_base_municipios()  #gera a base de municípios do Brasil que estão dentro do raio de 250km a partir de Uberlândia-MG e salva em um arquivo CSV na pasta data