import os
from dotenv import load_dotenv
from openai import OpenAI
from metricas import receita_total, total_pedidos, ticket_medio, clientes_unicos, taxa_cancelamento, receita_por_cliente

# 🔐 abre o cofre: lê o arquivo .env
load_dotenv()

# 📞 conecta no OpenRouter, usando a chave do cofre
cliente = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
modelo = os.getenv("OPENROUTER_MODEL")


# 🏭 monta uma "etiqueta" no formato que a IA entende
def etiqueta(nome, descricao):
    return {
        "type": "function",
        "function": {
            "name": nome,
            "description": descricao,
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }


# 🏷️ a caixa de calculadoras: o nome de cada função e para que ela serve
FERRAMENTAS = [
    etiqueta("receita_total", "Calcula a receita total, em reais, dos pedidos concluídos."),
    etiqueta("total_pedidos", "Conta quantos pedidos foram concluídos."),
    etiqueta("ticket_medio", "Calcula o ticket médio: quanto, em média, cada pedido concluído gastou, em reais."),
    etiqueta("clientes_unicos", "Conta quantos clientes diferentes compraram nos pedidos concluídos, sem repetir."),
    etiqueta("taxa_cancelamento", "Calcula a porcentagem de pedidos cancelados, em relação ao total de pedidos."),
    etiqueta("receita_por_cliente", "Calcula a receita média por cliente: quanto, em média, cada cliente gastou no total, em reais."),  # ✨ NOVA
]


# 📒 a agenda: o nome (texto) de cada função → a função de verdade
FUNCOES = {
    "receita_total": receita_total,
    "total_pedidos": total_pedidos,
    "ticket_medio": ticket_medio,
    "clientes_unicos": clientes_unicos,
    "taxa_cancelamento": taxa_cancelamento,
    "receita_por_cliente": receita_por_cliente,  # ✨ NOVA
}


# 💬 o jeito ANTIGO: pergunta para a IA, entregando os números como "contexto"
def perguntar(pergunta, contexto):
    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": "Você é um assistente de vendas. Responda em português, usando SÓ estes números: " + contexto},
            {"role": "user", "content": pergunta},
        ],
    )
    return resposta.choices[0].message.content


# 🔄 o jeito NOVO: a IA escolhe a ferramenta, o Python calcula, a IA explica
def conversar(pergunta, df):
    mensagens = [
        {"role": "system", "content": "Você é um assistente de vendas. Responda em português. Para qualquer número, use SEMPRE as ferramentas. Nunca invente números."},
        {"role": "user", "content": pergunta},
    ]

    # 🔁 RODADA 1: manda a pergunta E a caixa de calculadoras
    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=mensagens,
        tools=FERRAMENTAS,
    )
    mensagem = resposta.choices[0].message

    # 🤔 a IA pediu alguma calculadora?
    if mensagem.tool_calls:
        mensagens.append(mensagem)

        for pedido in mensagem.tool_calls:
            nome = pedido.function.name               # 📛 o nome que a IA pediu
            resultado = FUNCOES[nome](df)              # 🧮 o Python roda a função de verdade!
            mensagens.append({
                "role": "tool",
                "tool_call_id": pedido.id,
                "content": str(resultado),
            })

        # 🔁 RODADA 2: manda os resultados, e a IA explica
        resposta = cliente.chat.completions.create(model=modelo, messages=mensagens)
        mensagem = resposta.choices[0].message

    return mensagem.content


# 🧪 teste: só roda quando eu rodo ESTE arquivo
if __name__ == "__main__":
    from metricas import carregar_dados
    df = carregar_dados()
    print(conversar("Quanto cada cliente gastou, em média?", df))