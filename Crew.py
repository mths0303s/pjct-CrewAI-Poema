import litellm
from crewai import Agent, Task, Crew, Process

#Definindo os inputs para a escrita e resposta da carta
nome_remetente = input("Nome do remetente: ")
nome_destinatario = input("Nome do destinatário: ")
sentimentos_para_destinatario = input("Sentimentos que você quer passar para o destinatário: ")
sentimentos_para_remetente = input("Sentimentos que você quer passar para o remetente da carta: ")

#Criando o Agente remetente
agente_remetente = Agent(
    role='Escritor de Cartas de Amor',
    goal='escrever uma carta de amor para {nome_destinatario}, '
    'expressando os seguintes sentimentos: {sentimentos_para_destinatario}.',
    verbose=True,
    memory=True,
    llm="ollama/llama3.1:8b",
    backstory='''Você é um poeta experiente,
    conhecido por sua habilidade de expressar sentimentos
    profundos em palavras.'''
)

#Criando o Agente que responderá a carta.
agente_destinatário = Agent(
    role='Responder uma carta de amor',
    goal='escrever uma reposta para a carta de amor cujo o remetente foi o {nome_remetente}, '
    'expressando os seguintes sentimentos: {sentimentos_para_remetente}.',
    verbose=True,
    memory=True,
    llm="ollama/llama3.1:8b",
    backstory='''Você é um poetiza experiente, grata e gentil.
    conhecida por sua habilidade de responder os sentimentos
    profundos escritos nas palavras de quem te ama.'''
)



#Definindo a tarefa de escrever a carta
tarefa_escrita_carta = Task(
    description="Escrever uma carta de amor para o destinatário",
    expected_output="Uma carta de amor escrita com palavras lindas que aquecem o coração",
    agent=agente_remetente,
    output_file="carta.md"
)

#Criando a Crew com o agente rementente e a tarefa que escreve a carta
equipe_escrita = Crew(
    agents=[agente_remetente],
    tasks=[tarefa_escrita_carta],
    process=Process.sequential
)

#Executando a tarefa e mostrando o resultado da escrita da carta no terminal
resultados_escrita = equipe_escrita.kickoff(inputs={'nome_destinatario':nome_destinatario, 'sentimentos_para_destinatario': sentimentos_para_destinatario})

print("Carta de Amor:\n\n", resultados_escrita)

#Lendo o arquivo gerado
with open("carta.md", "r") as f:
    carta = f.read()


#Definindo a tarefa de responder a carta
tarefa_escrita_resposta = Task(
    description="Escrever uma resposta para a carta de amor do remetente",
    expected_output="Uma resposta para a carta de amor escrita com as palavras lindas do remetente",
    agent=agente_destinatário,
    input=carta,
    output_file="respostaCarta.md"
)

#Criando a Crew com o agente destinátario e a tarefa de responder a carta
equipe_resposta = Crew(
    agents=[agente_destinatário],
    tasks=[tarefa_escrita_resposta],
    process=Process.sequential
)


#Executando a tarefa e mostrando o resultado da reposta da carta no terminal
resultados_resposta = equipe_resposta.kickoff(inputs={'nome_remetente':nome_remetente, 'sentimentos_para_remetente': sentimentos_para_remetente})

print("\n\nResposta para a carta de Amor:\n\n", resultados_resposta)