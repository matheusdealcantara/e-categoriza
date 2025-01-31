import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Definir explicitamente o caminho dos dados do NLTK
nltk.data.path.append('C:/Users/theco/AppData/Roaming/nltk_data')


# Função para garantir que os recursos do NLTK estão disponíveis
def ensure_nltk_resources():
    try:
        stopwords.words('portuguese')
    except LookupError:
        nltk.download('stopwords')
    
    try:
        word_tokenize("test")
    except LookupError:
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        nltk.download('punkt_tab')

# Garantir que os recursos do NLTK estão disponíveis
ensure_nltk_resources()

def process_text(text):
    # Remover palavras comuns no texto e separar as palavras em tokens
    stop_words = set(stopwords.words('portuguese'))
    word_tokens = word_tokenize(text.lower())
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    
    # Retornar as palavras filtradas em uma string
    return ' '.join(filtered_sentence)