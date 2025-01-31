# AutoU

Repositório para versionamento do código do processo seletivo para a empresa AutoU.

## Configuração e Execução da Aplicação Localmente

### Pré-requisitos

- Python 3.x
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)

### Passos para Configuração e Execução

Siga os passos abaixo para configurar e executar a aplicação localmente:

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/autou.git
    cd autou
    ```

    Alternativamente, você pode usar SSH:

    ```bash
    git clone git@github.com:seu-usuario/autou.git
    cd autou
    ```

    Ou usando GitHub CLI:

    ```bash
    gh repo clone seu-usuario/autou
    cd autou
    ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

    python -m venv venv

3. **Ative o ambiente virtual:**
    - No Windows
        venv\Scripts\activate

    - No macOS/Linux:
        source venv/bin/activate

4. **Instale as dependências:**

    pip install -r requirements.txt

5. **Configure as variáveis de ambiente:**
    Crie um arquivo .env na raiz do projeto e adicione as variáveis de ambiente necessárias. Por exemplo:

    DEBUG=True
    SECRET_KEY=sua_chave_secreta
    DATABASE_URL=sqlite:///db.sqlite3

6. **Aplique as migrações do banco de dados:**

    python manage.py migrate

7. **Execute o servidor de desenvolvimento:**

    python manage.py runserver


### Acessando a Aplicação

    Após executar o servidor de desenvolvimento, você pode acessar a aplicação no seu navegador através do endereço:

    ```
    http://127.0.0.1:8000/
    ```

### Estrutura do Projeto

    A estrutura básica do projeto é a seguinte:

    ```
    autou/
    ├── manage.py
    ├── autou/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── app/
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── static/
    │   └── css/
    │       └── style.css
    └── templates/
        └── base.html
    ```

### Executando Testes

    Para executar os testes, utilize o comando:

    ```bash
    python manage.py test
    ```

### Contribuição

Se você deseja contribuir com este projeto, siga os passos abaixo:

1. **Fork o repositório:**

    Clique no botão "Fork" no canto superior direito da página do repositório no GitHub.

2. **Clone o seu fork:**

    ```bash
    git clone https://github.com/seu-usuario/autou.git
    cd autou
    ```

3. **Crie uma branch para sua feature:**

    ```bash
    git checkout -b minha-feature
    ```

4. **Faça as alterações desejadas e commit:**

    ```bash
    git commit -am 'Adiciona minha nova feature'
    ```

5. **Envie suas alterações para o seu fork:**

    ```bash
    git push origin minha-feature
    ```

6. **Abra um Pull Request:**

    Vá até a página do repositório original e clique no botão "New Pull Request".

    Obrigado por contribuir!