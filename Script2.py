import chromadb
from openai import OpenAI

api_key = "Coloque sua chave API"
client = OpenAI(api_key=api_key)

while True:
    questao = input("Como posso lhe ajudar?\nDigite 'sair' para encerrar.\n\n")

    if questao.lower() == "sair":
        print("\n\nObrigado por usar o assistente do Restaurante Sabores! Até a próxima!")
        break

    chroma_client = chromadb.Client()
    chroma_client = chromadb.PersistentClient(path="db")
    colletion = chroma_client.get_or_create_collection(name="artigo")

    results = colletion.query(query_texts=questao, n_results=2)
    if results and "documents" in results and results["documents"]:
        conteudo = results["documents"][0][0] + results ["documents"][0][1]
    else:
        conteudo = "Desculpe, mas não consigo ajudar. Você Tem alguma outra pergunta?"

    prompt = """
    Você é um assistente educado e útil do Restaurante Sabores.
    Use o seguinte contexto para responder a questão, não use nenhuma informação adicional, se não houver informação no contexto, responda: Desculpe mas não consigo ajudar com isso.
    Depois de responder a pergunta, diga: Fico feliz por você ter usado nossos serviços, se houver mais dúvidas, sinta-se à vontade para perguntar.
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "system", "content": conteudo},
            {"role": "user", "content": questao},
        ],
    )

    answer = completion.choices[0].message.content

    print("\n\n",answer,"\n\n")