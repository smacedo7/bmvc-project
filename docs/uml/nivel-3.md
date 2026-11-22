# UML — Nível 3: autenticação e área restrita

O terceiro nível mantém as classes comerciais e acrescenta `Usuario`, `Sessao` e `AuthService`. A senha é representada por salt e hash; a sessão armazena o hash do token e um token CSRF.

```mermaid
classDiagram
    class Application {
        -repositorio: Repositorio
        +auth: AuthService
        +csrf: str
        +usuario: Usuario
        +salvar(area, dados, id)
        +excluir(area, id)
    }
    class Repositorio {
        +listar(classe)
        +salvar_cliente(dados, id)
        +salvar_produto(dados, id)
        +salvar_venda(dados, id)
    }
    class AuthService {
        -engine
        +criar_usuario(nome, senha)
        +entrar(nome, senha) str
        +identificar(token)
        +sair(token)
        -_hash_token(token)
    }
    class Usuario {
        +id: int
        +nome: str
        +senha_salt: str
        +senha_hash: str
    }
    class Sessao {
        +id: int
        +usuario_id: int
        +token_hash: str
        +csrf_token: str
        +expira_em: datetime
    }
    class Cliente
    class Produto
    class Venda

    Application --> Repositorio
    Application --> AuthService
    AuthService --> Usuario : autentica
    AuthService --> Sessao : cria e invalida
    Usuario "1" *-- "0..*" Sessao
    Repositorio --> Cliente
    Repositorio --> Produto
    Repositorio --> Venda
```

## Leitura do diagrama

O losango preenchido em `Usuario *-- Sessao` representa composição: a sessão pertence a um usuário. O `AuthService` concentra segurança e ciclo de vida da sessão; o `Repositorio` continua responsável pelo domínio comercial.

## Fluxo de acesso protegido

```mermaid
sequenceDiagram
    actor Operador
    participant Rota as Hook Bottle
    participant Auth as AuthService
    participant DB as PostgreSQL
    participant Area as Área restrita

    Operador->>Rota: GET /clientes + cookie
    Rota->>Auth: identificar(token)
    Auth->>DB: busca Sessao e Usuario
    alt sessão válida
        DB-->>Auth: usuário + CSRF
        Auth-->>Rota: identidade
        Rota->>Area: permite requisição
        Area-->>Operador: página de clientes
    else sessão ausente ou expirada
        Auth-->>Rota: vazio
        Rota-->>Operador: 303 /login
    end
```

O bloco `alt` representa caminhos alternativos. Somente o caminho de sessão válida chega à área restrita; o outro termina no redirecionamento ao login.
