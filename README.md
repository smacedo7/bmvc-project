# BMVC Gestão — ERP/CRM acadêmico

Projeto de orientação a objetos em Python baseado no [BMVC fornecido pelo professor](https://github.com/hgmachine/bmvc_start_from_this). O objetivo é construir, em quatro níveis, um sistema interno simples para clientes, produtos, vendas e resumo administrativo. O planejamento está nos arquivos do [Spec Kit](https://github.com/github/spec-kit) em `.specify/` e `specs/`.

## Evolução por nível

| Nível | Entrega demonstrável | Vídeo |
| --- | --- | --- |
| BMVC I | Página estática própria, com CSS e JavaScript externos ativos | até 3 min |
| BMVC II | Modelos Python e CRUD completo em páginas BMVC | até 6 min |
| BMVC III | CRUD e controle de acesso com login e página restrita | até 10 min |
| BMVC IV | CRUD, login e atualização em tempo real por WebSocket | até 15 min |

Este checkout (`nivel/1-estatico`) contém o nível 1. As etapas futuras usarão SQLAlchemy e PostgreSQL. Veja `docs/videos/` para os roteiros.

## Executar o nível 1

Requer Python 3.11 ou superior. Na raiz do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python route.py
```

Abra `http://127.0.0.1:8080/`. Digite na busca dos módulos para conferir o JavaScript. A página original de ajuda do BMVC permanece em `/helper`.

## Organização BMVC

- `route.py`: servidor Bottle e rotas HTTP.
- `app/controllers/application.py`: controlador da renderização.
- `app/models/`: modelos de domínio nas próximas etapas.
- `app/views/html/`: templates HTML/TPL.
- `app/static/css/` e `app/static/js/`: apresentação e interação.
- `specs/`: especificação, plano e tarefas de cada nível.
- `docs/videos/`: roteiros de demonstração.

## Branches e gravação

`main` guarda a base estável publicada; `dev` recebe a integração; `nivel/1-estatico` até `nivel/4-websocket` guardam a evolução de cada etapa. As branches `video/nivel-1` até `video/nivel-4` congelam o código mostrado em cada gravação. Antes de gravar, faça checkout da branch do vídeo correspondente. Cada alteração significativa recebe um commit descritivo.

## Origem e limites

A estrutura inicial (`route.py`, `app/`, `Dockerfile`) veio do repositório do professor. A aplicação, páginas e regras do ERP/CRM são próprias. O nível 1 apresenta módulos planejados; cadastros e indicadores reais começam nos níveis seguintes. O vídeo e seu envio ao YouTube são feitos pelo estudante.
