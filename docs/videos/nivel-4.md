# Roteiro do vídeo 4 — BMVC IV

Tempo máximo: **15 minutos**. Objetivo: demonstrar CRUD, login, página restrita e atualização assíncrona em tempo real por WebSocket.

## Preparar o ambiente

Para reproduzir exatamente a etapa do nível 4:

```bash
git fetch origin
git switch video/nivel-4
git pull --ff-only origin video/nivel-4

docker compose -p bmvc_nivel4 up -d db

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python realtime.py
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
$env:DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python realtime.py
```

Use `realtime.py`, pois `route.py` não inicia o endpoint WebSocket.

Abra duas abas autenticadas:

- **Aba A:** `http://127.0.0.1:8080/`, com o resumo visível;
- **Aba B:** `http://127.0.0.1:8080/vendas`.

Deixe abertos `realtime.py`, `app/realtime.py`, `app/static/js/gestao.js`, `app/models/auth.py` e `app/models/repository.py`.

## O que falar e mostrar

### 0:00–1:00 — Visão geral

> “O BMVC Gestão é um ERP/CRM simples para clientes, produtos e vendas. O quarto nível reúne CRUD, autenticação, área restrita e atualização em tempo real por WebSocket.”

Mostre o resumo e a navegação.

### 1:00–2:30 — Arquitetura

Mostre a estrutura de pastas e explique:

- `route.py` contém rotas Bottle;
- `Application` coordena os casos de uso;
- `entities.py` contém os objetos;
- `repository.py` usa SQLAlchemy e PostgreSQL;
- `realtime.py` combina HTTP e WebSocket no servidor ASGI.

### 2:30–4:00 — Login e restrição

Abra uma janela anônima, tente acessar `/` e mostre o login. Entre corretamente e mostre a página restrita.

> “O handshake do WebSocket também verifica a mesma sessão usada pelas páginas HTTP.”

### 4:00–7:20 — CRUD completo

Faça o CRUD completo de um cliente sem vendas. Em seguida:

1. cadastre um cliente permanente;
2. cadastre um produto com estoque 10;
3. crie uma venda de quantidade 2;
4. mostre o total e o estoque 8;
5. edite a venda para quantidade 3;
6. exclua a venda e confirme a devolução do estoque.

### 7:20–10:20 — WebSocket em tempo real

Mantenha a Aba A no resumo e use a Aba B para criar uma venda.

Mostre na Aba A:

- a mensagem **Tempo real conectado**;
- a quantidade de vendas mudando;
- o valor vendido mudando;
- nenhuma atualização manual com F5.

Repita com edição ou exclusão para deixar o comportamento evidente.

> “Depois que a transação termina, a aplicação publica `dados-atualizados`. O navegador recebe o evento pelo WebSocket e consulta `/api/resumo` para buscar os valores atuais.”

### 10:20–12:20 — Código do tempo real

Mostre `ServidorBMVC.websocket`, a classe `Hub` e o trecho JavaScript que cria `new WebSocket`.

Explique:

- validação do cookie e da origem;
- registro da conexão no hub;
- envio do aviso;
- reconexão automática no navegador.

### 12:20–13:30 — Segurança e sessão

Mostre `AuthService` e o token CSRF sem revelar credenciais.

> “Senhas usam hash com salt, sessões guardam o hash do token, cookies são HttpOnly e operações de escrita exigem CSRF.”

### 13:30–14:20 — Logout

Saia do sistema e mostre que a área restrita volta ao login. Explique que a conexão em tempo real deixa de ser autorizada após o fim da sessão.

### 14:20–15:00 — Encerramento

Mostre o repositório público e a documentação.

> “A aplicação final combina BMVC, orientação a objetos, CRUD, PostgreSQL, autenticação e atualização assíncrona por WebSocket.”

## Opção com o Compose completo

Depois da integração da configuração Docker à `main`, todo o ambiente pode ser iniciado assim:

```bash
git switch main
git pull --ff-only
cp .env.example .env
docker compose up --build -d
docker compose run --rm web python -m app.manage create-user
docker compose ps
```

Nessa opção, o contêiner aplica `alembic upgrade head` automaticamente antes de iniciar a aplicação.

## Encerrar

Na execução local:

```bash
# Depois de pressionar Ctrl+C na aplicação
deactivate
docker compose -p bmvc_nivel4 down
```

Na execução completa por Compose:

```bash
docker compose down
```

## Checklist

- CRUD completo demonstrado.
- Login e página restrita demonstrados.
- Duas abas abertas.
- Indicadores atualizados sem F5.
- Status “Tempo real conectado” visível.
- CSS e JavaScript externos mostrados.
- Repositório público apresentado.
- Vídeo com no máximo 15 minutos.
