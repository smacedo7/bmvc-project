"""Autenticação por senha e sessões opacas persistidas em PostgreSQL."""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import re
import secrets

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models.entities import RegraDeNegocio, Sessao, Usuario


ITERACOES = 310_000
DURACAO_SESSAO = timedelta(hours=8)


class AuthService:
    def __init__(self, engine):
        self.engine = engine

    def criar_usuario(self, nome, senha):
        nome = str(nome or '').strip().lower()
        if not re.fullmatch(r'[a-z0-9_.-]{3,40}', nome):
            raise RegraDeNegocio('Usuário deve ter 3 a 40 caracteres: letras, números, _, - ou ponto.')
        if len(senha) < 8:
            raise RegraDeNegocio('Senha deve ter ao menos 8 caracteres.')
        salt = secrets.token_bytes(16)
        chave = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt, ITERACOES)
        try:
            with Session(self.engine) as db, db.begin():
                db.add(Usuario(nome=nome, senha_salt=salt.hex(), senha_hash=chave.hex()))
        except IntegrityError:
            raise RegraDeNegocio('Este nome de usuário já existe.') from None

    def entrar(self, nome, senha):
        nome = str(nome or '').strip().lower()
        senha = str(senha or '')
        with Session(self.engine) as db:
            usuario = db.scalar(select(Usuario).where(Usuario.nome == nome))
            if usuario is None:
                raise RegraDeNegocio('Usuário ou senha inválidos.')
            chave = hashlib.pbkdf2_hmac('sha256', senha.encode(),
                                        bytes.fromhex(usuario.senha_salt), ITERACOES)
            if not hmac.compare_digest(chave.hex(), usuario.senha_hash):
                raise RegraDeNegocio('Usuário ou senha inválidos.')
            usuario_id = usuario.id
        token = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        with Session(self.engine) as db, db.begin():
            db.add(Sessao(usuario_id=usuario_id,
                          token_hash=self._hash_token(token), csrf_token=csrf,
                          expira_em=datetime.now(timezone.utc) + DURACAO_SESSAO))
        return token

    def identificar(self, token):
        if not token:
            return None
        with Session(self.engine) as db:
            sessao = db.scalar(select(Sessao).options(joinedload(Sessao.usuario))
                               .where(Sessao.token_hash == self._hash_token(token)))
            if sessao is None:
                return None
            if sessao.expira_em <= datetime.now(timezone.utc):
                db.delete(sessao)
                db.commit()
                return None
            return sessao.usuario, sessao.csrf_token

    def sair(self, token):
        if not token:
            return
        with Session(self.engine) as db, db.begin():
            sessao = db.scalar(select(Sessao).where(Sessao.token_hash == self._hash_token(token)))
            if sessao:
                db.delete(sessao)

    @staticmethod
    def _hash_token(token):
        return hashlib.sha256(token.encode()).hexdigest()
