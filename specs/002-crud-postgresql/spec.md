# Nível 2 — CRUD com modelos Python

## Objetivo
Transformar a apresentação estática em um ERP/CRM operável com clientes, produtos e vendas persistidos em PostgreSQL via SQLAlchemy.

## Histórias e aceitação
1. O operador cria, lista, consulta detalhes, edita e exclui clientes. Nome e e-mail são válidos; e-mail é único.
2. O operador cria, lista, consulta detalhes, edita e exclui produtos. Preço em centavos é positivo e estoque não negativo.
3. O operador cria, lista, consulta detalhes, edita e exclui vendas de um produto para um cliente. Quantidade positiva não pode exceder estoque. Criar reduz estoque; editar ajusta estoque; excluir devolve estoque. O preço histórico da venda é preservado e o total é calculado pelo objeto `Venda`.
4. Não se exclui cliente ou produto que possua vendas; o sistema mostra mensagem legível.
5. Resumo administrativo apresenta contagens e valor das vendas.
6. Páginas legíveis carregam CSS e JS externos ativos. Busca e confirmação de exclusão usam JS.
7. Vídeo de até 6 minutos demonstra o CRUD completo de pelo menos um modelo e o funcionamento local do BMVC.

## Restrições
- PostgreSQL é o banco da aplicação; URL em `DATABASE_URL`, sem credenciais no Git.
- SQLAlchemy 2.0 para ORM; Bottle e estrutura BMVC preservados.
- Usar um item por venda para manter o escopo demonstrável.
- Criação automática das tabelas na inicialização local; alterações futuras de esquema exigirão migração documentada.
