# Este arquivo testa a função classify_text do arquivo api/utils/categorize.py
from api.utils.categorize import classify_text

def test_classify_text():
    emails = [
        'Obrigado, o projeto está ótimo!',
        'Preciso de ajuda com o projeto.',
        'O projeto está atrasado.',
        'Parabéns pelo excelente trabalho!',
        'Há um problema com o projeto.',
        'O projeto foi concluído com sucesso.',
        'Preciso de mais informações sobre o projeto.',
        'O projeto está dentro do prazo.',
        'O projeto precisa de ajustes.',
        'O projeto está em andamento conforme o planejado.'
    ]

    for email in emails:
        result = classify_text(email)
        print(f'Email: {email}\nClassificação: {result}\n')

if __name__ == "__main__":
    test_classify_text()
