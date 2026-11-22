# UML — Nível 1: página estática

O primeiro nível não possui entidades persistidas. O diagrama representa a colaboração entre a rota Bottle, o controlador BMVC, o template e os arquivos estáticos.

```mermaid
classDiagram
    class BottleApp {
        +GET /()
        +GET /helper()
        +GET /static/path()
    }

    class Application {
        -pages: dict
        +render(page)
        +inicio()
        +helper()
    }

    class InicioTPL {
        <<view>>
        +apresentarModulos()
    }

    class GestaoCSS {
        <<stylesheet>>
        +layoutResponsivo()
    }

    class GestaoJS {
        <<script>>
        +filtrarModulos()
    }

    BottleApp --> Application : solicita renderização
    Application --> InicioTPL : renderiza
    InicioTPL ..> GestaoCSS : carrega
    InicioTPL ..> GestaoJS : carrega
```

## Leitura do diagrama

- `BottleApp` representa as funções de rota de `route.py`.
- `Application` é uma classe Python real e atua como controlador.
- Os três elementos com estereótipos representam arquivos e responsabilidades da interface, não classes Python.
- A rota chama o controlador, o controlador renderiza a view e a view carrega CSS e JavaScript.

## Fluxo principal

```mermaid
sequenceDiagram
    actor Visitante
    participant Rota as route.py
    participant Controle as Application
    participant View as inicio.tpl
    participant Browser as Navegador

    Visitante->>Rota: GET /
    Rota->>Controle: render("inicio")
    Controle->>View: template(...)
    View-->>Browser: HTML + referências CSS/JS
    Visitante->>Browser: digita termo de busca
    Browser->>Browser: filtra cartões com gestao.js
```

O diagrama de sequência mostra a ordem temporal: a requisição HTTP é processada no servidor, enquanto o filtro ocorre depois no navegador, sem uma nova requisição.
