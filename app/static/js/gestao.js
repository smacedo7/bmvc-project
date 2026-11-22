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
