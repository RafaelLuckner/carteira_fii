import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import ast
import sys


# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helpers import logger


# mudando layout para wide
st.set_page_config(layout="wide")

# Nome do arquivo CSV para armazenar os dados
data_file = "data/final/fiis_carteira.csv"

# Colunas do dataset
columns = [
    "Código", "Tipo", "Segmento", "Categoria", "Dividend Yield (%)",
    "P/VP", "Vacância (%)", "Preço Médio (R$)", "Qtde Cotas", "Valor Investido (R$)", "% da Carteira"
]

# Verifica se já existe um arquivo CSV, senão cria um dataframe vazio
def load_data():
    if os.path.exists(data_file):
        logger.info("Iniciando load data")
        df = pd.read_csv(data_file)
        # Converte a coluna 'Segmento' de volta para lista
        df["Segmento"] = df["Segmento"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else [])
        return df
    else:
        print("Arquivo CSV não encontrado.")
        logger.info("Load data falhou")
        return pd.DataFrame(columns=columns)

def save_data(df):
    # Certifique-se de que a coluna 'Segmento' seja tratada corretamente como lista
    df["Segmento"] = df["Segmento"].apply(lambda x: str(x) if isinstance(x, list) else x)
    
    # Recalcular os valores de "% da Carteira"
    total_investido = df["Valor Investido (R$)"].sum()
    df["% da Carteira"] = (df["Valor Investido (R$)"] / total_investido) * 100 if total_investido > 0 else 0

    # Garante que o CSV seja salvo apenas com as colunas desejadas
    df = df[columns]  # Mantém as colunas esperadas
    df.to_csv(data_file, index=False)

def atualizar_dataframe(df):
    df["Valor Investido (R$)"] = df["Preço Médio (R$)"] * df["Qtde Cotas"]
    total_investido = df["Valor Investido (R$)"].sum()
    df["% da Carteira"] = (df["Valor Investido (R$)"] / total_investido) * 100 if total_investido > 0 else 0
    return df

def dividir_percentual(df):
    df_exploded = df.explode("Segmento")  # Explodir a coluna de segmentos
    df_exploded["% da Carteira"] = df_exploded.groupby("Código")["% da Carteira"].transform(lambda x: x / len(x))
    return df_exploded

# Carregar dados
st.title("📊 Gerenciador de FIIs")
df = load_data()
df = atualizar_dataframe(df)

# Criar abas
tab1, tab2, tab3 = st.tabs(["Adicionar ou Modificar Ativo", "Visualizar Carteira", "Remover Ativo"])

segmentos = ["Cri (Crédito Imobiliário)", "Shoppings", "Fundo de Fundos (FoF)",
              "Galpões Logísticos/Indústrial", "Hotéis", "Lajes Corporativas",
                "Renda Urbana","Terras Agricolas", "Outros"]

