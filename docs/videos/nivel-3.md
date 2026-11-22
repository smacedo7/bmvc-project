# Roteiro do vídeo 3 — BMVC III

Tempo máximo: **10 minutos**. Objetivo: demonstrar CRUD completo, login e página de acesso restrito.

## Preparar o ambiente

```bash
git fetch origin
git switch video/nivel-3
git pull --ff-only origin video/nivel-3

docker compose -p bmvc_nivel3 up -d db

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python route.py
```

Crie um usuário como `apresentacao` e uma senha com pelo menos oito caracteres. Não mostre a senha durante a gravação.

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
$env:DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python route.py
```

Abra primeiro uma janela anônima em `http://127.0.0.1:8080/`. Deixe abertos `app/models/auth.py`, as classes `Usuario` e `Sessao` em `entities.py`, e o hook `proteger_rotas` em `route.py`.

## O que falar e mostrar

### 0:00–0:50 — Apresentação

> “O terceiro nível mantém o CRUD do ERP/CRM e acrescenta controle de acesso com usuário, senha, sessão e páginas restritas.”

Mostre brevemente Clientes, Produtos, Vendas e o Resumo.

### 0:50–1:50 — Proteção de acesso

Na janela anônima, tente abrir `/` e mostre o redirecionamento para `/login`. Tente uma senha incorreta e depois entre corretamente.

> “Sem uma sessão válida, o hook do Bottle redireciona qualquer área interna para o login.”

### 1:50–4:40 — CRUD completo

Faça o CRUD completo de um cliente sem vendas:

1. crie `Cliente Demonstração`;
2. consulte o detalhe;
3. edite nome ou e-mail;
4. exclua o registro.

Depois cadastre um cliente e produto permanentes, crie uma venda e mostre total e estoque.

### 4:40–6:20 — Implementação do login

Mostre `Usuario`, `Sessao` e `AuthService`.

> “A senha não é armazenada em texto puro. O sistema usa PBKDF2 com salt. O login cria um token aleatório, mas o banco guarda apenas o hash desse token.”

Mostre `entrar`, `identificar` e `sair`, sem abrir valores reais do banco, cookies ou senhas.

### 6:20–7:30 — Sessão e CSRF

Mostre `proteger_rotas` e um campo `_csrf` no formulário.

> “A sessão identifica o usuário em cada requisição e os formulários de escrita exigem um token CSRF.”

### 7:30–8:40 — Logout

Clique em **Sair** e tente voltar à página anterior ou abrir `/clientes`.

> “O logout remove a sessão do banco. Depois disso, a área volta a exigir autenticação.”

### 8:40–9:30 — CSS e JavaScript

Mostre o filtro de tabela, a confirmação de exclusão e a interface responsiva.

### 9:30–10:00 — Encerramento

Mostre o repositório público.

> “O projeto combina BMVC, objetos Python, CRUD completo e controle de acesso com página restrita.”

## Encerrar

```bash
# Depois de pressionar Ctrl+C na aplicação
deactivate
docker compose -p bmvc_nivel3 down
```

## Checklist

- Redirecionamento de visitante mostrado.
- Login correto e incorreto demonstrados.
- CRUD completo demonstrado.
- Página restrita mostrada.
- Logout e bloqueio posterior demonstrados.
- Vídeo com no máximo 10 minutos.
