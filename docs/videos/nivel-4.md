# Roteiro do vídeo 4 — BMVC IV (até 15 minutos)

## Preparação
- Fazer checkout de `video/nivel-4`, subir PostgreSQL e configurar `DATABASE_URL`.
- Criar usuário de demonstração se necessário; iniciar **`python realtime.py`**.
- Abrir duas abas autenticadas: A no resumo, B no cadastro de vendas. Deixar o status “Tempo real conectado” visível na aba A.

## Falas e demonstração
1. **0:00–1:00** — Contexto, propósito e estrutura BMVC; explicar que Bottle serve HTTP e o servidor ASGI atende `/ws`.
2. **1:00–3:30** — Login, bloqueio de área restrita para visitante e modelos SQLAlchemy/PostgreSQL.
3. **3:30–7:00** — CRUD completo de um cliente sem vendas; depois produto e venda, com estoque e total.
4. **7:00–10:30** — Manter o resumo na aba A. Na aba B, criar, editar e excluir uma venda; mostrar os indicadores na aba A mudando sem F5. Apontar a conexão WebSocket e a busca assíncrona `/api/resumo`.
5. **10:30–12:30** — Mostrar `realtime.py`, o hub, o JS e a verificação da sessão no handshake.
6. **12:30–14:00** — Demonstrar logout e impossibilidade de entrar na área restrita; mostrar CSS/JS ativos.
7. **14:00–15:00** — Mostrar repositório público e encerrar.

Conferir duração, áudio, legibilidade e que a atualização ocorreu sem recarregar a página.
