# BMVC Gestão

Aplicação web para gestão de clientes, produtos e vendas, com painel administrativo, controle de estoque, autenticação e atualização de indicadores em tempo real.

O projeto utiliza Python com Bottle na camada HTTP, SQLAlchemy para persistência, PostgreSQL como banco de dados e WebSocket para sincronização do painel. O ambiente completo pode ser iniciado com Docker Compose.

## Funcionalidades

- Cadastro, consulta, edição e exclusão de clientes.
- Cadastro de produtos com preço e controle de estoque.
- Registro de vendas vinculadas a clientes e produtos.
- Atualização automática do estoque ao criar, editar ou excluir uma venda.
- Painel com totais de clientes, produtos, vendas e valor vendido.
- Autenticação com sessões persistidas e proteção CSRF.
- Atualização do painel em tempo real por WebSocket.
- Filtro de registros e interface responsiva.

## Tecnologias

| Área | Tecnologia |
| --- | --- |
| Backend | Python 3.12 e Bottle |
| ORM | SQLAlchemy 2 |
| Banco de dados | PostgreSQL 16 |
| Servidor | Uvicorn e ASGI |
| Tempo real | WebSocket |
| Frontend | HTML/TPL, CSS e JavaScript |
| Ambiente | Docker e Docker Compose |

## Início rápido com Docker

### 1. Clonar o repositório

```bash
git clone https://github.com/smacedo7/bmvc-project.git
cd bmvc-project
```

### 2. Iniciar a aplicação

```bash
docker compose up --build -d
```

O Compose inicia a aplicação e o PostgreSQL. O serviço web aguarda o banco ficar saudável antes de iniciar.

### 3. Criar o primeiro usuário

```bash
docker compose run --rm web python -m app.manage create-user
```

Informe o nome do usuário e uma senha com pelo menos oito caracteres.

### 4. Acessar

Abra [http://127.0.0.1:8080/login](http://127.0.0.1:8080/login) e entre com o usuário criado.

Para acompanhar os serviços:

```bash
docker compose ps
docker compose logs -f web
```

Para encerrar:

```bash
docker compose down
```

O banco fica armazenado em um volume Docker. Para remover também os dados locais, use `docker compose down -v`.

## Execução local

É possível executar o Python localmente e manter apenas o PostgreSQL no Docker:

```bash
docker compose up -d db

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"

alembic upgrade head
python -m app.manage create-user
python realtime.py
```

No Windows PowerShell, ative o ambiente com `.venv\Scripts\Activate.ps1` e defina a conexão com:

```powershell
$env:DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
```

## Como usar

1. Cadastre um cliente com nome e e-mail.
2. Cadastre um produto com preço e estoque disponível.
3. Registre uma venda selecionando cliente, produto e quantidade.
4. Acompanhe os indicadores no resumo administrativo.
5. Abra o resumo em outra aba para observar as atualizações em tempo real.

Uma venda guarda o preço vigente no momento do registro. Ao criar uma venda, a quantidade é retirada do estoque; ao editar, a diferença é ajustada; ao excluir, as unidades são devolvidas. Operações com estoque insuficiente são recusadas sem alterar os dados.

Clientes e produtos vinculados a vendas não podem ser excluídos enquanto houver dependências.

## Arquitetura

O código segue a divisão MVC usada pelo BMVC:

| Caminho | Responsabilidade |
| --- | --- |
| `route.py` | Rotas HTTP, validação da sessão e adaptação das requisições. |
| `app/controllers/application.py` | Coordenação dos casos de uso e preparação das páginas. |
| `app/models/entities.py` | Entidades e regras de domínio. |
| `app/models/repository.py` | Consultas e transações com SQLAlchemy. |
| `app/models/auth.py` | Autenticação, criação e encerramento de sessões. |
| `app/views/html/` | Templates da interface. |
| `app/static/` | CSS, JavaScript e imagens. |
| `app/realtime.py` | Distribuição de eventos em tempo real. |
| `realtime.py` | Entrada ASGI para HTTP e WebSocket. |
| `migrations/` | Histórico de alterações do banco gerenciado pelo Alembic. |

O servidor ASGI adapta a aplicação Bottle para HTTP e atende conexões WebSocket em `/ws`. Após uma alteração confirmada no banco, o painel recebe um evento e consulta `/api/resumo` para atualizar os indicadores.

## Segurança

- Senhas armazenadas com PBKDF2, salt individual e sem texto puro.
- Sessões com tokens aleatórios armazenados como hash.
- Cookies `HttpOnly` e `SameSite=Lax`.
- Validação CSRF em operações de escrita.
- Validação de sessão e origem no WebSocket.
- Serviços publicados apenas em `127.0.0.1` no ambiente local.

Para uma implantação com HTTPS, configure `BMVC_COOKIE_SECURE=1` e utilize um proxy reverso com TLS.

## Testes

Os testes de integração precisam de um banco PostgreSQL descartável cujo nome termine em `_test`:

```bash
docker compose exec db createdb -U bmvc bmvc_test

export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc_test"
export TEST_DATABASE_URL="$DATABASE_URL"

python -m unittest discover -s tests -v
```

Os testes recriam as tabelas do banco indicado por `TEST_DATABASE_URL`. Não utilize o banco principal da aplicação.

## Documentação

- [Manual completo de instalação e uso](docs/manual-de-uso.md)
- [UML do nível 1](docs/uml/nivel-1.md)
- [UML do nível 2](docs/uml/nivel-2.md)
- [UML do nível 3](docs/uml/nivel-3.md)
- [UML do nível 4](docs/uml/nivel-4.md)
- [Especificações técnicas](specs/)

## Origem

O projeto foi desenvolvido a partir da estrutura [BMVC](https://github.com/hgmachine/bmvc_start_from_this), preservando sua organização de rotas, controladores, modelos, templates e arquivos estáticos.
