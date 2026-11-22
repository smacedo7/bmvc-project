"""Controlador BMVC: coordena casos de uso e prepara as visões."""

from bottle import template

from app.models.entities import Cliente, Produto, RegraDeNegocio, Venda, reais
from app.models.repository import Repositorio


AREAS = {
    'clientes': (Cliente, 'Clientes', 'Cliente'),
    'produtos': (Produto, 'Produtos', 'Produto'),
    'vendas': (Venda, 'Vendas', 'Venda'),
}


class Application:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio or Repositorio()
        self.pages = {'helper': self.helper, 'inicio': self.inicio}

    def render(self, page):
        content = self.pages.get(page, self.helper)
        return content()

    def helper(self):
        return template('app/views/html/helper')

    def inicio(self):
        return template('app/views/html/inicio', resumo=self.repositorio.resumo(), reais=reais)

    def lista(self, area, erro=None):
        classe, titulo, singular = AREAS[area]
        return template('app/views/html/lista', area=area, titulo=titulo, singular=singular,
                        registros=self.repositorio.listar(classe), erro=erro, reais=reais)

    def formulario(self, area, id=None, erro=None, valores=None):
        classe, titulo, singular = AREAS[area]
        obj = self.repositorio.obter(classe, id) if id else None
        if id and obj is None:
            raise RegraDeNegocio('Registro não encontrado.')
        if valores is None:
            valores = self._valores(obj, area)
        return template('app/views/html/formulario', area=area, titulo=titulo,
                        singular=singular, obj=obj, valores=valores, erro=erro,
                        clientes=self.repositorio.listar(Cliente) if area == 'vendas' else [],
                        produtos=self.repositorio.listar(Produto) if area == 'vendas' else [],
                        reais=reais)

    def detalhe(self, area, id):
        classe, titulo, singular = AREAS[area]
        obj = self.repositorio.obter(classe, id)
        if obj is None:
            raise RegraDeNegocio('Registro não encontrado.')
        return template('app/views/html/detalhe', area=area, titulo=titulo,
                        singular=singular, obj=obj, reais=reais)

    def salvar(self, area, dados, id=None):
        if area == 'clientes':
            self.repositorio.salvar_cliente(dados, id)
        elif area == 'produtos':
            self.repositorio.salvar_produto(dados, id)
        else:
            self.repositorio.salvar_venda(dados, id)

    def excluir(self, area, id):
        self.repositorio.excluir(AREAS[area][0], id)

    @staticmethod
    def _valores(obj, area):
        if obj is None:
            return {}
        if area == 'clientes':
            return {'nome': obj.nome, 'email': obj.email}
        if area == 'produtos':
            return {'nome': obj.nome, 'preco': f'{obj.preco_centavos / 100:.2f}',
                    'estoque': str(obj.estoque)}
        return {'cliente_id': str(obj.cliente_id), 'produto_id': str(obj.produto_id),
                'quantidade': str(obj.quantidade)}
