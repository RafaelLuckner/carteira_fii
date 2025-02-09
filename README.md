# 📈 Projeto de Carteira de FIIs  

Este projeto tem como objetivo coletar, processar e analisar dados de Fundos Imobiliários (FIIs) para otimizar a tomada de decisão na construção de uma carteira de investimentos.  

## 💁️ Estrutura do Projeto  

A estrutura do projeto é organizada da seguinte forma:  

```
carteira_fiis/
│── data/
│   ├── raw/         # Dados brutos coletados de APIs e web scraping  
│   ├── processed/   # Dados tratados e prontos para análise  
│   └── final/       # Dados finais utilizados na modelagem  
│  
│── etl/  
│   ├── extract.py   # Scripts para coleta de dados (APIs, web scraping)  
│   ├── transform.py # Processamento e limpeza dos dados  
│   └── load.py      # Armazenamento dos dados processados  
│  
│── analysis/  
│   ├── metrics.py      # Cálculo de métricas financeiras (DY, P/VP, FFO Yield)  
│   └── optimization.py # Algoritmos de otimização da carteira  
│  
│── dashboard/  
│   └── app.py  # Aplicação web para visualização dos dados  
│  
│── models/  
│   └── model.py  # Modelos de Machine Learning para análise preditiva  
│  
│── utils/  
│   └── helpers.py  # Funções auxiliares para o projeto  
│  
│── logs/  
│   └── app.log  # Arquivo de log do sistema  
│  
│── config/  
│   └── settings.py  # Configurações do projeto  
│  
│── README.md       # Documentação do projeto  
│── requirements.txt # Dependências do projeto  
│── app.py          # Arquivo principal do projeto  
```

## 🚀 Funcionalidades  

- 📊 **Coleta de dados**: Obtém dados fundamentalistas e cotações de FIIs através de APIs e web scraping.  
- 🔍 **Análise financeira**: Calcula indicadores como Dividend Yield, P/VP, Volatilidade e FFO Yield.  
- 📈 **Otimização da carteira**: Aplica modelos de otimização para balancear risco e retorno.  
- 🌐 **Dashboard interativo**: Permite visualizar métricas e acompanhar a performance dos FIIs.  

## 📦 Instalação  

1. Clone este repositório:  
   ```bash
   git clone https://github.com/seu-usuario/carteira_fiis.git
   cd carteira_fiis
   ```  

2. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```  

3. Execute o pipeline de dados:  
   ```bash
   python etl/extract.py
   python etl/transform.py
   python etl/load.py
   ```  

4. Rode o dashboard:  
   ```bash
   python dashboard/app.py
   ```  

## 🛠 Tecnologias utilizadas  

- **Python** (pandas, numpy, requests, BeautifulSoup, Scikit-learn)  
- **APIs Financeiras** (Yahoo Finance, Status Invest, Alpha Vantage)  
- **Banco de Dados** (PostgreSQL, SQLite, MongoDB)  
- **Dashboard** (Streamlit, Dash)  

---

📌 **Mantenedor**: Seu Nome - [LinkedIn](https://linkedin.com/in/seu-perfil)  

📣 **Sugestões e melhorias são bem-vindas!** 🚀  