% rebase('app/views/html/base', titulo_pagina=singular)
<div class="cabecalho"><div><p class="sobretitulo">{{titulo}}</p><h1>{{singular}} #{{obj.id}}</h1></div><a href="/{{area}}">← Voltar</a></div>
<section class="painel detalhe">
% if area == 'clientes':
<dl><dt>Nome</dt><dd>{{obj.nome}}</dd><dt>E-mail</dt><dd>{{obj.email}}</dd></dl>
% elif area == 'produtos':
<dl><dt>Produto</dt><dd>{{obj.nome}}</dd><dt>Preço</dt><dd>{{reais(obj.preco_centavos)}}</dd><dt>Estoque</dt><dd>{{obj.estoque}}</dd></dl>
% else:
<dl><dt>Cliente</dt><dd>{{obj.cliente.nome}}</dd><dt>Produto</dt><dd>{{obj.produto.nome}}</dd><dt>Quantidade</dt><dd>{{obj.quantidade}}</dd><dt>Preço unitário na venda</dt><dd>{{reais(obj.preco_unitario_centavos)}}</dd><dt>Total</dt><dd>{{reais(obj.total_centavos)}}</dd><dt>Registrada em</dt><dd>{{obj.criado_em.strftime('%d/%m/%Y %H:%M')}}</dd></dl>
% end
<a class="botao" href="/{{area}}/{{obj.id}}/editar">Editar</a>
</section>
