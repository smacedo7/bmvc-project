# UML — Nível 2: CRUD com PostgreSQL

O segundo nível acrescenta objetos de domínio e persistência SQLAlchemy. `Venda` liga um `Cliente` a um `Produto` e preserva o preço unitário usado no registro.

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

## Leitura do diagrama

`Application` não executa SQL diretamente. Ela solicita operações ao `Repositorio`, que abre a transação e persiste os objetos. As associações indicam que cada venda referencia exatamente um cliente e um produto, enquanto ambos podem possuir várias vendas.

## Transação de uma venda

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

O bloqueio evita que duas operações concorrentes vendam as mesmas últimas unidades. O `COMMIT` garante que venda e estoque sejam confirmados juntos.
