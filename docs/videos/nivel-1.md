# Roteiro do vídeo 1 — BMVC I

Tempo máximo: **3 minutos**. Objetivo: demonstrar uma página própria servida pelo BMVC, com CSS e JavaScript externos funcionando.

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

No Windows PowerShell, substitua a ativação por:

```powershell
.venv\Scripts\Activate.ps1
```

Abra `http://127.0.0.1:8080/`. Antes de gravar, feche notificações, aumente a fonte do editor e deixe abertas estas abas:

- página inicial no navegador;
- `route.py`;
- `app/controllers/application.py`;
- `app/views/html/inicio.tpl`;
- `app/static/css/gestao.css`;
- `app/static/js/gestao.js`.

## O que falar e mostrar

### 0:00–0:20 — Apresentação

> “Este é o BMVC Gestão, um sistema interno planejado para organizar clientes, produtos, vendas e indicadores administrativos. Neste primeiro nível, apresento a página inicial personalizada.”

Mostre rapidamente a página completa.

### 0:20–0:50 — Estrutura BMVC

Mostre em `route.py` a rota `/` chamando o controlador. Depois mostre `Application.inicio()` renderizando `inicio.tpl`.

> “A rota recebe a requisição, o controlador escolhe a página e o template monta a interface.”

### 0:50–1:25 — HTML/TPL e CSS

Mostre o título, a descrição e os quatro módulos. Abra brevemente `inicio.tpl` e `gestao.css`.

> “O template possui conteúdo próprio e carrega um arquivo CSS externo. O layout se adapta ao tamanho da tela.”

Reduza um pouco a janela para demonstrar a responsividade.

### 1:25–2:15 — JavaScript ativo

Digite `clientes` na busca. Depois digite um termo inexistente.

> “O JavaScript filtra os módulos sem recarregar a página, atualiza a quantidade de resultados e mostra uma mensagem quando nada é encontrado.”

Mostre rapidamente o listener de `input` em `gestao.js`.

### 2:15–2:45 — Arquivos estáticos

Abra as ferramentas do navegador ou apenas mostre no template as referências `/static/css/gestao.css` e `/static/js/gestao.js`.

> “CSS e JavaScript são servidos pela rota de arquivos estáticos do BMVC.”

### 2:45–3:00 — Encerramento

Mostre a página final e o endereço do repositório.

> “O código está disponível no repositório público. Esta etapa atende à página personalizada com HTML/TPL, CSS e JavaScript funcionais.”

## Encerrar

No terminal, pressione `Ctrl+C` e execute `deactivate`.

## Checklist

- Página legível e diferente do exemplo de sala.
- CSS externo visível.
- Busca JavaScript demonstrada.
- Repositório público mostrado.
- Vídeo com no máximo 3 minutos.
