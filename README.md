# BMVC Gestão — ERP/CRM acadêmico

Projeto de orientação a objetos em Python baseado no [BMVC fornecido pelo professor](https://github.com/hgmachine/bmvc_start_from_this). O objetivo é construir, em quatro níveis, um sistema interno simples para clientes, produtos, vendas e resumo administrativo. O planejamento está nos arquivos do [Spec Kit](https://github.com/github/spec-kit) em `.specify/` e `specs/`.

## Evolução por nível

| Nível | Entrega demonstrável | Vídeo |
| --- | --- | --- |
| BMVC I | Página estática própria, com CSS e JavaScript externos ativos | até 3 min |
| BMVC II | Modelos Python e CRUD completo em páginas BMVC | até 6 min |
| BMVC III | CRUD e controle de acesso com login e página restrita | até 10 min |
| BMVC IV | CRUD, login e atualização em tempo real por WebSocket | até 15 min |

Este checkout (`nivel/3-login`) contém o nível 3. As versões anteriores permanecem nas branches `video/nivel-1` e `video/nivel-2`. Veja `docs/videos/` para os roteiros.

## Executar o nível 3

Requer Python 3.11 ou superior, Docker com Compose ou PostgreSQL local e a porta 8080 livre. Na raiz do projeto:

```bash
docker compose up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python route.py
```

Abra `http://127.0.0.1:8080/login` e entre com o usuário criado. O resumo, os cadastros e as vendas exigem login. A aplicação cria as tabelas na primeira execução. Use os links Clientes, Produtos e Vendas para demonstrar o CRUD. A página original do BMVC permanece em `/helper`. Para PostgreSQL já instalado, crie um banco próprio e ajuste `DATABASE_URL`; o formato está em `.env.example`. A configuração do Compose contém credenciais **somente para desenvolvimento local**. Não a use em implantação pública.

## Organização BMVC

- `route.py`: servidor Bottle e rotas HTTP.
- `app/controllers/application.py`: controlador da renderização.
- `app/models/entities.py`: classes ORM e regras de domínio.
- `app/models/repository.py`: consultas e transações SQLAlchemy.
- `app/models/auth.py`: senha, sessão e validação de acesso.
- `app/manage.py`: criação local de usuários.
- `app/views/html/`: templates HTML/TPL.
- `app/static/css/` e `app/static/js/`: apresentação e interação.
- `specs/`: especificação, plano e tarefas de cada nível.
- `docs/videos/`: roteiros de demonstração.

## Branches e gravação

`main` guarda a base estável publicada; `dev` recebe a integração; `nivel/1-estatico` até `nivel/4-websocket` guardam a evolução de cada etapa. As branches `video/nivel-1` até `video/nivel-4` congelam o código mostrado em cada gravação. Antes de gravar, faça checkout da branch do vídeo correspondente. Cada alteração significativa recebe um commit descritivo.

## Origem e limites

A estrutura inicial (`route.py`, `app/`, `Dockerfile`) veio do repositório do professor. A aplicação, páginas e regras do ERP/CRM são próprias. O nível 1 apresenta módulos planejados. O nível 2 usa dados reais no PostgreSQL. Cada venda contém um produto. O nível 3 adiciona login e sessão; execute em `127.0.0.1` no ambiente local. Para usar HTTPS em outro ambiente, configure `BMVC_COOKIE_SECURE=1` e uma implantação apropriada. O vídeo e seu envio ao YouTube são feitos pelo estudante.

## Regras e testes do nível 2

Clientes e produtos com vendas não podem ser excluídos. A venda guarda o preço no momento do registro. Criar, editar e excluir uma venda ajusta o estoque numa transação; uma tentativa inválida não altera os dados. Para rodar os testes, crie um banco **descartável** cujo nome termine em `_test` e informe sua URL:

```bash
export TEST_DATABASE_URL="postgresql+psycopg:///bmvc_test"
python -m unittest discover -s tests -v
```

Os testes apagam e recriam as tabelas nesse banco de teste. Não use o banco da aplicação. O projeto ainda não inclui migrações de esquema; para mudanças futuras, será preciso adicionar um processo de migração.

## Controle de acesso do nível 3

O comando `create-user` pede a senha sem exibi-la no terminal; o banco guarda um hash PBKDF2 com salt, nunca a senha original. A sessão usa token aleatório em cookie HttpOnly e SameSite=Lax e expira após oito horas. Formulários de alteração exigem CSRF. A página `/helper` do framework e os arquivos estáticos continuam públicos. O botão “Sair” invalida a sessão no banco.
