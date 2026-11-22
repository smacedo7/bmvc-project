# Apresentação do Nível 3 — BMVC III

Tempo máximo: **10 minutos**. Planejamento: **9 minutos e 40 segundos**.

## O que foi implementado

O Nível 3 mantém o CRUD de clientes, produtos e vendas e acrescenta autenticação e área restrita. Foram implementados usuário, senha protegida por hash e salt, sessão persistida, cookie, logout e proteção CSRF para formulários.

```text
Requisição -> hook de proteção -> AuthService -> Sessao/Usuario -> área restrita
```

- `Usuario` representa a conta e armazena salt e hash, nunca a senha original.
- `Sessao` relaciona o usuário a um token, CSRF e data de expiração.
- `AuthService` cria usuário, autentica, identifica a sessão e realiza logout.
- O hook Bottle protege as rotas internas antes de executar o controlador.
- Operações de escrita exigem o token CSRF da sessão.

## Como explicar a UML

Abra [`docs/uml/nivel-3.md`](../uml/nivel-3.md).

- `Application` continua usando `Repositorio` para o CRUD e passa a receber a identidade e o CSRF.
- `AuthService` é responsável pela autenticação, separado do CRUD comercial.
- A composição entre `Usuario` e `Sessao` mostra que uma sessão existe vinculada a um usuário.
- Um usuário pode possuir zero ou várias sessões.

No fluxo protegido, o hook recebe o cookie, pede ao `AuthService` que identifique o token e consulta usuário e sessão. Se forem válidos, a requisição continua. Caso contrário, o navegador recebe redirecionamento para `/login`.

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

Crie um usuário de apresentação com senha de pelo menos oito caracteres. Não exiba a senha, o cookie ou tokens durante a gravação. Abra uma janela anônima em `http://127.0.0.1:8080/`.

## Roteiro cronometrado

| Tempo | Mostrar | Fala sugerida |
|---|---|---|
| 0:00–0:40 | Página e módulos | “O terceiro nível mantém o ERP/CRM com clientes, produtos, vendas e resumo e acrescenta controle de acesso com usuário, senha, sessão e páginas restritas.” |
| 0:40–1:20 | UML de classes | “AuthService concentra as operações de autenticação. Usuario guarda o hash da senha, e Sessao relaciona um usuário a um token protegido, CSRF e expiração.” |
| 1:20–1:45 | UML de sequência | “Antes de uma rota interna ser executada, o hook identifica a sessão. Uma sessão válida libera a página; uma sessão ausente ou expirada redireciona para o login.” |
| 1:45–2:35 | Janela anônima e login | “Sem autenticação, a aplicação impede o acesso ao resumo e redireciona para o login. Uma senha incorreta é rejeitada; com as credenciais corretas, a sessão é criada.” |
| 2:35–5:20 | CRUD completo | “Dentro da área restrita, vou criar, consultar, editar e excluir o mesmo cliente. O sistema continua oferecendo também produtos, vendas, cálculo de total e controle de estoque.” |
| 5:20–6:35 | `Usuario`, `Sessao` e `AuthService` | “A senha não é salva em texto puro. PBKDF2 utiliza um salt para gerar o hash. O navegador recebe um token aleatório, mas o banco guarda apenas o hash desse token.” |
| 6:35–7:20 | Hook e formulário com CSRF | “O hook protege as rotas antes do controlador. Nas operações de escrita, o formulário envia um CSRF que precisa corresponder ao valor da sessão.” |
| 7:20–8:10 | Logout e tentativa de retorno | “Ao sair, a sessão é removida do banco. Mesmo tentando voltar ou acessar `/clientes` diretamente, o sistema exige uma nova autenticação.” |
| 8:10–9:05 | CSS e JavaScript | “O filtro das tabelas e a confirmação de exclusão demonstram o JavaScript externo, enquanto o CSS mantém a interface legível e responsiva.” |
| 9:05–9:40 | Repositório e encerramento | “O projeto reúne BMVC, orientação a objetos, PostgreSQL, CRUD completo e controle de acesso. O código e a documentação estão neste repositório público.” |

## Perguntas prováveis

**A senha fica salva no banco?**

Não. O banco guarda salt e hash produzidos com PBKDF2. O texto original não é recuperável.

**O que é uma sessão?**

É um registro temporário que relaciona uma autenticação válida ao usuário e possui expiração.

**Por que o banco guarda o hash do token?**

Para reduzir o impacto de um vazamento do banco: o valor utilizável pelo navegador não fica armazenado diretamente.

**O que é CSRF?**

É uma proteção contra formulários maliciosos enviados por outro site em nome de um usuário autenticado.

**Onde a rota é protegida?**

No hook do Bottle, executado antes das rotas internas. Ele consulta o `AuthService` e decide continuar ou redirecionar.

## Encerrar e conferir

```bash
# depois de Ctrl+C
deactivate
docker compose -p bmvc_nivel3 down
```

- Visitante redirecionado ao login.
- Login incorreto e correto demonstrados.
- CRUD completo demonstrado.
- Página restrita, CSRF e logout explicados.
- Vídeo com no máximo 10 minutos.
