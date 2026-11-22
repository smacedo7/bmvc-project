# Apresentação do Nível 2 — BMVC II

Tempo máximo: **6 minutos**. Planejamento: **5 minutos e 45 segundos**.

## O que foi implementado

O Nível 2 transforma a página conceitual em um sistema com objetos Python e persistência. Foram implementados `Cliente`, `Produto` e `Venda`, páginas TPL para listar, cadastrar, consultar, editar e excluir registros, além de PostgreSQL acessado por SQLAlchemy.

```text
Navegador -> rotas Bottle -> Application -> Repositorio -> PostgreSQL
                                      -> templates TPL
```

- `Cliente` armazena nome e e-mail.
- `Produto` armazena preço em centavos e controla o estoque.
- `Venda` relaciona cliente e produto, registra quantidade e calcula o total.
- `Repositorio` concentra consultas, transações e regras de persistência.
- `Application` coordena formulários, validações, repositório e templates.

Ao criar uma venda, o estoque diminui. Ao editar, a diferença é ajustada. Ao excluir, as unidades são devolvidas. Cliente ou produto relacionado a venda não pode ser removido, preservando a integridade dos dados.

## Como explicar a UML

Abra [`docs/uml/nivel-2.md`](../uml/nivel-2.md).

- `Application` coordena os casos de uso da interface.
- `Repositorio` isola a persistência e usa SQLAlchemy para acessar PostgreSQL.
- `Cliente`, `Produto` e `Venda` são classes de domínio e tabelas mapeadas.
- Um cliente pode ter várias vendas; cada venda possui um cliente.
- Um produto pode aparecer em várias vendas; cada venda possui um produto.
- `1` e `0..*` expressam “um para zero ou muitos”.

No diagrama de sequência, uma nova venda passa pela rota e pelo controlador. O repositório carrega o produto, chama `reservar`, insere a venda e atualiza o estoque na mesma transação. O `COMMIT` confirma as duas alterações juntas.

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

Abra `http://127.0.0.1:8080/`. Prepare um cliente sem vendas para demonstrar exclusão, outro cliente para a venda e um produto com estoque 10.

## Roteiro cronometrado

| Tempo | Mostrar | Fala sugerida |
|---|---|---|
| 0:00–0:30 | Resumo e navegação | “No segundo nível, o BMVC Gestão passa a trabalhar com objetos Python persistidos em PostgreSQL. O sistema administra clientes, produtos e vendas e apresenta indicadores no resumo.” |
| 0:30–1:05 | UML de classes | “Application coordena a interface e utiliza o Repositorio. Cliente, Produto e Venda representam o domínio. Venda associa um cliente a um produto e Produto encapsula as operações de reservar e devolver estoque.” |
| 1:05–1:25 | UML de sequência | “Ao salvar uma venda, o repositório carrega e bloqueia o produto, reserva a quantidade e grava a venda e o estoque na mesma transação.” |
| 1:25–2:40 | CRUD de cliente | “Vou demonstrar as quatro operações sobre o mesmo modelo: criar, consultar, editar e excluir este cliente. Os dados são realmente persistidos no PostgreSQL.” |
| 2:40–3:25 | Cadastro de produto | “O produto possui nome, preço armazenado em centavos e estoque inteiro não negativo. O formulário valida os dados antes da persistência.” |
| 3:25–4:40 | Criar, editar e excluir venda | “Ao vender duas unidades, o total é calculado e o estoque cai de dez para oito. Ao alterar a quantidade, o sistema ajusta somente a diferença; ao excluir, devolve as unidades.” |
| 4:40–5:10 | Regra inválida | “O domínio impede estoque negativo e o repositório protege os relacionamentos, evitando excluir um cliente ou produto que participa de uma venda.” |
| 5:10–5:35 | Código de entidades e repositório | “As regras ficam nos objetos e a persistência fica no Repositorio. Essa separação reduz o acoplamento entre a interface e o banco.” |
| 5:35–5:45 | CSS, JS e repositório | “As páginas continuam utilizando CSS e JavaScript externos, e a implementação completa está disponível no repositório público.” |

## Perguntas prováveis

**O que significa CRUD?**

Create, Read, Update e Delete: criar, consultar, editar e excluir.

**Por que guardar o preço em centavos?**

Para evitar imprecisão de ponto flutuante em valores monetários. `2590` representa R$ 25,90.

**Por que existe um repositório?**

Para centralizar consultas e transações, sem misturar SQLAlchemy com as rotas e templates.

**O que acontece se faltar estoque?**

`Produto.reservar()` rejeita a operação. A transação não é confirmada e nenhuma venda parcial é gravada.

**Qual é a relação entre as entidades?**

Cada venda pertence a um cliente e a um produto; clientes e produtos podem participar de várias vendas.

## Encerrar e conferir

```bash
# depois de Ctrl+C
deactivate
docker compose -p bmvc_nivel2 down
```

- CRUD completo do mesmo modelo demonstrado.
- PostgreSQL e SQLAlchemy explicados.
- Cálculo, estoque e validação mostrados.
- CSS e JavaScript ativos.
- Vídeo com no máximo 6 minutos.
