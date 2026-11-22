<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BMVC Gestão | Visão do projeto</title>
  <link rel="stylesheet" href="/static/css/gestao.css">
  <script src="/static/js/gestao.js" defer></script>
</head>
<body>
  <header class="topo"><div class="container topo-conteudo"><a class="marca" href="/">BMVC <strong>Gestão</strong></a><span class="selo">Projeto acadêmico · Nível 1</span></div></header>
  <main class="container">
    <section class="hero">
      <p class="sobretitulo">ERP + CRM simples</p>
      <h1>Uma visão clara da operação</h1>
      <p>Este projeto organiza clientes, produtos e vendas em um só lugar. Nesta primeira etapa, a página apresenta o propósito do sistema e a estrutura dos módulos.</p>
      <a class="botao" href="#modulos">Conhecer módulos ↓</a>
    </section>
    <section id="modulos" class="modulos" aria-labelledby="titulo-modulos">
      <div class="secao-titulo"><div><p class="sobretitulo">Estrutura do sistema</p><h2 id="titulo-modulos">Módulos planejados</h2></div><p>Use a busca para filtrar os módulos.</p></div>
      <label class="busca">Buscar módulo <input id="busca-modulos" type="search" placeholder="Ex.: clientes" autocomplete="off"></label>
      <p id="resultado-busca" class="resultado" role="status" aria-live="polite">4 módulos encontrados</p>
      <div class="grade" id="lista-modulos">
        <article class="cartao" data-modulo="clientes relacionamento cadastro contatos crm"><span class="icone" aria-hidden="true">01</span><h3>Clientes</h3><p>Dados de contato e relacionamento com compradores.</p></article>
        <article class="cartao" data-modulo="produtos catalogo preco estoque erp"><span class="icone" aria-hidden="true">02</span><h3>Produtos</h3><p>Catálogo de itens, preços e disponibilidade.</p></article>
        <article class="cartao" data-modulo="vendas pedidos quantidade total erp"><span class="icone" aria-hidden="true">03</span><h3>Vendas</h3><p>Registro de pedidos e acompanhamento comercial.</p></article>
        <article class="cartao" data-modulo="resumo administrativo indicadores painel dashboard"><span class="icone" aria-hidden="true">04</span><h3>Resumo administrativo</h3><p>Indicadores para acompanhar a operação.</p></article>
      </div>
      <p id="sem-resultados" class="vazio" hidden>Nenhum módulo corresponde à busca.</p>
    </section>
    <section class="proximos"><h2>Próximas etapas</h2><p>O nível 2 incluirá modelos Python e operações de cadastro, consulta, edição e exclusão. Os níveis seguintes acrescentarão controle de acesso e atualização em tempo real.</p></section>
  </main>
  <footer class="container rodape">Construído com Python, Bottle e a estrutura BMVC fornecida pelo professor.</footer>
</body>
</html>
