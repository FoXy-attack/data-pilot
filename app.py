import streamlit as st
import plotly.express as px
from metricas import carregar_dados, receita_total, total_pedidos, ticket_medio, receita_por_mes
from chat import conversar

#titulo
st.title("data pilot")

df = carregar_dados()

# o seletor dos dois menus, na barra lateral
menu = st.sidebar.radio("Menu", ["Painel", "Converse com os dados"])

# o filtro de categorias, na barra lateral
categorias = sorted(df["categoria"].unique())
escolhidas = st.sidebar.multiselect("Categorias", categorias, default=categorias)
# deixa só as linhas das categorias escolhidas
df = df[df["categoria"].isin(escolhidas)]

# a tela do PAINEL
if menu == "Painel":
    st.write("painel de vendas")
    col1,col2,col3 = st.columns(3)
    col1.metric("receita total", round(receita_total(df), 2))
    col2.metric("pedido", total_pedidos(df))
    col3.metric("ticket medio", ticket_medio(df))

    # o gráfico de receita por mês
    receita_mes = receita_por_mes(df)
    grafico = px.line(receita_mes, x="mes", y="receita", markers=True, title="Receita por mês")
    st.plotly_chart(grafico)

# a tela do CHAT
else:
    st.write("Pergunte sobre as vendas da loja!")
    pergunta = st.chat_input("Ex.: Qual foi a receita total?")

    if pergunta:
        st.chat_message("user").write(pergunta)
        resposta = conversar(pergunta, df)
        st.chat_message("assistant").write(resposta)