with tab1:
    st.subheader("➕ Adicionar ou Modificar FII")
    codigo = st.selectbox(
    "Código do FII",
    ['Adicionar Novo']+df['Código'].tolist() )

    if codigo in df["Código"].values:  # Verifica se o código já existe
        # Exibe as informações do fundo para edição
        st.write("Fundo já existe, modifique os dados abaixo.")
        selected_index = df[df["Código"] == codigo].index[0]

        with st.form("edit_fii_form"):
            codigo = st.text_input("Código do FII", value=df.at[selected_index, "Código"]).upper()
            tipo = st.selectbox("Tipo", ["Tijolo", "Papel"], index=["Tijolo", "Papel"].index(df.at[selected_index, "Tipo"]))
            segmento = st.multiselect("Segmento", segmentos, default=df.loc[selected_index, "Segmento"])
            categoria = st.selectbox("Categoria", ["Ancoragem", "Oportunidade", "Risco"])
            dy = st.number_input("Dividend Yield (%)", min_value=0.0, step=0.25, value=df.at[selected_index, "Dividend Yield (%)"])
            p_vp = st.number_input("P/VP", min_value=0.0, step=0.01, value=df.at[selected_index, "P/VP"])
            vacancia = st.number_input("Vacância (%)", min_value=0.0, step=0.1, value=df.at[selected_index, "Vacância (%)"])
            preco_medio = st.number_input("Preço Médio (R$)", min_value=0.0, step=0.1, value=df.at[selected_index, "Preço Médio (R$)"])
            qtde_cotas = st.number_input("Qtde Cotas", min_value=1, step=1, value=df.at[selected_index, "Qtde Cotas"])

            submitted_edit = st.form_submit_button("Modificar")
            if submitted_edit:
                # Atualiza os dados do fundo
                df.at[selected_index, "Código"] = codigo
                df.at[selected_index, "Tipo"] = tipo
                df.at[selected_index, "Segmento"] = segmento
                df.at[selected_index, "Categoria"] = categoria
                df.at[selected_index, "Dividend Yield (%)"] = dy
                df.at[selected_index, "P/VP"] = p_vp
                df.at[selected_index, "Vacância (%)"] = vacancia
                df.at[selected_index, "Preço Médio (R$)"] = preco_medio
                df.at[selected_index, "Qtde Cotas"] = qtde_cotas
                df = atualizar_dataframe(df)
                save_data(df)
                st.success("Fundo modificado com sucesso!")
                time.sleep(3)
                st.rerun()

    else:
        with st.form("add_fii_form"):
            codigo = st.text_input("Código do FII").upper()
            tipo = st.selectbox("Tipo", ["Tijolo", "Papel"])
            segmento = st.multiselect("Segmento", segmentos)
            categoria = st.selectbox("Categoria", ["Ancoragem", "Oportunidade", "Risco"])
            dy = st.number_input("Dividend Yield (%)", min_value=0.0, step=0.25)
            p_vp = st.number_input("P/VP", min_value=0.0, step=0.01)
            vacancia = st.number_input("Vacância (%)", min_value=0.0, step=0.1)
            preco_medio = st.number_input("Preço Médio (R$)", min_value=0.0, step=0.1)
            qtde_cotas = st.number_input("Qtde Cotas", min_value=1, step=1)

            submitted = st.form_submit_button("Adicionar")
            if submitted and codigo:
                new_row = pd.DataFrame([[codigo, tipo, segmento, categoria, dy, p_vp, vacancia, preco_medio, qtde_cotas, 0, 0]], columns=columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df = atualizar_dataframe(df)
                st.success("Fundo adicionado com sucesso!")
                time.sleep(3)
                save_data(df)
                st.rerun()



paleta = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

if not df.empty:
    with tab2:
        st.subheader("📋 Sua Carteira de FIIs")
        st.dataframe(df)
        st.subheader("📈 Análise da Carteira")
        subtab1, subtab2, subtab3 = st.tabs(["Por Categoria", "Por Segmento", "Proventos"])
        with subtab1:
            
            fig = px.pie(
                values=df["% da Carteira"].round(2),
                names=df["Categoria"],
                color_discrete_sequence=paleta)

            fig.update_traces(marker=dict(line=dict(color='black', width=1)))  
            fig.update_layout(
                legend_title=dict(text='Segmentos', font=dict(size=14, color='black')),
                font=dict(size=12, family='Arial')
            )
            
            
            st.plotly_chart(fig)



        # Atualize o gráfico para exibir os dados com a porcentagem ajustada
        with subtab2:
            
            # Explodir e dividir a porcentagem
            df_exploded = dividir_percentual(df)
            # Agrupar por segmento e calcular a soma da % da carteira
            segmento_soma = df_exploded.groupby("Segmento")["% da Carteira"].sum()
            segmento_soma = segmento_soma.round(2)
            # Exibir o gráfico de barras

            fig = px.pie(
                values=segmento_soma,
                names=segmento_soma.index,
                color_discrete_sequence=paleta
                )

            fig.update_traces(marker=dict(line=dict(color='black', width=1)))  
            fig.update_layout(
                legend_title=dict(text='Segmentos', font=dict(size=14, color='black')),
                font=dict(size=12, family='Arial')
            )
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(fig)


            with subtab3:

                dfaux = df.copy()
                # Calcular o valor total da carteira
                total_investido = dfaux["Valor Investido (R$)"].sum()

                # Calcular a média ponderada dos dividendos
                dfaux["Valor Esperado Anual (R$)"] = np.round((dfaux["Valor Investido (R$)"] * dfaux["Dividend Yield (%)"] / 100),2)
                media_ponderada_dividendos = dfaux["Valor Esperado Anual (R$)"].sum() / total_investido

                # Calcular o valor mensal e anual que será recebido
                valor_mensal_total = dfaux["Valor Esperado Anual (R$)"].sum() / 12
                valor_anual_total = valor_mensal_total * 12

                st.write(f"**Média Ponderada de Dividendos da Carteira:** {media_ponderada_dividendos*100:.2f}%")
                st.write(f"**Valor Total Esperado de Dividendos Anuais:** R${valor_anual_total:,.2f}")
                st.write(f"**Valor Total Esperado de Dividendos Mensais:** R${valor_mensal_total:,.2f}")

                st.write("Abaixo estão os detalhes de cada FII e seu valor de dividendos esperado:")

                # Exibir uma tabela com os valores esperados de dividendos
                dfaux["Valor Esperado Mensal (R$)"] = (np.round(dfaux["Valor Esperado Anual (R$)"] / 12 ,2))
                
                df_analise = dfaux[["Código", "Dividend Yield (%)", "Valor Investido (R$)", "Valor Esperado Anual (R$)", "Valor Esperado Mensal (R$)"]]
                st.dataframe(df_analise)





    with tab3:
        st.subheader("🗑️ Remover FII")
        selected_fii = st.selectbox("Selecione um FII para remover", df["Código"].unique() if not df.empty else [])
        
        if selected_fii:
            if st.button("Remover FII"):
                df = df[df["Código"] != selected_fii]
                df = atualizar_dataframe(df)
                save_data(df)
                st.success("FII removido com sucesso!")
                time.sleep(3)
                st.rerun()
else :
    st.error("Nenhum FII encontrado. Adicione alguns e tente novamente.")