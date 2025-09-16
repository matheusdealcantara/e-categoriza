# Essa função é responsável por classificar os emails entre produtiovo e,
# improdutivo.
import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('NSCALE_SERVICE_TOKEN'), 
                base_url="https://inference.api.nscale.com/v1")

def classify_text(text: str):
    message = [{
        "role": "user",
        "content": f"""
        Você é um assistente virtual que deve categorizar emails entre "Produtivo" ou "Improdutivo", onde emails produtivos são 
        Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema,
        solicitação de reuniões, atualizações sobre o andamento de projetos, etc). 
        e emails improdutivos são Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos, elogios,
        informações desnecessárias, etc). 
        Responda apenas com a palavra "Produtivo" ou "Improdutivo".
        Classifique o email abaixo:\n\nEmail:\n{text}"""
    }]

    response = client.chat.completions.create(
        model="Qwen/Qwen3-4B-Instruct-2507", 
        messages= message,
    )


    return response.choices[0].message.content
