# Plano — Nível 4

Preservar Bottle como aplicação HTTP BMVC. Adicionar uma camada ASGI: `WsgiToAsgi` adapta Bottle para HTTP, enquanto `/ws` trata WebSocket autenticado. Uvicorn executa ambos via `python realtime.py`. Após transações de escrita, o controlador publica evento de atualização em um hub assíncrono; o JS do resumo recebe o evento e busca `/api/resumo` com `fetch`. A API usa a mesma sessão do nível 3. Testar conexão autorizada e recusada, evento de broadcast e resposta da API.
