<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Entrar | BMVC Gestão</title><link rel="stylesheet" href="/static/css/gestao.css"><script src="/static/js/gestao.js" defer></script></head>
<body class="pagina-login"><main class="login-painel"><p class="sobretitulo">Acesso interno</p><h1>BMVC Gestão</h1><p>Entre para consultar o resumo e administrar clientes, produtos e vendas.</p>
% if erro:
<p class="erro" role="alert">{{erro}}</p>
% end
<form method="post" action="/login"><label>Usuário<input name="usuario" required autocomplete="username" autofocus></label><label>Senha<input type="password" name="senha" required autocomplete="current-password"></label><button class="botao" type="submit">Entrar</button></form>
</main></body></html>
