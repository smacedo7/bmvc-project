# Execução do BMVC IV com Docker Compose

## Objetivo
Permitir que o estudante execute a aplicação e PostgreSQL com um único `docker compose up --build -d` para a demonstração do nível 4.

## Critérios de aceitação
- O serviço `db` usa PostgreSQL, volume persistente e healthcheck.
- O serviço `web` constrói a imagem Python, espera `db` ficar saudável e inicia `realtime.py`.
- HTTP e PostgreSQL são publicados apenas em `127.0.0.1` nas portas 8080 e 5433.
- O primeiro usuário pode ser criado por `docker compose run --rm web python -m app.manage create-user`.
- O README descreve inicialização, verificação, parada e persistência dos dados.
- O roteiro do vídeo 4 inclui o caminho via Compose.
