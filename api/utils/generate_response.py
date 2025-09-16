import os

from dotenv import load_dotenv
from openai import OpenAI

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Criar um cliente de inferência
client = OpenAI(api_key=os.getenv('NSCALE_SERVICE_TOKEN'), 
                base_url="https://inference.api.nscale.com/v1")

# Função para gerar uma resposta para um email
def generate_response(text: str) -> str:
    messages = [
        { "role": "user", "content": f"""Você é um assistente virtual de Inteligência Artificial que escreve respostas educadas e profissionais para emails. 
         Sua resposta deve ser educada e profissional. Evite erros gramaticais e ortográficos. 
         A resposta deve ser apropriada para o contexto do email, você deve gerar uma resposta única e original. 
         A resposta também não deve possuir nenhuma parte do email recebido, ela deve ser apenas uma resposta ao email.
         Por exemplo, caso o email possua "Obrigado, o projeto está ótimo!", a resposta deve ser algo como "Fico feliz que tenha gostado do projeto!".
         Ou, caso o email possua "Gostaria de solicitar uma atualização sobr e o status atual do projeto [Nome do Projeto]." 
         a resposta deve ser algo como "Claro, aqui está uma atualização sobre o projeto [Nome do Projeto]".
         Aqui está um exemplo de email que você deve responder:\n\nEmail:\n{text}"""}
    ]

    # Extrair texto da resposta
    response = client.chat.completions.create(
        model="Qwen/Qwen3-4B-Instruct-2507",
        messages = messages,
    )

    return response.choices[0].message.content