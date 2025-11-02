# Frontend Automation Testing Project

Validar fluxo de cadastro com: validações dinâmicas, elementos assíncronos e componentes customizados.

## Setup

1. Instalar Python 3.x
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Running Tests
Primeiro deve ativar um ambiente virtual Python (venv): venv\Scripts\activate
To run the tests:
```bash
pytest tests/
```

## Project Structure

- `pages/`: Estruturado em Page Object Models
  - `base_page.py`: Definicao de classe base, onde contem metodos e utilitarios comuns como clicar em elementos, preencher campos aguardar visibilidade.
  - `practice_form_page.py`: Definicao de classes especificas do formulario do DemoQA, herdando da base_page
- `tests/`: Arquivos de teste
- `requirements.txt`: Dependencias do projeto 
