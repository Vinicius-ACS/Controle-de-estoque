# Controle de Estoque para Microempreendedores

Aplicação desktop em Python com interface gráfica para cadastro de produtos e controle de estoque.

## Problema
Microempreendedores frequentemente não possuem uma ferramenta simples para controlar entradas, saídas e níveis mínimos de estoque.

## Solução
Este projeto oferece uma interface gráfica intuitiva para gerenciar produtos, consultar quantidades e registrar movimentações.

## Publico Alvo
O público alvo deste projeto é pequenos empreendedores que queiram fazer um controle de estoque simples.

## Funcionalidades
- cadastro de produtos;
- edição e exclusão;
- entrada e saída de estoque;
- busca por nome;
- alerta de estoque baixo.

## Tecnologias
- Python
- Tkinter
- SQLite
- pytest
- ruff

## Como executar
```bash
# Clone o repositório:
git clone https://github.com/Vinicius-ACS/Controle-de-estoque.git
cd projeto1

# Instale as dependências:
pip install -r requirements.txt

# Rode o arquivo:
python app/ui/start_window.py

## Primeiro acesso ao iniciar o sistema:

1. Crie um novo usuário na tela de cadastro
2. Utilize o login criado para acessar o sistema

# Rode os testes:
pytest

# Rode o lint
ruff check .
