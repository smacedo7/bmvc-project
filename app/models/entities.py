"""Objetos de domínio persistidos pelo SQLAlchemy."""

from decimal import Decimal, InvalidOperation
import re
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class RegraDeNegocio(ValueError):
    """Uma operação viola as regras do ERP/CRM."""


def texto(valor, campo):
    valor = str(valor or '').strip()
    if not valor:
        raise RegraDeNegocio(f'{campo} é obrigatório.')
    return valor


def inteiro(valor, campo, minimo=0):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise RegraDeNegocio(f'{campo} deve ser um número inteiro.') from None
    if str(valor).strip() != str(numero) or numero < minimo:
        raise RegraDeNegocio(f'{campo} deve ser um inteiro maior ou igual a {minimo}.')
    return numero


def centavos(valor):
    try:
        decimal = Decimal(str(valor).strip().replace(',', '.')) * 100
    except InvalidOperation:
        raise RegraDeNegocio('Preço inválido.') from None
    if not decimal.is_finite() or decimal != decimal.to_integral_value() or decimal <= 0:
        raise RegraDeNegocio('Preço deve ser positivo e ter no máximo duas casas decimais.')
    return int(decimal)


def reais(valor):
    parte_inteira = f'{valor // 100:,}'.replace(',', '.')
    return f'R$ {parte_inteira},{valor % 100:02d}'


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = 'clientes'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    vendas: Mapped[list['Venda']] = relationship(back_populates='cliente')

    def atualizar(self, nome, email):
        nome = texto(nome, 'Nome')
        email = texto(email, 'E-mail').lower()
        if len(nome) > 120 or len(email) > 160:
            raise RegraDeNegocio('Nome ou e-mail excede o limite de caracteres.')
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            raise RegraDeNegocio('E-mail inválido.')
        self.nome, self.email = nome, email


class Produto(Base):
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    preco_centavos: Mapped[int] = mapped_column(Integer, nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False)
    vendas: Mapped[list['Venda']] = relationship(back_populates='produto')

    def atualizar(self, nome, preco, estoque):
        nome = texto(nome, 'Nome')
        if len(nome) > 120:
            raise RegraDeNegocio('Nome excede 120 caracteres.')
        self.nome = nome
        self.preco_centavos = centavos(preco)
        self.estoque = inteiro(estoque, 'Estoque')

    def reservar(self, quantidade):
        quantidade = inteiro(quantidade, 'Quantidade', 1)
        if quantidade > self.estoque:
            raise RegraDeNegocio('Estoque insuficiente para a venda.')
        self.estoque -= quantidade

    def devolver(self, quantidade):
        self.estoque += inteiro(quantidade, 'Quantidade', 1)


class Venda(Base):
    __tablename__ = 'vendas'

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey('clientes.id'), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey('produtos.id'), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario_centavos: Mapped[int] = mapped_column(Integer, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    cliente: Mapped[Cliente] = relationship(back_populates='vendas')
    produto: Mapped[Produto] = relationship(back_populates='vendas')

    @property
    def total_centavos(self):
        return self.quantidade * self.preco_unitario_centavos

    def atualizar(self, cliente_id, produto, quantidade):
        self.cliente_id = inteiro(cliente_id, 'Cliente', 1)
        self.produto_id = produto.id
        self.quantidade = inteiro(quantidade, 'Quantidade', 1)
        self.preco_unitario_centavos = produto.preco_centavos


class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    senha_salt: Mapped[str] = mapped_column(String(64), nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    sessoes: Mapped[list['Sessao']] = relationship(back_populates='usuario', cascade='all, delete-orphan')


class Sessao(Base):
    __tablename__ = 'sessoes'

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    csrf_token: Mapped[str] = mapped_column(String(64), nullable=False)
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    usuario: Mapped[Usuario] = relationship(back_populates='sessoes')
