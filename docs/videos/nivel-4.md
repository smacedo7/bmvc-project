# Apresentação do Nível 4 — BMVC IV

Tempo máximo: **15 minutos**. Planejamento: **14 minutos e 35 segundos**.

## O que foi implementado

O Nível 4 reúne página personalizada, CRUD, PostgreSQL, login e área restrita e acrescenta comunicação WebSocket. Quando um registro é alterado, outras abas autenticadas recebem um aviso e atualizam o resumo sem utilizar F5.

```text
Aba B altera dados -> Application -> Repositorio -> COMMIT
                            |
                            v
                           Hub -> WebSocket -> Aba A -> GET /api/resumo
```

- `ServidorBMVC` combina as rotas HTTP do Bottle com o endpoint WebSocket `/ws`.
- `Hub` registra conexões e distribui o evento `dados-atualizados`.
- `Application` publica o evento somente depois da transação bem-sucedida.
- O JavaScript recebe o aviso e consulta `/api/resumo` para obter os valores atuais.
- O handshake verifica sessão e origem antes de aceitar a conexão.

O WebSocket não envia todo o banco: ele funciona como aviso. Depois do aviso, a página busca um resumo novo por HTTP. Essa separação mantém a fonte dos dados no servidor e simplifica o evento.

## Como explicar a UML

Abra [`docs/uml/nivel-4.md`](../uml/nivel-4.md).

- `ServidorBMVC` decide se a conexão é HTTP ou WebSocket.
- Para HTTP, ele adapta a aplicação WSGI Bottle por meio de `WsgiToAsgi`.
- Para `/ws`, valida a sessão com `AuthService` e registra a conexão no `Hub`.
- `Application` continua coordenando o repositório e publica após a confirmação no banco.
- `Hub` mantém as filas dos clientes conectados e entrega o aviso.

No diagrama de sequência, a Aba A conecta ao WebSocket. A Aba B salva ou exclui um registro. Depois do `COMMIT`, o evento chega à Aba A, que chama `/api/resumo` e modifica os indicadores sem recarregar a página inteira.

## Preparar o ambiente

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

Use `realtime.py`, pois `route.py` sozinho não inicia o endpoint WebSocket. Abra duas abas autenticadas:

- Aba A: `http://127.0.0.1:8080/`, com o resumo;
- Aba B: `http://127.0.0.1:8080/vendas`.

Deixe visível o estado **Tempo real conectado**. Não exponha senhas, cookies ou tokens.

## Roteiro cronometrado

| Tempo | Mostrar | Fala sugerida |
|---|---|---|
| 0:00–0:50 | Resumo do sistema | “O BMVC Gestão é um ERP e CRM simples para clientes, produtos e vendas. O quarto nível reúne CRUD, autenticação, área restrita e atualização em tempo real por WebSocket.” |
| 0:50–1:50 | UML de classes | “ServidorBMVC adapta as rotas HTTP do Bottle e também atende `/ws`. AuthService valida a sessão, Hub administra as conexões e Application publica avisos após alterações confirmadas.” |
| 1:50–2:30 | UML de sequência | “A Aba A mantém a conexão. Quando a Aba B confirma uma alteração, o Hub envia `dados-atualizados`. A Aba A consulta `/api/resumo` e substitui os indicadores sem F5.” |
| 2:30–3:30 | Login e área restrita | “A aplicação mantém o controle de acesso do nível anterior. Visitantes são redirecionados, e até o handshake do WebSocket exige uma sessão válida.” |
| 3:30–6:30 | CRUD completo | “Vou criar, consultar, editar e excluir o mesmo cliente. Em seguida, cadastro produto e venda para demonstrar total, reserva de estoque e transação no PostgreSQL.” |
| 6:30–9:30 | Duas abas e WebSocket | “A Aba A está conectada ao tempo real. Na Aba B, vou criar uma venda. Sem atualizar manualmente, quantidade e valor vendido mudam na Aba A. O mesmo ocorre ao editar ou excluir.” |
| 9:30–11:10 | `ServidorBMVC` e `Hub` | “O servidor diferencia HTTP de WebSocket. Após validar sessão e origem, registra uma fila no Hub. O Hub distribui um aviso para cada conexão ativa.” |
| 11:10–12:15 | JavaScript e `/api/resumo` | “O JavaScript recebe o evento e realiza uma busca assíncrona no endpoint de resumo. O WebSocket avisa que houve alteração; a API fornece os dados atuais.” |
| 12:15–13:10 | Segurança | “A conexão reutiliza a autenticação, valida a origem e não é aceita sem sessão. Formulários continuam protegidos por CSRF, e senhas e tokens não ficam armazenados em texto puro.” |
| 13:10–13:50 | Logout | “Ao sair, a sessão é invalidada. As páginas internas e uma nova conexão WebSocket voltam a exigir autenticação.” |
| 13:50–14:35 | Repositório e encerramento | “A versão final combina BMVC, orientação a objetos, CRUD, PostgreSQL, autenticação e atualização assíncrona em tempo real. O código e a documentação estão neste repositório público.” |

## Perguntas prováveis

**Qual é a diferença entre HTTP e WebSocket?**

No HTTP tradicional, o cliente faz uma requisição e recebe uma resposta. O WebSocket mantém uma conexão aberta e permite ao servidor enviar eventos quando necessário.

**Por que buscar `/api/resumo` depois do evento?**

O evento é apenas um aviso. A API continua sendo a fonte dos valores atuais, evitando duplicar todos os dados dentro da mensagem WebSocket.

**Por que publicar somente depois do `COMMIT`?**

Para não avisar os navegadores sobre uma alteração que pode falhar ou ser desfeita no banco.

**Como o WebSocket é protegido?**

O handshake valida o cookie de sessão e a origem antes de aceitar a conexão.

**O que ocorre se a conexão cair?**

O JavaScript agenda uma tentativa de reconexão. Enquanto isso, a aplicação HTTP continua funcionando.

## Opção com o Compose completo

Na branch com a integração Docker, todo o ambiente pode ser iniciado assim:

```bash
cp .env.example .env
docker compose up --build -d
docker compose run --rm web python -m app.manage create-user
docker compose ps
```

## Encerrar e conferir

```bash
# execução local, depois de Ctrl+C
deactivate
docker compose -p bmvc_nivel4 down
```

- CRUD completo, login e página restrita demonstrados.
- Duas abas abertas e status conectado visível.
- Indicadores atualizados sem F5.
- WebSocket, Hub e consulta assíncrona explicados.
- Vídeo com no máximo 15 minutos.
