# Manual de instalação e uso

Este manual explica como executar e demonstrar cada etapa do BMVC Gestão. Antes de começar, clone o repositório e entre na pasta:

```bash
git clone https://github.com/smacedo7/bmvc-project.git
cd bmvc-project
```

## Escolher o nível

Cada vídeo possui uma branch congelada. Trocar de nível também troca os arquivos, dependências e funcionalidades disponíveis.

| Nível | Branch | Funcionalidade principal | Inicialização |
| --- | --- | --- | --- |
| 1 | `video/nivel-1` | Página estática com CSS e JavaScript | `python route.py` |
| 2 | `video/nivel-2` | CRUD com PostgreSQL | `python route.py` |
| 3 | `video/nivel-3` | CRUD, login e área restrita | `python route.py` |
| 4 | `video/nivel-4` | CRUD, login e WebSocket | `python realtime.py` |
| Projeto completo | `main` após a integração do PR Docker | Nível 4 com aplicação e banco no Compose | `docker compose up --build -d` |

Para selecionar uma etapa:

```bash
git switch video/nivel-1
```

Substitua o número pelo nível desejado.

## Nível 1 — página estática

### Instalar e iniciar

```bash
git switch video/nivel-1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python route.py
```

Abra `http://127.0.0.1:8080/`. A página apresenta o propósito do ERP/CRM e os módulos Clientes, Produtos, Vendas e Resumo administrativo.

### O que conferir

1. Digite “clientes” na busca e confirme que os cartões são filtrados sem recarregar a página.
2. Digite um termo inexistente e confira a mensagem de nenhum resultado.
3. Redimensione a janela e confira o layout responsivo.
4. Abra `/helper` para mostrar que a página original do framework foi preservada.

## Nível 2 — CRUD completo

### Iniciar o PostgreSQL

```bash
git switch video/nivel-2
docker compose up -d db
```

### Instalar e iniciar a aplicação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python route.py
```

Abra `http://127.0.0.1:8080/`.

### Ordem recomendada de uso

1. Em **Clientes**, cadastre nome e e-mail.
2. Em **Produtos**, cadastre nome, preço e estoque.
3. Em **Vendas**, selecione cliente, produto e quantidade.
4. Confira no resumo o número de registros e o valor vendido.
5. Edite a venda e observe o ajuste do estoque.
6. Exclua a venda e observe a devolução das unidades ao estoque.

Clientes e produtos associados a vendas não podem ser excluídos. Para demonstrar o CRUD completo, crie um cliente separado, consulte, edite e exclua esse registro antes de vinculá-lo a uma venda.

## Nível 3 — login e área restrita

### Iniciar banco e aplicação

```bash
git switch video/nivel-3
docker compose up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python route.py
```

O comando `create-user` pede nome, senha e confirmação. A senha deve ter pelo menos oito caracteres.

Abra `http://127.0.0.1:8080/login` e entre com o usuário criado.

### O que conferir

1. Abra `/` em uma janela anônima e confirme o redirecionamento para `/login`.
2. Tente uma senha incorreta e confira a mensagem de erro.
3. Entre e use Clientes, Produtos e Vendas normalmente.
4. Clique em **Sair** e confirme que a área interna voltou a exigir autenticação.

## Nível 4 — atualização em tempo real

### Executar a branch congelada do vídeo

```bash
git switch video/nivel-4
docker compose up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python -m app.manage create-user
python realtime.py
```

### Demonstrar o WebSocket

1. Entre no sistema e deixe o **Resumo administrativo** aberto na primeira aba.
2. Abra uma segunda aba autenticada e acesse Clientes, Produtos ou Vendas.
3. Cadastre, edite ou exclua um registro.
4. Volte à primeira aba e confirme que os indicadores mudaram sem pressionar F5.
5. Confira a mensagem **Tempo real conectado** abaixo dos indicadores.

## Projeto completo com Docker Compose

Depois que o PR Docker estiver integrado à `main`, a aplicação e o banco podem ser iniciados juntos:

```bash
git switch main
git pull
docker compose up --build -d
docker compose run --rm web python -m app.manage create-user
docker compose ps
```

Abra `http://127.0.0.1:8080/login`. Os serviços `web` e `db` devem aparecer como `healthy`.

Comandos úteis:

```bash
docker compose logs -f web
docker compose stop
docker compose start
docker compose down
```

`docker compose down` preserva o volume do PostgreSQL. `docker compose down -v` remove também o banco local e todos os dados; use esse último comando apenas quando quiser recomeçar.

## Problemas comuns

### A porta já está ocupada

Encerre a aplicação ou contêiner que já usa as portas 8080 ou 5433. Confira os contêineres com:

```bash
docker compose ps
```

### A aplicação informa que `DATABASE_URL` não foi configurada

Execute novamente o `export DATABASE_URL=...` no mesmo terminal em que iniciará `route.py` ou `realtime.py`.

### O login não funciona

Crie o usuário no mesmo banco usado pela aplicação. Na execução local, mantenha `DATABASE_URL` configurada antes de rodar `python -m app.manage create-user`. No Compose completo, use `docker compose run --rm web python -m app.manage create-user`.

### O tempo real aparece desconectado

No nível 4, inicie com `python realtime.py`. `python route.py` serve as páginas Bottle, mas não cria o endpoint WebSocket `/ws`.

## Encerrar a demonstração

Para execução local, pressione `Ctrl+C`. Para execução com Compose:

```bash
docker compose down
```

Os roteiros de gravação ficam em `docs/videos/` e os diagramas UML em `docs/uml/`.
