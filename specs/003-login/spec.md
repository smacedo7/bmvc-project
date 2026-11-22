# Nível 3 — Login e área restrita

## Histórias e aceitação
- Operador criado por comando local consegue entrar com usuário e senha.
- Senha incorreta recebe mensagem genérica; senha não é armazenada em texto puro.
- Página inicial e CRUD redirecionam visitante para `/login`.
- Usuário autenticado pode usar o CRUD do nível 2 e acessar o resumo restrito.
- Sair invalida a sessão; a mesma sessão não funciona depois.
- Formulários de alteração exigem token CSRF da sessão.
- CSS/JS externos continuam ativos; o vídeo de até 10 minutos mostra login, área restrita e CRUD completo.

## Restrições
Sessão opaca armazenada no banco, cookie HttpOnly e SameSite=Lax. Sem cadastro público de usuários. Para implantação HTTPS, ativar cookie Secure.
