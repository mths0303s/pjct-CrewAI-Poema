import litellm
from crewai import Agent, Task, Crew, Process

#Definindo os inputs para a escrita e resposta da carta
nome_remetente = input("Nome do remetente: ")
nome_destinatario = input("Nome do destinatário: ")
sentimentos_para_destinatario = input("Sentimentos que você quer passar para o destinatário: ")
sentimentos_para_remetente = input("Sentimentos que você quer passar para o remetente da carta: ")


#Criando o Agente gerenciador
agente_gerenciador = Agent(
    role='Gerente de Projeto',
    goal='''Organizar e supervisionar as tarefas do processo hierárquico para garantir que cada etapa seja concluída corretamente,
      mantenha os processos na lingua portuguesa falada pelos brasileiros, somente adiministre o processo e corrija-o quando for necessário.''',
    verbose=True,
    memory=True,
    llm="ollama/llama3.1:8b",
    backstory="Você é um gerente de projeto experiente, responsável por coordenar todas as etapas e garantir que as tarefas sejam realizadas na sequência correta."
)

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
    backstory='''Você é uma poetiza experiente, grata e gentil.
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

#Definindo a tarefa de responder a carta
tarefa_escrita_resposta = Task(
    description="Escrever uma resposta para a carta de amor do remetente",
    expected_output="Uma resposta para a carta de amor escrita com as palavras lindas do remetente",
    agent=agente_destinatário,
    input=tarefa_escrita_carta.output_file,
    output_file="respostaCarta.md"
)


#Criando a Crew com o agente destinátario e a tarefa de responder a carta
equipe = Crew(
    agents=[agente_remetente, agente_destinatário],
    tasks=[tarefa_escrita_carta, tarefa_escrita_resposta],
    process=Process.hierarchical,
    manager_agent=agente_gerenciador
)

#Executando a tarefa e mostrando o resultado da reposta da carta no terminal
resultados = equipe.kickoff(inputs={
    'nome_destinatario':nome_destinatario, 
    'sentimentos_para_destinatario': sentimentos_para_destinatario,
    'nome_remetente':nome_remetente, 
    'sentimentos_para_remetente': sentimentos_para_remetente
    })

print("\n\nCarta de Amor:\n\n", resultados)