import pandas as pd
#carrega a planilha limpa
def carregar_dados():
    df = pd.read_csv("data/vendas_limpas.csv", sep=";", decimal=",")
    return df

#pedidos concluidos
def receita_total(df):
    concluidos = df[df["status"] == "concluido"]
    return concluidos["receita"].sum()
    #txt rapido
#  quantos pedidos concluídos
def total_pedidos(df):
    concluidos = df[df["status"] == "concluido"]
    return len(concluidos)

#  ticket médio: receita dividida pelos pedidos
def ticket_medio(df):
    return round(receita_total(df) / total_pedidos(df), 2)

#  quantos clientes diferentes compraram
def clientes_unicos(df):
    concluidos = df[df["status"] == "concluido"]
    return concluidos["cliente_id"].nunique()

#  a porcentagem de pedidos cancelados
def taxa_cancelamento(df):
    cancelados = df[df["status"] == "cancelado"]
    return round(len(cancelados) / len(df) * 100, 2)
    # 👥💰 receita média por cliente: quanto, em média, cada cliente gastou
def receita_por_cliente(df):
    return round(receita_total(df) / clientes_unicos(df), 2)
# 📈 a receita de cada mês, só dos pedidos concluídos
def receita_por_mes(df):
    concluidos = df[df["status"] == "concluido"].copy()
    concluidos["mes"] = pd.to_datetime(concluidos["data"]).dt.strftime("%Y-%m")
    return concluidos.groupby("mes")["receita"].sum().reset_index()
if __name__ == "__main__":

    #  testes
    df = carregar_dados()
    print("Receita total: R$", round(receita_total(df), 2))
    print("Pedidos:", total_pedidos(df))
    print("Ticket médio: R$", ticket_medio(df))
    print("Clientes únicos:", clientes_unicos(df))
    print("Taxa de cancelamento:", taxa_cancelamento(df), "%")
    print(receita_por_mes(df))
    print("Receita por cliente: R$", receita_por_cliente(df))