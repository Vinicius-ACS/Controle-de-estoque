# Controle de Estoque para Microempreendedores

Aplicação desktop em Python com interface gráfica para cadastro de produtos e controle de estoque.

## Link público da aplicação

Repositório GitHub: https://github.com/Vinicius-ACS/Controle-de-estoque

Download do executável: https://github.com/Vinicius-ACS/Controle-de-estoque/releases/tag/v1.3.0

> Obs: esta é uma aplicação desktop desenvolvida com Python e Tkinter. Por esse motivo, não possui deploy web tradicional em Vercel ou GitHub Pages. A publicação da aplicação foi realizada por meio do GitHub Releases, disponibilizando um executável para Windows.


## Problema

Microempreendedores frequentemente não possuem uma ferramenta simples, acessível e objetiva para controlar entradas, saídas e níveis mínimos de estoque.

A ausência desse controle pode gerar problemas como falta de produtos, excesso de mercadorias paradas, dificuldade de reposição e perda de informações importantes para a gestão do negócio.

## Solução

Este projeto oferece uma interface gráfica intuitiva para gerenciar produtos, consultar quantidades, registrar movimentações e visualizar a cotação atual do dólar.

A integração com a API pública de cotação USD/BRL agrega valor ao sistema, especialmente para pequenos empreendedores que trabalham com produtos importados ou que possuem custos influenciados pela variação cambial.

## Público-alvo

Pequenos empreendedores que queiram fazer um controle de estoque simples.

## API integrada

A aplicação consome uma API pública para consultar a cotação do dólar em relação ao real.

API utilizada:

```text
AwesomeAPI - Cotação USD/BRL

## Funcionalidades

- Cadastro de produtos;
- edição de produtos;
- exclusão de produtos;
- registro de entrada de estoque;
- registro de saída de estoque;
- busca de produtos por nome;
- alerta de estoque baixo;
- visualização de resumo do estoque;
- integração com API pública de cotação do dólar;
- atualização da cotação ao abrir o sistema;
- atualização manual pelo botão Atualizar;
- login e cadastro de usuários.

## Tecnologias

- Python;
- Tkinter;
- ttkbootstrap;
- SQLite;
- API AwesomeAPI;
- pytest;
- ruff;
- Git;
- GitHub Actions;
- PyInstaller.

## Como executar pelo codigo fonte

```bash
# clone o repositorio
git clone https://github.com/Vinicius-ACS/Controle-de-estoque.git

# Entre na pasta do projeto
cd Controle-de-estoque

# Instale as dependências de desenvolvimento
pip install -r requirements.txt

# Rode o sistema
python -m app.main
```

## Primeiro acesso

1. Crie um novo usuário na tela de cadastro.
2. Utilize o login criado para acessar o sistema.

## Testes

```bash
python -m pytest
```

## Lint

```bash
ruff check .
```

## Estrutura do projeto

```text
Controle-de-estoque/
├── .github/
│   └── workflows/
├── app/
│   ├── ui/
│   ├── main.py
│   ├── database.py
│   ├── exchange_service.py
│   ├── models.py
│   ├── repository.py
│   └── service.py
├── tests/
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```
