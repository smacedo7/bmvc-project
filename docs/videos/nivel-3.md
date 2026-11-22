# Roteiro do vídeo 3 — BMVC III (até 10 minutos)

## Preparação
- Fazer checkout de `video/nivel-3` e subir PostgreSQL.
- Criar usuário de demonstração com `python -m app.manage create-user` (não mostrar a senha na gravação).
- Iniciar `python route.py`; abrir navegador em janela privada.

## Falas e demonstração
1. **0:00–0:50** — Explicar propósito e estrutura BMVC, modelos Python e PostgreSQL.
2. **0:50–2:00** — Abrir `/` sem login; mostrar redirecionamento. Entrar com usuário de teste e abrir resumo restrito.
3. **2:00–5:40** — Mostrar CRUD completo de um cliente sem vendas: criar, consultar, editar e excluir. Mostrar também produto e venda com cálculo e ajuste de estoque.
4. **5:40–7:00** — Mostrar `Usuario`, `Sessao`, hash de senha e proteção no hook Bottle, sem revelar tokens ou credenciais.
5. **7:00–8:15** — Sair e tentar acessar a área restrita; mostrar que voltou ao login.
6. **8:15–9:20** — Mostrar CSS e JS externos funcionando com o filtro de tabela e confirmação de exclusão.
7. **9:20–10:00** — Mostrar link do repositório público e encerrar.

Conferir duração, áudio, legibilidade, execução na própria máquina e links de entrega.
