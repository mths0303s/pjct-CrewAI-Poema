import chromadb
from openai import OpenAI

api_key = ""
client = OpenAI(api_key=api_key)

questao = input("""Como posso lhe ajudar?

""")

chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="db")
colletion = chroma_client.get_or_create_collection(name="artigo")

results = colletion.query(query_texts=questao, n_results=2)

conteudo = results["documents"][0][0] + results ["documents"][0][1]

prompt = """
Você é um assistente do Restaurante Sabores.
Use o seguinte contexto para responder a questão, não use nenhuma informação adicional, se não houver informação no contexto, responda: Desculpe mas não consigo ajudar. Tem alguma outra pergunta?
Sempre termine a resposta com: Foi um prazer falar com você, não deixe de provar nossos sabores e se houver outra pergunta, ficarei feliz em ajudá-lo.
"""

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": prompt,
        },
        {"role": "system", "content": conteudo},
        {"role": "user", "content": questao},
    ],
)

answer = completion.choices[0].message.content

print("\n\n",answer,"\n\n")