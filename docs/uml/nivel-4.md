# UML — Nível 4: atualização por WebSocket

O quarto nível mantém CRUD e autenticação. `ServidorBMVC` adapta o Bottle para HTTP e atende `/ws`; `Hub` registra conexões e distribui avisos após alterações confirmadas no banco.

```mermaid
classDiagram
    class ServidorBMVC {
        -http: WsgiToAsgi
        +__call__(scope, receive, send)
        +websocket(scope, receive, send)
    }
    class BottleApp {
        <<WSGI>>
        +rotas HTTP
        +GET /api/resumo
    }
    class Application {
        -repositorio: Repositorio
        +auth: AuthService
        +salvar(area, dados, id)
        +excluir(area, id)
    }
    class Hub {
        -clientes: set
        -loop
        +registrar() Queue
        +remover(fila)
        +publicar()
        -_entregar()
    }
    class AuthService {
        +identificar(token)
    }
    class Repositorio {
        +resumo() dict
        +salvar_cliente(dados, id)
        +salvar_produto(dados, id)
        +salvar_venda(dados, id)
        +excluir(classe, id)
    }
    class PostgreSQL {
        <<database>>
    }

    ServidorBMVC --> BottleApp : adapta HTTP
    ServidorBMVC --> AuthService : valida WebSocket
    ServidorBMVC --> Hub : registra conexão
    BottleApp --> Application
    Application --> Repositorio
    Application --> Hub : publica após commit
    Repositorio --> PostgreSQL
```

## Leitura do diagrama

`ServidorBMVC` é a entrada ASGI e encaminha requisições HTTP ao Bottle. Conexões WebSocket seguem outro caminho: autenticação, registro no `Hub` e espera por eventos. O controlador publica somente após a persistência terminar com sucesso.

## Atualização do resumo em duas abas

```mermaid
sequenceDiagram
    actor Operador
    participant Resumo as Aba A: resumo
    participant WS as ServidorBMVC /ws
    participant Cadastro as Aba B: cadastro
    participant App as Application
    participant Repo as Repositorio
    participant Hub
    participant API as GET /api/resumo

    Resumo->>WS: conecta com cookie de sessão
    WS-->>Resumo: websocket.accept
    Operador->>Cadastro: salva ou exclui registro
    Cadastro->>App: POST autenticado + CSRF
    App->>Repo: executa transação
    Repo-->>App: COMMIT
    App->>Hub: publicar()
    Hub->>WS: dados-atualizados
    WS-->>Resumo: dados-atualizados
    Resumo->>API: fetch /api/resumo
    API-->>Resumo: contagens e valor vendido
    Resumo->>Resumo: atualiza indicadores sem F5
```

A ordem evidencia duas garantias: o aviso só ocorre após o `COMMIT`, e a tela consulta a API antes de exibir os números novos.
