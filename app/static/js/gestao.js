// Interação do nível 1: filtra os cartões sem recarregar a página.
const busca = document.querySelector('#busca-modulos');
const cartoes = [...document.querySelectorAll('[data-modulo]')];
const resultado = document.querySelector('#resultado-busca');
const vazio = document.querySelector('#sem-resultados');

if (busca && resultado && vazio) {
  busca.addEventListener('input', () => {
    const termo = busca.value.trim().toLocaleLowerCase('pt-BR');
    let encontrados = 0;
    cartoes.forEach((cartao) => {
      const texto = `${cartao.dataset.modulo} ${cartao.textContent}`.toLocaleLowerCase('pt-BR');
      const visivel = texto.includes(termo);
      cartao.hidden = !visivel;
      if (visivel) encontrados += 1;
    });
    resultado.textContent = `${encontrados} ${encontrados === 1 ? 'módulo encontrado' : 'módulos encontrados'}`;
    vazio.hidden = encontrados !== 0;
  });
}

// Filtro local de tabelas e confirmação de exclusão nas páginas CRUD.
const filtro = document.querySelector('[data-filtro]');
if (filtro) {
  const linhas = [...document.querySelectorAll('[data-linha]')];
  const contagem = document.querySelector('[data-contagem]');
  filtro.addEventListener('input', () => {
    const termo = filtro.value.trim().toLocaleLowerCase('pt-BR');
    let visiveis = 0;
    linhas.forEach((linha) => {
      const corresponde = linha.textContent.toLocaleLowerCase('pt-BR').includes(termo);
      linha.hidden = !corresponde;
      if (corresponde) visiveis += 1;
    });
    if (contagem) contagem.textContent = `${visiveis} registro(s) exibido(s)`;
  });
}

document.querySelectorAll('[data-confirmar]').forEach((formulario) => {
  formulario.addEventListener('submit', (evento) => {
    if (!window.confirm(formulario.dataset.confirmar)) evento.preventDefault();
  });
});

// O resumo recebe avisos por WebSocket e busca os números atualizados por HTTP.
const statusTempoReal = document.querySelector('[data-tempo-real]');
if (statusTempoReal) {
  let tentativas = 0;
  let ativo = true;
  const formatarReais = (centavos) => new Intl.NumberFormat('pt-BR', {
    style: 'currency', currency: 'BRL',
  }).format(centavos / 100);

  async function sincronizarResumo() {
    try {
      const resposta = await fetch('/api/resumo', { credentials: 'same-origin', cache: 'no-store' });
      if (resposta.redirected || !resposta.ok) {
        ativo = false;
        statusTempoReal.textContent = 'Sessão encerrada. Entre novamente.';
        return;
      }
      const dados = await resposta.json();
      document.querySelectorAll('[data-resumo]').forEach((campo) => {
        const chave = campo.dataset.resumo;
        campo.textContent = chave === 'faturamento_centavos'
          ? formatarReais(dados[chave]) : String(dados[chave]);
      });
    } catch (erro) {
      statusTempoReal.textContent = 'Não foi possível sincronizar os indicadores.';
    }
  }

  function conectar() {
    if (!ativo) return;
    const protocolo = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const socket = new WebSocket(`${protocolo}//${window.location.host}/ws`);
    socket.addEventListener('open', () => {
      tentativas = 0;
      statusTempoReal.textContent = 'Tempo real conectado';
      sincronizarResumo();
    });
    socket.addEventListener('message', (evento) => {
      if (evento.data === 'dados-atualizados') sincronizarResumo();
    });
    socket.addEventListener('close', () => {
      if (!ativo) return;
      statusTempoReal.textContent = 'Tempo real desconectado. Reconectando…';
      tentativas += 1;
      window.setTimeout(conectar, Math.min(1000 * 2 ** tentativas, 15000));
    });
    socket.addEventListener('error', () => socket.close());
  }
  conectar();
}
