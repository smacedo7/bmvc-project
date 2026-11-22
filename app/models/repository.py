"""Casos de uso e persistência transacional do ERP/CRM."""

import os
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models.entities import Cliente, Produto, RegraDeNegocio, Venda, inteiro


class Repositorio:
    def __init__(self, url=None):
        url = url or os.getenv('DATABASE_URL')
        if not url:
            raise RuntimeError('Configure DATABASE_URL com a conexão PostgreSQL. Veja .env.example.')
        if not url.startswith('postgresql+psycopg://'):
            raise RuntimeError('DATABASE_URL deve usar PostgreSQL com o driver psycopg.')
        self.engine = create_engine(url, pool_pre_ping=True)

    def fechar(self):
        self.engine.dispose()

    def listar(self, classe):
        with Session(self.engine) as db:
            consulta = select(classe).order_by(classe.id)
            if classe is Venda:
                consulta = consulta.options(joinedload(Venda.cliente), joinedload(Venda.produto))
            return list(db.scalars(consulta))

    def obter(self, classe, id):
        with Session(self.engine) as db:
            consulta = select(classe).where(classe.id == id)
            if classe is Venda:
                consulta = consulta.options(joinedload(Venda.cliente), joinedload(Venda.produto))
            return db.scalars(consulta).first()

    def _obrigatorio(self, db, classe, id):
        obj = db.get(classe, inteiro(id, 'Identificador', 1))
        if obj is None:
            raise RegraDeNegocio('Registro não encontrado.')
        return obj

    def salvar_cliente(self, dados, id=None):
        try:
            with Session(self.engine) as db, db.begin():
                cliente = self._obrigatorio(db, Cliente, id) if id else Cliente()
                cliente.atualizar(dados.get('nome'), dados.get('email'))
                db.add(cliente)
        except IntegrityError:
            raise RegraDeNegocio('Já existe um cliente com este e-mail.') from None

    def salvar_produto(self, dados, id=None):
        with Session(self.engine) as db, db.begin():
            produto = self._obrigatorio(db, Produto, id) if id else Produto()
            produto.atualizar(dados.get('nome'), dados.get('preco'), dados.get('estoque'))
            db.add(produto)

    def salvar_venda(self, dados, id=None):
        with Session(self.engine) as db, db.begin():
            cliente_id = inteiro(dados.get('cliente_id'), 'Cliente', 1)
            produto_id = inteiro(dados.get('produto_id'), 'Produto', 1)
            quantidade = inteiro(dados.get('quantidade'), 'Quantidade', 1)
            if db.get(Cliente, cliente_id) is None:
                raise RegraDeNegocio('Selecione um cliente válido.')
            venda = self._obrigatorio(db, Venda, id) if id else Venda()
            ids_produtos = {produto_id}
            if id:
                ids_produtos.add(venda.produto_id)
            produtos = {
                produto.id: produto for produto in db.scalars(
                    select(Produto).where(Produto.id.in_(ids_produtos))
                    .order_by(Produto.id).with_for_update())
            }
            produto = produtos.get(produto_id)
            if produto is None:
                raise RegraDeNegocio('Selecione um produto válido.')
            if id:
                produtos[venda.produto_id].devolver(venda.quantidade)
            produto.reservar(quantidade)
            venda.atualizar(cliente_id, produto, quantidade)
            db.add(venda)

    def excluir(self, classe, id):
        try:
            with Session(self.engine) as db, db.begin():
                obj = self._obrigatorio(db, classe, id)
                if classe is Venda:
                    produto = db.scalars(select(Produto).where(Produto.id == obj.produto_id).with_for_update()).one()
                    produto.devolver(obj.quantidade)
                elif db.scalar(select(func.count()).select_from(Venda).where(
                    (Venda.cliente_id if classe is Cliente else Venda.produto_id) == id)):
                    raise RegraDeNegocio('Não é possível excluir um registro que possui vendas.')
                db.delete(obj)
        except IntegrityError:
            raise RegraDeNegocio('Não é possível excluir este registro porque está em uso.') from None

    def resumo(self):
        with Session(self.engine) as db:
            return {
                'clientes': db.scalar(select(func.count()).select_from(Cliente)),
                'produtos': db.scalar(select(func.count()).select_from(Produto)),
                'vendas': db.scalar(select(func.count()).select_from(Venda)),
                'faturamento_centavos': db.scalar(select(func.coalesce(func.sum(
                    Venda.quantidade * Venda.preco_unitario_centavos), 0)))
            }
