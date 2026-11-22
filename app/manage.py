"""Comandos de administração local: python -m app.manage create-user."""

import getpass
import sys

from app.models.auth import AuthService
from app.models.entities import RegraDeNegocio
from app.models.repository import Repositorio


def main():
    if len(sys.argv) != 2 or sys.argv[1] != 'create-user':
        raise SystemExit('Uso: python -m app.manage create-user')
    nome = input('Nome de usuário: ')
    senha = getpass.getpass('Senha (mínimo 8 caracteres): ')
    confirmar = getpass.getpass('Confirmar senha: ')
    if senha != confirmar:
        raise SystemExit('As senhas não conferem.')
    repo = Repositorio()
    try:
        AuthService(repo.engine).criar_usuario(nome, senha)
    except RegraDeNegocio as erro:
        raise SystemExit(str(erro)) from None
    finally:
        repo.fechar()
    print('Usuário criado.')


if __name__ == '__main__':
    main()
