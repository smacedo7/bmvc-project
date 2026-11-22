# Plano técnico

Construir uma imagem a partir de `python:3.12-slim`, instalar `requirements.txt` e copiar somente o código necessário. Executar como usuário sem privilégios. No Compose, criar `web` e `db`, configurar `DATABASE_URL` com o hostname interno `db`, aguardar o healthcheck do PostgreSQL, expor serviços apenas no loopback e manter dados em volume nomeado. Validar com `docker compose config`; executar build e teste HTTP quando houver daemon disponível.
