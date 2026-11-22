# BMVC Gestão — ERP/CRM acadêmico

Sistema interno simples para cadastrar clientes e produtos, registrar vendas e acompanhar um resumo administrativo. O projeto foi construído em Python sobre a estrutura [BMVC fornecida pelo professor](https://github.com/hgmachine/bmvc_start_from_this). O planejamento está em `.specify/` e `specs/`, seguindo o [Spec Kit](https://github.com/github/spec-kit).

Repositório do trabalho: [smacedo7/bmvc-project](https://github.com/smacedo7/bmvc-project).

## Entregas por nível

| Nível | O que demonstrar | Branch congelada | Roteiro | Vídeo máximo |
| --- | --- | --- | --- | --- |
| BMVC I | Página estática própria com CSS e JS externos ativos | `video/nivel-1` | [Nível 1](docs/videos/nivel-1.md) | 3 min |
| BMVC II | Objetos Python e CRUD completo | `video/nivel-2` | [Nível 2](docs/videos/nivel-2.md) | 6 min |
| BMVC III | CRUD, login e área restrita | `video/nivel-3` | [Nível 3](docs/videos/nivel-3.md) | 10 min |
| BMVC IV | CRUD, login e atualização em tempo real por WebSocket | `video/nivel-4` | [Nível 4](docs/videos/nivel-4.md) | 15 min |

Os vídeos precisam ser gravados e publicados pelo estudante. Os roteiros em `docs/videos/` orientam a demonstração; este repositório não contém links de vídeos publicados.

O [manual de instalação e uso](docs/manual-de-uso.md) explica como executar cada branch e demonstrar suas funcionalidades. Os diagramas UML estão disponíveis por nível: [Nível 1](docs/uml/nivel-1.md), [Nível 2](docs/uml/nivel-2.md), [Nível 3](docs/uml/nivel-3.md) e [Nível 4](docs/uml/nivel-4.md).

## Branches e histórico

`main` é a versão completa e estável; `dev` é a integração. As branches `nivel/1-estatico`, `nivel/2-crud`, `nivel/3-login` e `nivel/4-websocket` registram a evolução. Cada `video/nivel-*` aponta para o commit exato planejado para a gravação correspondente. Para reproduzir uma etapa, execute `git switch video/nivel-1` (troque o número conforme o vídeo). Não grave um nível usando a branch de outro.

## Requisitos

- Para executar tudo em contêineres: Docker com Compose e porta **8080** disponível.
- Para executar Python diretamente: Python 3.11 ou superior e PostgreSQL 16 ou superior. `compose.yaml` pode fornecer apenas o banco na porta **5433**.
- As dependências Python estão em `requirements.txt`.

## Executar tudo com Docker Compose (BMVC IV)

Na branch `feat/docker-compose` (ou `main` após a integração do PR), na raiz do repositório:

```bash
docker compose up --build -d
docker compose run --rm web python -m app.manage create-user
docker compose ps
```

O primeiro comando constrói a imagem da aplicação, inicia PostgreSQL e espera o banco ficar saudável antes de iniciar o servidor. O segundo cria o primeiro usuário e pede a senha interativamente; rode-o apenas uma vez para cada usuário. Em seguida, abra [http://127.0.0.1:8080/login](http://127.0.0.1:8080/login). `docker compose logs -f web` mostra os logs e `docker compose down` para os contêineres **sem apagar** o volume do banco. O serviço `web` e o PostgreSQL estão publicados apenas em `127.0.0.1`.

Para repetir a demonstração em um banco novo, crie outro nome de volume ou remova o volume conscientemente. `docker compose down -v` **apaga os dados locais** do banco. A senha em `compose.yaml` é somente para desenvolvimento na própria máquina.

## Executar Python localmente (BMVC IV)

Na raiz do repositório:

```bash
docker compose up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python realtime.py
```

O comando `create-user` é necessário apenas para o primeiro usuário; ele pede nome e senha sem mostrar a senha digitada. Abra [http://127.0.0.1:8080/login](http://127.0.0.1:8080/login). Entre e navegue por Resumo, Clientes, Produtos e Vendas. Para demonstrar tempo real, abra o Resumo em uma aba e, em outra aba autenticada, cadastre ou altere uma venda. Os indicadores da primeira aba mudam sem F5.

Para os **níveis 1 a 3**, faça checkout da respectiva branch `video/nivel-*` e use `python route.py` no lugar de `python realtime.py`. O nível 1 requer somente Bottle e dispensa PostgreSQL. Os níveis 2 e 3 requerem `DATABASE_URL`; o nível 3 também exige `create-user`. As tabelas são criadas na primeira execução. Se usar PostgreSQL próprio, adapte a URL de `.env.example`. A branch `video/nivel-4` é o registro congelado antes da configuração do serviço `web` no Compose; use a branch `main` após a integração para executar os dois contêineres juntos. Não publique `.env` nem use a configuração de desenvolvimento como implantação pública.

## Funcionalidades e regras

- **Clientes:** criar, listar, consultar, editar e excluir. E-mail válido e único.
- **Produtos:** criar, listar, consultar, editar e excluir. Preço positivo, em centavos; estoque não negativo.
- **Vendas:** um cliente, um produto e uma quantidade por venda. Criar reduz o estoque; editar ajusta a quantidade; excluir devolve as unidades. A venda guarda o preço unitário vigente no momento do registro e calcula o total.
- **Integridade:** operação com estoque insuficiente falha sem modificar venda ou estoque. Clientes e produtos com vendas não podem ser excluídos.
- **Resumo:** contagens e valor histórico vendido. No nível 4, WebSocket avisa a página sobre alterações e `fetch('/api/resumo')` sincroniza os valores sem recarregar.
- **Acesso:** resumo e CRUD exigem login nos níveis 3 e 4. A senha usa PBKDF2 com salt; sessões têm token aleatório em cookie HttpOnly e SameSite=Lax, expiram em oito horas e são invalidadas ao sair. Formulários de alteração exigem CSRF.

## Como o BMVC foi usado

| Arquivo | Responsabilidade |
| --- | --- |
| `route.py` | Rotas Bottle e adaptação de requisições HTTP. |
| `app/controllers/application.py` | Coordena casos de uso e prepara os templates. |
| `app/models/entities.py` | Classes de domínio `Cliente`, `Produto`, `Venda`, `Usuario` e `Sessao`, com validações e comportamento. |
| `app/models/repository.py` | Consultas e transações SQLAlchemy/PostgreSQL. |
| `app/models/auth.py` | Autenticação e ciclo de vida da sessão. |
| `app/views/html/` | Páginas TPL. A página `helper.tpl` original foi preservada em `/helper`. |
| `app/static/css/` e `app/static/js/` | Estilo e interação carregados pelas páginas. |
| `app/realtime.py` e `realtime.py` | Hub WebSocket e servidor ASGI do nível 4. O HTTP continua sendo atendido pelo Bottle. |

O WebSocket atende `/ws`, valida cookie e origem e emite apenas um aviso de alteração. Os dados do resumo vêm de `/api/resumo`, que também exige login. O hub fica em memória e foi feito para **uma instância local**; vários processos exigiriam um canal compartilhado, como Redis.

## Testes

Crie um banco de teste **descartável** cujo nome termine em `_test`. Com o PostgreSQL do Compose:

```bash
docker compose exec db createdb -U bmvc bmvc_test
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc_test"
export TEST_DATABASE_URL="$DATABASE_URL"
python -m unittest discover -s tests -v
```

Os testes **apagam e recriam tabelas** nesse banco de teste. Nunca use o banco da aplicação para `TEST_DATABASE_URL`. A suíte cobre CRUD, validação, ajuste e reversão de estoque, login, CSRF, API e broadcast WebSocket. Para conferir o JavaScript, `node --check app/static/js/gestao.js` verifica a sintaxe. A demonstração visual e a gravação dos vídeos continuam sendo etapas manuais.

A configuração Docker foi verificada com a construção da imagem e a inicialização dos dois serviços. Os healthchecks de `web` e `db`, o login, `/api/resumo` e a conexão autenticada em `/ws` funcionaram no ambiente do Compose.

## Limites conhecidos

- Uma venda contém um produto; impostos, notas fiscais, fornecedores e múltiplos usuários simultâneos não foram incluídos.
- `Base.metadata.create_all()` cria tabelas ausentes, mas não migra tabelas já existentes. Mudanças futuras no esquema precisam de migrações.
- O servidor padrão escuta em `127.0.0.1`; para HTTPS em outro ambiente, configure uma implantação própria e `BMVC_COOKIE_SECURE=1`.

## Spec Kit

Cada nível tem `spec.md`, `plan.md` e `tasks.md` em `specs/`. A constituição fica em `.specify/memory/constitution.md`. A integração do Spec Kit neste repositório é a estrutura compartilhada (`none`), com templates e scripts oficiais; o trabalho de especificar, planejar, implementar e verificar foi aplicado em cada nível.
