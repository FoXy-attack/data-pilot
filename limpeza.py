import pandas as pd
#le a planilha de vendas
df = pd.read_csv("data/sales.csv")
#transforma texto em data real
df["data"] = pd.to_datetime(df["data"], dayfirst=True)
#confere
print(df["data"].head())
#padroniza o status, tira espaços deixa minucuslo e tira os acentos
df["status"] = df["status"].str.strip().str.lower().str.replace("í","i")
#confere quanto de cada status
print(df["status"].value_counts())
# 🗑️ remove os pedidos repetidos
print("Linhas antes:", len(df))
df = df.drop_duplicates()
print("Linhas depois:", len(df))
#quantidade * preço
df["receita"] = df["quantidade"] * df["preco_unitario"]
#confere
print(df[["produto", "quantidade", "preco_unitario", "receita"]].head())
#salva a planilha limpa no padrao BR
df.to_csv("data/vendas_limpas.csv", sep=";", decimal=",", index=False)
print("planilha limpa salva")
#le de volta para conferir
df_limpo = pd.read_csv("data/vendas_limpas.csv", sep=";", decimal="i")
