# Essa função é responsável por classificar os emails entre produtiovo e,
# improdutivo. Ela utiliza um modelo de classificação de texto pré-treinado
import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()
client = InferenceClient(api_key=os.getenv('HF_API_KEY'))

def classify_text(text: str):
    message = {
        "role": "user",
        "content": f"""
        Você é um assistente virtual que deve categorizar emails entre "Produtivo" ou "Improdutivo", onde emails produtivos são 
        Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema,
        solicitação de reuniões, atualizações sobre o andamento de projetos, etc). 
        e emails improdutivos são Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos, elogios,
        informações desnecessárias, etc). 
        Responda apenas com a palavra "Produtivo" ou "Improdutivo".
        Classifique o email abaixo:\n\nEmail:\n{text}"""
    }

    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct", 
        messages=[message], 
        temperature=0.5,
        max_tokens=2048,
        top_p=0.7,
        stream=True
    )


    response_text = ""
    for chunk in stream:
        response_text += chunk.choices[0].delta.content

    return response_text.strip()
