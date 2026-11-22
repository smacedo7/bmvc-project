# Roteiro do vídeo 2 — BMVC II (até 6 minutos)

## Preparação
- Fazer checkout de `video/nivel-2`.
- Subir PostgreSQL com `docker compose up -d db`, configurar `DATABASE_URL` conforme `.env.example`, instalar dependências e rodar `python route.py`.
- Deixar o repositório público e os arquivos `route.py`, `entities.py` e `repository.py` acessíveis.

## Falas e demonstração
1. **0:00–0:35** — Apresentar o ERP/CRM e a estrutura BMVC.
2. **0:35–1:15** — Mostrar classes Python `Cliente`, `Produto`, `Venda`, SQLAlchemy e PostgreSQL.
3. **1:15–2:50** — Fazer CRUD completo de um cliente: criar, visualizar, editar e excluir. Para exclusão, usar um cliente sem venda.
4. **2:50–4:35** — Criar produto e venda, mostrar o estoque diminuir e o total no resumo. Editar a venda e mostrar ajuste do estoque; excluir e mostrar devolução.
5. **4:35–5:20** — Mostrar validação de entrada e o bloqueio de exclusão de cliente/produto com venda.
6. **5:20–6:00** — Mostrar CSS/JS externos, endereço do repositório público e encerrar.

## Conferência
Gravar na própria máquina, conferir áudio e duração, demonstrar ao menos um CRUD completo e entregar links do vídeo e do repositório.
