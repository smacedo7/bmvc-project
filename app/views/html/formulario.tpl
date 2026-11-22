% rebase('app/views/html/base', titulo_pagina=('Editar ' if obj else 'Novo ') + singular)
<div class="cabecalho"><div><p class="sobretitulo">{{titulo}}</p><h1>{{'Editar' if obj else 'Novo'}} {{singular.lower()}}</h1></div><a href="/{{area}}">← Voltar</a></div>
<section class="painel formulario">
% if erro:
<p class="erro" role="alert">{{erro}}</p>
% end
<form method="post" action="{{('/' + area + '/' + str(obj.id) + '/editar') if obj else ('/' + area + '/novo')}}">
<input type="hidden" name="_csrf" value="{{csrf}}">
% if area == 'clientes':
<label>Nome<input name="nome" required maxlength="120" value="{{valores.get('nome', '')}}"></label>
<label>E-mail<input name="email" type="email" required maxlength="160" value="{{valores.get('email', '')}}"></label>
% elif area == 'produtos':
<label>Nome<input name="nome" required maxlength="120" value="{{valores.get('nome', '')}}"></label>
<label>Preço (R$)<input name="preco" type="number" min="0.01" step="0.01" required value="{{valores.get('preco', '')}}"></label>
<label>Estoque<input name="estoque" type="number" min="0" step="1" required value="{{valores.get('estoque', '')}}"></label>
% else:
<label>Cliente<select name="cliente_id" required><option value="">Selecione</option>
% for cliente in clientes:
<option value="{{cliente.id}}" {{'selected' if str(cliente.id) == valores.get('cliente_id') else ''}}>{{cliente.nome}}</option>
% end
</select></label>
<label>Produto<select name="produto_id" required><option value="">Selecione</option>
% for produto in produtos:
<option value="{{produto.id}}" {{'selected' if str(produto.id) == valores.get('produto_id') else ''}}>{{produto.nome}} · {{reais(produto.preco_centavos)}} · {{produto.estoque}} em estoque</option>
% end
</select></label>
<label>Quantidade<input name="quantidade" type="number" min="1" step="1" required value="{{valores.get('quantidade', '1')}}"></label>
% if not clientes or not produtos:
<p class="resultado">Cadastre ao menos um cliente e um produto antes de registrar vendas.</p>
% end
% end
<button class="botao" type="submit">{{'Salvar alterações' if obj else 'Cadastrar'}}</button>
</form></section>
