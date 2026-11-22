"""Testes de integração; exigem TEST_DATABASE_URL de um banco descartável."""

import io
import os
import unittest
from urllib.parse import urlencode

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

from app.models.entities import Base, Cliente, Produto, RegraDeNegocio, Venda, reais
from app.models.repository import Repositorio


TEST_URL = os.getenv('TEST_DATABASE_URL')


@unittest.skipUnless(TEST_URL, 'Configure TEST_DATABASE_URL para testar com PostgreSQL.')
class CrudPostgresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not make_url(TEST_URL).database.endswith('_test'):
            raise RuntimeError('TEST_DATABASE_URL deve apontar para um banco terminado em _test.')
        cls.engine = create_engine(TEST_URL)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.repo = Repositorio(TEST_URL)

    def tearDown(self):
        self.repo.fechar()

    def _dados(self):
        self.repo.salvar_cliente({'nome': 'Ana', 'email': 'ana@example.com'})
        self.repo.salvar_produto({'nome': 'Caderno', 'preco': '20,00', 'estoque': '3'})

    def test_crud_cliente_e_produto(self):
        self._dados()
        self.assertEqual(self.repo.obter(Cliente, 1).nome, 'Ana')
        self.repo.salvar_cliente({'nome': 'Ana Maria', 'email': 'ana2@example.com'}, 1)
        self.repo.salvar_produto({'nome': 'Caderno A4', 'preco': '22.50', 'estoque': '5'}, 1)
        self.assertEqual(self.repo.obter(Cliente, 1).nome, 'Ana Maria')
        self.assertEqual(self.repo.obter(Produto, 1).preco_centavos, 2250)
        self.repo.excluir(Produto, 1)
        self.repo.excluir(Cliente, 1)
        self.assertEqual(self.repo.resumo()['clientes'], 0)

    def test_venda_estoque_total_e_rollback(self):
        self._dados()
        self.repo.salvar_venda({'cliente_id': '1', 'produto_id': '1', 'quantidade': '2'})
        self.assertEqual(self.repo.obter(Venda, 1).total_centavos, 4000)
        self.assertEqual(self.repo.obter(Produto, 1).estoque, 1)
        with self.assertRaises(RegraDeNegocio):
            self.repo.salvar_venda({'cliente_id': '1', 'produto_id': '1', 'quantidade': '5'}, 1)
        self.assertEqual(self.repo.obter(Produto, 1).estoque, 1)
        self.assertEqual(self.repo.obter(Venda, 1).quantidade, 2)
        self.repo.salvar_venda({'cliente_id': '1', 'produto_id': '1', 'quantidade': '1'}, 1)
        self.assertEqual(self.repo.obter(Produto, 1).estoque, 2)
        with self.assertRaises(RegraDeNegocio):
            self.repo.excluir(Cliente, 1)
        with self.assertRaises(RegraDeNegocio):
            self.repo.excluir(Produto, 1)
        self.repo.excluir(Venda, 1)
        self.assertEqual(self.repo.obter(Produto, 1).estoque, 3)

    def test_validacao_e_email_unico(self):
        self._dados()
        with self.assertRaises(RegraDeNegocio):
            self.repo.salvar_cliente({'nome': 'Outra', 'email': 'ANA@example.com'})
        with self.assertRaises(RegraDeNegocio):
            self.repo.salvar_produto({'nome': 'Ruim', 'preco': '1.999', 'estoque': '2'})
        self.assertEqual(self.repo.resumo()['produtos'], 1)
        self.assertEqual(reais(123456), 'R$ 1.234,56')

    def test_http_crud(self):
        import route
        from app.controllers.application import Application
        anterior = route.ctl
        route.ctl = Application(self.repo)
        try:
            self.assertEqual(self.request(route.app, 'GET', '/login')[0], '200 OK')
            self.assertEqual(self.request(route.app, 'GET', '/static/js/gestao.js')[0], '200 OK')
            self.assertEqual(self.request(route.app, 'GET', '/')[0], '303 See Other')
            route.ctl.auth.criar_usuario('teste', 'senha-forte-123')
            self.assertIn('Usuário ou senha inválidos.', self.request(route.app, 'POST', '/login',
                          {'usuario': 'teste', 'senha': 'errada'})[1])
            _, _, headers = self.request(route.app, 'POST', '/login',
                                          {'usuario': 'teste', 'senha': 'senha-forte-123'})
            cookie = next(valor.split(';')[0] for chave, valor in headers
                          if chave.lower() == 'set-cookie')
            csrf = route.ctl.auth.identificar(cookie.split('=', 1)[1])[1]
            self.assertEqual(self.request(route.app, 'GET', '/', cookie=cookie)[0], '200 OK')
            self.assertEqual(self.request(route.app, 'GET', '/clientes', cookie=cookie)[0], '200 OK')
            self.assertEqual(self.request(route.app, 'GET', '/clientes/novo', cookie=cookie)[0], '200 OK')
            self.assertEqual(self.request(route.app, 'POST', '/clientes/novo',
                             {'nome': 'Bia', 'email': 'bia@example.com'}, cookie)[0], '403 Forbidden')
            self.assertEqual(self.request(route.app, 'POST', '/clientes/novo',
                             {'nome': 'Bia', 'email': 'bia@example.com', '_csrf': csrf}, cookie)[0], '303 See Other')
            self.assertEqual(self.request(route.app, 'POST', '/produtos/novo',
                             {'nome': 'Lápis', 'preco': '4.50', 'estoque': '8', '_csrf': csrf}, cookie)[0], '303 See Other')
            self.assertEqual(self.request(route.app, 'POST', '/vendas/novo',
                             {'cliente_id': '1', 'produto_id': '1', 'quantidade': '2', '_csrf': csrf}, cookie)[0], '303 See Other')
            status, body, _ = self.request(route.app, 'GET', '/vendas/1', cookie=cookie)
            self.assertEqual(status, '200 OK')
            self.assertIn('R$ 9,00', body)
            self.assertEqual(self.request(route.app, 'POST', '/vendas/1/excluir', {'_csrf': csrf}, cookie)[0], '303 See Other')
            self.assertEqual(self.request(route.app, 'POST', '/produtos/1/excluir', {'_csrf': csrf}, cookie)[0], '303 See Other')
            self.assertEqual(self.request(route.app, 'POST', '/clientes/1/excluir', {'_csrf': csrf}, cookie)[0], '303 See Other')
            self.assertEqual(self.request(route.app, 'POST', '/logout', {'_csrf': csrf}, cookie)[0], '303 See Other')
            self.assertEqual(self.request(route.app, 'GET', '/', cookie=cookie)[0], '303 See Other')
        finally:
            route.ctl = anterior
            anterior.repositorio.fechar()

    @staticmethod
    def request(app, method, path, dados=None, cookie=None):
        conteudo = urlencode(dados or {}).encode()
        ambiente = {'REQUEST_METHOD': method, 'PATH_INFO': path, 'SERVER_NAME': 'localhost',
                    'SERVER_PORT': '80', 'SERVER_PROTOCOL': 'HTTP/1.1', 'wsgi.url_scheme': 'http',
                    'SCRIPT_NAME': '', 'QUERY_STRING': '', 'CONTENT_TYPE': 'application/x-www-form-urlencoded',
                    'CONTENT_LENGTH': str(len(conteudo)), 'wsgi.input': io.BytesIO(conteudo),
                    'wsgi.errors': io.StringIO(), 'wsgi.version': (1, 0),
                    'wsgi.multithread': False, 'wsgi.multiprocess': False, 'wsgi.run_once': False}
        if cookie:
            ambiente['HTTP_COOKIE'] = cookie
        resultado = {}
        resposta = app(ambiente, lambda status, headers, exc_info=None: resultado.update(status=status, headers=headers))
        try:
            corpo = b''.join(resposta)
        finally:
            if hasattr(resposta, 'close'):
                resposta.close()
        return resultado['status'], corpo.decode(), resultado['headers']


if __name__ == '__main__':
    unittest.main()
