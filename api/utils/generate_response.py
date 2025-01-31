from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = InferenceClient(api_key=os.getenv('HF_API_KEY'))

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

    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct", 
        messages=messages, 
        temperature=0.9,
        max_tokens=1024,
        top_p=0.95,
        stream=True
    )

    response_text = ""
    for chunk in stream:
        response_text += chunk.choices[0].delta.content

    return response_text.strip()