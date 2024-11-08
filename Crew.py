from litellm import completion
from crewai import Agent, Task, Crew, Process

#Criando o Agente
agente_escritor = Agent(
    role='Escritor de Cartas de Amor',
    goal='escreva uma carta de amor para {nome_destinatario}, '
    'expressando os seguintes sentimentos: {sentimentos}.',
    verbose=True,
    memory=True,
    llm="ollama/llama3.1:8b",
    backstory='''Você é um poeta experiente,
    conhecido por sua habilidade de expressar sentimentos
    profundos em palavras.'''
)

#Definindo a tarefa
tarefa_escrita_carta = Task(
    description="Escrever uma carta de amor para o destinatário",
    expected_output="Uma carta de amor escrita com palavras lindas que aquecem o coração",
    agent=agente_escritor,
    output_file="amor.md"
)

#Criando a Crew com o agente e a tarefa
equipe = Crew(
    agents=[agente_escritor],
    tasks=[tarefa_escrita_carta],
    process=Process.sequential
)

nome_destinatario = "Maria"
sentimentos = "Amor profundo"

resultados = equipe.kickoff(inputs={'nome_destinatario':nome_destinatario, 'sentimentos': sentimentos})

print("Carta de Amor:\n", resultados)