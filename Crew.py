from litellm import completion
from crewai import Agent, Task, Crew, Process

nome_remetente = input("Nome do remetente: ")
nome_destinatario = input("Nome do destinatário: ")
sentimentos_para_destinatario = input("Sentimentos que você quer passar para o destinatário: ")
sentimentos_para_remetente = input("Sentimentos que você quer passar para o remetente da carta: ")

#Criando o Agente remetente
agente_remetente = Agent(
    role='Escritor de Cartas de Amor',
    goal='escrever uma carta de amor para {nome_destinatario}, '
    'expressando os seguintes sentimentos: {sentimentos_para_remetente}.',
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

#Definindo as tarefas e lendo o arquivo gerado
tarefa_escrita_carta = Task(
    description="Escrever uma carta de amor para o destinatário",
    expected_output="Uma carta de amor escrita com palavras lindas que aquecem o coração",
    agent=agente_remetente,
    output_file="carta.md"
)

with open("carta.md", "r") as f:
    carta = f.read()

tarefa_escrita_resposta = Task(
    description="Escrever uma resposta para a carta de amor do remetente",
    expected_output="Uma resposta para a carta de amor escrita com as palavras lindas do remetente",
    agent=agente_destinatário,
    input=carta,
    output_file="Respostadoamor.md"
)

#Criando a Crew com o agente e a tarefa
equipe = Crew(
    agents=[agente_remetente, agente_destinatário],
    tasks=[tarefa_escrita_carta, tarefa_escrita_resposta],
    process=Process.sequential
)

resultados = equipe.kickoff(inputs={'nome_destinatario':nome_destinatario, 'sentimentos_para_destinatario': sentimentos_para_destinatario})

print("Carta de Amor:\n", resultados)