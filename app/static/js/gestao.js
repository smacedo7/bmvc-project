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
