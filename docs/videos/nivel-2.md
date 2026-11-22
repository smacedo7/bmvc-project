# Roteiro do vídeo 2 — BMVC II

Tempo máximo: **6 minutos**. Objetivo: demonstrar objetos Python e CRUD completo servido em páginas BMVC.

## Preparar o ambiente

```bash
git fetch origin
git switch video/nivel-2
git pull --ff-only origin video/nivel-2

docker compose -p bmvc_nivel2 up -d db

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python route.py
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
$env:DATABASE_URL="postgresql+psycopg://bmvc:bmvc_local@127.0.0.1:5433/bmvc"
python route.py
```

Abra `http://127.0.0.1:8080/`. Prepare estes dados antes ou durante a gravação:

- cliente da venda: `Ana Souza`, `ana@example.com`;
- cliente do CRUD: `Cliente Teste`, `teste@example.com`;
- produto: `Caderno Executivo`, preço `25,90`, estoque `10`.

Deixe abertos `app/models/entities.py`, `app/models/repository.py`, `app/controllers/application.py` e `route.py`.

## O que falar e mostrar

### 0:00–0:30 — Contexto

> “No segundo nível, o BMVC Gestão passa a trabalhar com objetos Python persistidos em PostgreSQL. O sistema possui clientes, produtos, vendas e resumo administrativo.”

### 0:30–1:10 — Modelos e arquitetura

Mostre as classes `Cliente`, `Produto` e `Venda` em `entities.py`.

> “As classes representam as entidades do domínio. Produto controla o estoque, Venda calcula o total e o repositório executa as transações com SQLAlchemy.”

Mostre rapidamente `Repositorio.salvar_cliente`, `salvar_produto` e `salvar_venda`.

### 1:10–2:35 — CRUD completo de cliente

Use `Cliente Teste` para demonstrar as quatro operações:

1. crie o cliente;
2. abra **Ver**;
3. edite o nome para `Cliente Atualizado`;
4. volte à lista e exclua o registro.

> “Aqui estão Create, Read, Update e Delete funcionando sobre o mesmo modelo.”

### 2:35–3:30 — Produto

Cadastre `Caderno Executivo`, preço `25,90` e estoque `10`. Mostre o detalhe e a listagem.

> “O preço é convertido para centavos e o estoque aceita somente valores inteiros não negativos.”

### 3:30–4:50 — Venda e estoque

Cadastre `Ana Souza` e crie uma venda de 2 cadernos. Mostre:

- total de `R$ 51,80`;
- estoque reduzido de 10 para 8;
- indicadores atualizados no resumo.

Edite a quantidade para 3 e mostre o estoque em 7. Exclua a venda e mostre o estoque voltando para 10.

> “A criação reserva estoque, a edição ajusta a diferença e a exclusão devolve as unidades. Tudo ocorre na mesma transação.”

### 4:50–5:25 — Regras de negócio

Tente criar uma venda com quantidade maior que o estoque ou tente excluir um cliente que ainda possua venda.

> “As regras impedem estoque negativo e preservam os relacionamentos existentes.”

### 5:25–6:00 — CSS, JS e encerramento

Use o filtro da tabela e mostre a confirmação de exclusão.

> “As páginas carregam CSS e JavaScript externos, e o código completo está no repositório público.”

## Encerrar

```bash
# Depois de pressionar Ctrl+C na aplicação
deactivate
docker compose -p bmvc_nivel2 down
```

O comando `down` preserva o volume do banco desse nível.

## Checklist

- Classes Python mostradas.
- CRUD completo do mesmo modelo demonstrado.
- PostgreSQL e SQLAlchemy mencionados.
- CSS e JavaScript ativos.
- Vídeo com no máximo 6 minutos.
