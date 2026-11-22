# Apresentação do Nível 1 — BMVC I

Tempo máximo: **3 minutos**. Planejamento: **2 minutos e 45 segundos**, com 15 segundos de margem.

## O que foi implementado

O primeiro nível apresenta o **BMVC Gestão**, a página inicial de um ERP/CRM simples planejado para administrar clientes, produtos, vendas e indicadores. Nesta etapa, o projeto serve uma página TPL personalizada com conteúdo legível, propósito definido e arquivos CSS e JavaScript externos.

O fluxo é:

```text
Navegador -> route.py -> Application -> inicio.tpl -> CSS e JavaScript
```

- `route.py` recebe `GET /` e solicita a página `inicio` ao controlador.
- `Application` associa o nome da página ao método `inicio()` e renderiza o template.
- `inicio.tpl` contém a estrutura e o conteúdo da página.
- `gestao.css` define o visual e o comportamento responsivo.
- `gestao.js` filtra os cartões e atualiza a contagem sem recarregar a página.

Ainda não há banco, CRUD, login, WebSocket ou entidades de negócio. A pasta `models` fica vazia porque esses objetos começam no Nível 2. A orientação a objetos desta etapa aparece no controlador `Application`, instanciado e utilizado pelas rotas.

## Como explicar a UML

Abra [`docs/uml/nivel-1.md`](../uml/nivel-1.md).

- `BottleApp` representa as rotas declaradas em `route.py`.
- `Application` é a classe Python que controla a escolha e a renderização das páginas.
- `InicioTPL`, `GestaoCSS` e `GestaoJS` representam os papéis dos arquivos da interface; não são classes Python.
- `+` indica uma operação pública e `-` um atributo interno.
- `-->` representa uma chamada direta.
- `..>` representa o uso de um recurso, como o template carregando CSS e JavaScript.
- `<<view>>`, `<<stylesheet>>` e `<<script>>` identificam o papel de cada elemento.

No diagrama de sequência, leia de cima para baixo: o visitante acessa `/`, a rota chama `render("inicio")`, o controlador processa `inicio.tpl`, o navegador recebe o HTML e depois executa o filtro local ao receber uma pesquisa.

## Preparar o ambiente

```bash
git fetch origin
git switch video/nivel-1
git pull --ff-only origin video/nivel-1

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python route.py
```

Abra `http://127.0.0.1:8080/`. Deixe também abertos `route.py`, `app/controllers/application.py`, `app/views/html/inicio.tpl` e a UML.

## Roteiro cronometrado

| Tempo | Mostrar | Fala sugerida |
|---|---|---|
| 0:00–0:20 | Repositório e página | “Este é o BMVC Gestão, um projeto acadêmico de ERP e CRM simples desenvolvido em Python com o framework BMVC. Neste primeiro nível, o objetivo é servir uma página personalizada com CSS e JavaScript funcionais.” |
| 0:20–0:45 | Módulos da página | “A página apresenta a visão do projeto e os módulos planejados: clientes, produtos, vendas e resumo administrativo. Neste nível ela é estática; os objetos, o CRUD e o banco serão adicionados nos próximos níveis.” |
| 0:45–1:15 | UML de classes/componentes | “A UML representa o fluxo da aplicação. BottleApp corresponde às rotas de `route.py`. A rota principal utiliza o controlador `Application`, que seleciona a página e renderiza `inicio.tpl`.” |
| 1:15–1:35 | UML de sequência | “A requisição chega à rota, passa pelo controlador e retorna o template ao navegador. A view carrega CSS e JavaScript externos. Depois disso, a pesquisa é executada no próprio navegador.” |
| 1:35–1:55 | `route.py` | “A rota `/` recebe a requisição e chama `render` passando `inicio`. A rota `static` entrega os arquivos CSS e JavaScript.” |
| 1:55–2:15 | `application.py` | “A classe `Application` funciona como controlador. Seu dicionário associa o nome lógico da página ao método correspondente, e `inicio()` renderiza o template correto.” |
| 2:15–2:30 | TPL, CSS e JS | “O TPL contém a estrutura da página, o CSS cria o layout responsivo e o JavaScript implementa a pesquisa dos módulos.” |
| 2:30–2:40 | Busca funcionando | “Ao pesquisar por ‘vendas’, os cartões são filtrados e a quantidade de resultados muda sem recarregar a página, comprovando que o JavaScript está ativo.” |
| 2:40–2:45 | Repositório público | “O código, a documentação e a UML estão disponíveis neste repositório público.” |

## Perguntas prováveis

**Onde está a orientação a objetos?**

A classe `Application` encapsula os métodos de renderização e é instanciada como controlador. As entidades de negócio começam no Nível 2.

**Por que a pasta `models` está vazia?**

Porque o escopo do Nível 1 é uma página estática. Clientes, produtos e vendas ainda não são objetos persistidos.

**A página é HTML ou TPL?**

É um template TPL processado pelo Bottle. O conteúdo desta etapa é estático.

**Como provar que o JavaScript funciona?**

Pesquisando no campo de módulos: cartões, contador e mensagem vazia mudam sem recarregar a página.

## Checklist

- Página executada na própria máquina.
- CSS e JavaScript externos demonstrados.
- Busca e responsividade mostradas.
- Repositório público exibido.
- Vídeo com no máximo 3 minutos.
