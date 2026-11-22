% rebase('app/views/html/base', titulo_pagina='Resumo')
<section class="hero"><p class="sobretitulo">ERP + CRM simples</p><h1>Resumo administrativo</h1><p>Acompanhe clientes, produtos e vendas da operação.</p></section>
<section class="grade resumo" aria-label="Indicadores">
  <a class="cartao indicador" href="/clientes"><span>Clientes</span><strong data-resumo="clientes">{{resumo['clientes']}}</strong><small>Ver cadastro →</small></a>
  <a class="cartao indicador" href="/produtos"><span>Produtos</span><strong data-resumo="produtos">{{resumo['produtos']}}</strong><small>Ver catálogo →</small></a>
  <a class="cartao indicador" href="/vendas"><span>Vendas</span><strong data-resumo="vendas">{{resumo['vendas']}}</strong><small>Ver registros →</small></a>
  <a class="cartao indicador" href="/vendas"><span>Valor vendido</span><strong data-resumo="faturamento_centavos">{{reais(resumo['faturamento_centavos'])}}</strong><small>Somatório histórico →</small></a>
</section>
<p class="status-tempo-real" data-tempo-real role="status" aria-live="polite">Conectando ao tempo real…</p>
