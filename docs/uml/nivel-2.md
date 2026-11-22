# UML — Nível 2: CRUD com PostgreSQL

O segundo nível acrescenta os objetos de domínio e a persistência SQLAlchemy. `Venda` liga um `Cliente` a um `Produto` e preserva o preço unitário utilizado no momento do registro.

```mermaid
classDiagram
    class Application {
        -repositorio: Repositorio
        +inicio()
        +lista(area, erro)
        +formulario(area, id, erro, valores)
        +detalhe(area, id)
        +salvar(area, dados, id)
        +excluir(area, id)
    }

    class Repositorio {
        -engine
        +listar(classe)
        +obter(classe, id)
        +salvar_cliente(dados, id)
        +salvar_produto(dados, id)
        +salvar_venda(dados, id)
        +excluir(classe, id)
        +resumo()
    }

    class Cliente {
        +id: int
        +nome: str
        +email: str
        +atualizar(nome, email)
    }

    class Produto {
        +id: int
        +nome: str
        +preco_centavos: int
        +estoque: int
        +atualizar(nome, preco, estoque)
        +reservar(quantidade)
        +devolver(quantidade)
    }

    class Venda {
        +id: int
        +cliente_id: int
        +produto_id: int
        +quantidade: int
        +preco_unitario_centavos: int
        +criado_em: datetime
        +total_centavos: int
        +atualizar(cliente_id, produto, quantidade)
    }

    class PostgreSQL {
        <<database>>
    }

    Application --> Repositorio : coordena
    Repositorio --> Cliente : persiste
    Repositorio --> Produto : persiste
    Repositorio --> Venda : persiste
    Repositorio --> PostgreSQL : SQLAlchemy
    Cliente "1" <-- "0..*" Venda : comprador
    Produto "1" <-- "0..*" Venda : item
```

Transação de uma nova venda:

```mermaid
sequenceDiagram
    actor Operador
    participant Rota as route.py
    participant Controle as Application
    participant Repo as Repositorio
    participant Produto
    participant DB as PostgreSQL

    Operador->>Rota: POST /vendas/novo
    Rota->>Controle: salvar("vendas", dados)
    Controle->>Repo: salvar_venda(dados)
    Repo->>DB: bloqueia e carrega produto
    Repo->>Produto: reservar(quantidade)
    Produto-->>Repo: estoque reduzido
    Repo->>DB: INSERT venda + UPDATE produto
    DB-->>Repo: COMMIT
    Rota-->>Operador: redireciona para /vendas
```
