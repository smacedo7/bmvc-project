# UML — Nível 1: página estática

O primeiro nível ainda não possui entidades de negócio persistidas. O diagrama mostra a colaboração entre a rota Bottle, o controlador BMVC, o template e os arquivos estáticos.

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

Fluxo principal:

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
