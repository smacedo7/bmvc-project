# Plano — Nível 2

- `app/models/entities.py`: classes ORM `Cliente`, `Produto`, `Venda` com validações e comportamento.
- `app/models/repository.py`: operações CRUD e transações, incluindo ajuste de estoque.
- `app/controllers/application.py`: prepara dados para templates e chama repositório.
- `route.py`: rotas HTTP, entrada dos formulários e redirecionamentos.
- `app/views/html/`: templates compartilhados de lista, formulário e detalhe.
- `compose.yaml`: PostgreSQL local para demonstração.
- Testar regras com PostgreSQL temporário e percursos HTTP do Bottle.
