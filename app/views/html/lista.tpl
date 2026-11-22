% rebase('app/views/html/base', titulo_pagina=titulo)
<div class="cabecalho"><div><p class="sobretitulo">Gestão interna</p><h1>{{titulo}}</h1></div><a class="botao" href="/{{area}}/novo">+ Novo {{singular.lower()}}</a></div>
% if erro:
<p class="erro" role="alert">{{erro}}</p>
% end
<section class="painel">
  <label class="busca">Filtrar {{titulo.lower()}}<input type="search" data-filtro placeholder="Digite para filtrar a tabela"></label>
  <p data-contagem class="resultado">{{len(registros)}} registro(s)</p>
  % if registros:
  <div class="tabela-rolagem"><table><thead><tr><th>ID</th>
  % if area == 'clientes':
    <th>Nome</th><th>E-mail</th>
  % elif area == 'produtos':
    <th>Produto</th><th>Preço</th><th>Estoque</th>
  % else:
    <th>Cliente</th><th>Produto</th><th>Qtd.</th><th>Total</th>
  % end
    <th>Ações</th></tr></thead><tbody>
  % for item in registros:
  <tr data-linha><td>{{item.id}}</td>
  % if area == 'clientes':
    <td>{{item.nome}}</td><td>{{item.email}}</td>
  % elif area == 'produtos':
    <td>{{item.nome}}</td><td>{{reais(item.preco_centavos)}}</td><td>{{item.estoque}}</td>
  % else:
    <td>{{item.cliente.nome}}</td><td>{{item.produto.nome}}</td><td>{{item.quantidade}}</td><td>{{reais(item.total_centavos)}}</td>
  % end
    <td class="acoes"><a href="/{{area}}/{{item.id}}">Ver</a><a href="/{{area}}/{{item.id}}/editar">Editar</a><form method="post" action="/{{area}}/{{item.id}}/excluir" data-confirmar="Excluir este registro?"><input type="hidden" name="_csrf" value="{{csrf}}"><button type="submit" class="botao-texto perigo">Excluir</button></form></td></tr>
  % end
  </tbody></table></div>
  % else:
  <p class="vazio">Nenhum registro ainda. Use “Novo {{singular.lower()}}” para começar.</p>
  % end
</section>
