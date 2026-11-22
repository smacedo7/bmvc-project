# Plano — Nível 3

Adicionar `Usuario` e `Sessao` ao ORM. `AuthService` gera hash PBKDF2 de senha, valida credenciais, cria token aleatório, armazena apenas seu hash, aplica prazo de validade e invalida no logout. Hook Bottle protege rotas de gestão; `login` e arquivos estáticos ficam públicos. O controlador passa CSRF aos templates. Um comando CLI cria o primeiro usuário sem credenciais versionadas.
