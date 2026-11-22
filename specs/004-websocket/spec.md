# Nível 4 — Atualização em tempo real por WebSocket

## Histórias e aceitação
- Um usuário autenticado abre o resumo em uma aba e mantém uma conexão WebSocket ativa.
- Outro usuário ou aba cria, edita ou exclui cliente, produto ou venda. Após o commit, a primeira aba atualiza contagens e valor vendido sem recarregar.
- Conexão WebSocket sem sessão válida é recusada.
- Se a conexão cair, a página tenta reconectar e sincroniza os dados novamente.
- CRUD completo e login do nível 3 continuam funcionando.
- CSS/JS externos permanecem ativos; o vídeo de até 15 minutos demonstra duas abas e atualização assíncrona real.

## Limites
O hub em memória atende a uma instância do servidor local para a demonstração acadêmica. Uma implantação com múltiplos processos exigiria um canal compartilhado, como Redis.
