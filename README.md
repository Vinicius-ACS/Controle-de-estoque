# Controle de Estoque para Microempreendedores

Aplicação desktop em Python com interface gráfica para cadastro de produtos e controle de estoque.

## Problema

Microempreendedores frequentemente não possuem uma ferramenta simples para controlar entradas, saídas e níveis mínimos de estoque.

## Solução

Este projeto oferece uma interface gráfica intuitiva para gerenciar produtos, consultar quantidades, registrar movimentações e visualizar a cotação atual do dólar.

## Público-alvo

Pequenos empreendedores que queiram fazer um controle de estoque simples.

## Funcionalidades

- Cadastro de produtos;
- edição e exclusão de produtos;
- entrada e saída de estoque;
- busca por nome;
- alerta de estoque baixo;
- cotação do dólar via API ao abrir o sistema e pelo botão Atualizar.

## Tecnologias

- Python;
- Tkinter;
- SQLite;
- API AwesomeAPI para cotação USD/BRL;
- pytest;
- ruff.

## Como executar

```bash
# Entre na pasta do projeto
cd controle_estoque_interface_corrigida

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
