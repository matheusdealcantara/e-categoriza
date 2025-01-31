# Essa função é responsável por classificar os emails entre produtiovo e,
# improdutivo. Ela utiliza um modelo de classificação de texto pré-treinado
from transformers import pipeline, AutoModelForSequenceClassification
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
model_path = os.getenv('MODEL_PATH')

def classify_text(text: str):
    
    classifier = pipeline("text-classification", model=model_path)
    result = classifier(text)
    label = result[0]['label']

    if label == "LABEL_0":
        return 0
    else:
        return 1
