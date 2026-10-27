# Automação de Captura de Lojas e PDVs 

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Requests / Selenium](https://img.shields.io/badge/Web_Scraping-gray.svg)]()
[![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-darkblue.svg)](https://pandas.pydata.org/)
[![LGPD Compliant](https://img.shields.io/badge/LGPD-Compliant-success.svg)]()

Um projeto de **Engenharia de Dados e Inteligência Comercial** desenhado para automatizar a extração, o monitoramento e a estruturação de dados de lojas e pontos de venda (PDVs). 

Este projeto substitui o levantamento manual por um pipeline inteligente de requisições web, tratamento de texto e atualização dinâmica de planilhas de mercado, preparando a base para análises de expansão e inteligência competitiva em dashboards (como o Power BI).

---

## 🧠 Arquitetura e Regras de Negócio (Diferenciais)

Foi construído com foco em **escalabilidade e confiabilidade dos dados**, aplicando lógicas de limpeza e normalização antes de qualquer gravação na base final.

*   **Captura Automatizada:** O script navega e extrai sistematicamente dados de localização, contato e características operacionais das lojas alvo, utilizando tratamento de exceções para lidar com instabilidades na fonte.
*   **Enriquecimento e Geolocalização:** Cruzamento de informações e sanitização de CEPs (podendo integrar com soluções como a Brasil API) para garantir a precisão espacial de cada PDV no mapa.
*   **Validação e Higienização de Dados:** Filtros robustos para remover duplicidades e normalizar strings (remoção de caracteres especiais, formatação e padronização Unicode), garantindo que a base de inteligência não seja corrompida.
*   **LGPD e Confidencialidade:** Para fins de portfólio público, **este repositório foi higienizado**, ou seja, os nomes de clientes reais, chaves de acesso e bases confidenciais foram substituídas por nomes genéricos e dados anonimizados.

---

## ⚙️ Funcionalidades

- [x] Extração em lote de informações de lojas a partir de fontes web.
- [x] Tratamento de ruídos na leitura dos dados e padronização de textos.
- [x] Consolidação autônoma das informações e exportação para formatos tabulares estruturados (`.xlsx` ou `.csv`).
- [x] Arquitetura modular facilitando a futura integração direta com bancos de dados (como PostgreSQL).

---

## 📁 Estrutura do Projeto

```text
captura_lojas/
│
├── data/                        #Diretório de dados 
│   ├── base_lojas.xlsx          #Planilha modelo (Anonimizada)
│   └── raw/                     #Arquivos e logs temporários de captura
│
├── script/
│   ├── main.py                  #Script principal de automação e requisições
│   └── processamento.py         #Lógicas de tratamento e higienização com Pandas
│
├── requirements.txt             #Dependências do projeto
└── README.md
