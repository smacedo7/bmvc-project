"""Ponto de entrada e rotas HTTP do BMVC."""

import os
import hmac
from bottle import Bottle, abort, redirect, request, response, run, static_file, template

from app.controllers.application import Application, AREAS
from app.models.entities import RegraDeNegocio

app = Bottle()
ctl = Application()


@app.hook('before_request')
def proteger_rotas():
    if request.path.startswith('/static/') or request.path in ('/login', '/helper'):
        return
    token = request.get_cookie('bmvc_session')
    identidade = ctl.auth.identificar(token)
    if identidade is None:
        return redirect('/login')
    usuario, csrf = identidade
    request.environ['bmvc.usuario'] = usuario
    request.environ['bmvc.csrf'] = csrf
    if request.method == 'POST' and not hmac.compare_digest(
            str(request.forms.get('_csrf', '')), csrf):
        abort(403, 'Formulário expirado. Atualize a página e tente novamente.')


def area_valida(area):
    if area not in AREAS:
        abort(404, 'Página não encontrada.')
    return area


@app.get('/login')
def login():
    if ctl.auth.identificar(request.get_cookie('bmvc_session')):
        return redirect('/')
    return template('app/views/html/login', erro=None)


@app.post('/login')
def entrar():
    try:
        token = ctl.auth.entrar(request.forms.get('usuario'), request.forms.get('senha'))
    except RegraDeNegocio as erro:
        return template('app/views/html/login', erro=str(erro))
    response.set_cookie('bmvc_session', token, path='/', max_age=8 * 60 * 60,
                        httponly=True, samesite='Lax',
                        secure=os.getenv('BMVC_COOKIE_SECURE') == '1')
    return redirect('/')


@app.post('/logout')
def sair():
    ctl.auth.sair(request.get_cookie('bmvc_session'))
    response.delete_cookie('bmvc_session', path='/')
    return redirect('/login')


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


@app.get('/helper')
def helper():
    return ctl.render('helper')


@app.get('/')
def inicio():
    return ctl.render('inicio')


@app.get('/<area>')
def lista(area):
    return ctl.lista(area_valida(area))


@app.get('/<area>/novo')
def novo(area):
    return ctl.formulario(area_valida(area))


@app.post('/<area>/novo')
def criar(area):
    area_valida(area)
    dados = dict(request.forms)
    try:
        ctl.salvar(area, dados)
    except RegraDeNegocio as erro:
        return ctl.formulario(area, erro=str(erro), valores=dados)
    return redirect(f'/{area}')


@app.get('/<area>/<id:int>')
def detalhe(area, id):
    area_valida(area)
    try:
        return ctl.detalhe(area, id)
    except RegraDeNegocio:
        abort(404, 'Registro não encontrado.')


@app.get('/<area>/<id:int>/editar')
def editar(area, id):
    area_valida(area)
    try:
        return ctl.formulario(area, id=id)
    except RegraDeNegocio:
        abort(404, 'Registro não encontrado.')


@app.post('/<area>/<id:int>/editar')
def atualizar(area, id):
    area_valida(area)
    dados = dict(request.forms)
    try:
        ctl.salvar(area, dados, id)
    except RegraDeNegocio as erro:
        return ctl.formulario(area, id=id, erro=str(erro), valores=dados)
    return redirect(f'/{area}/{id}')


@app.post('/<area>/<id:int>/excluir')
def excluir(area, id):
    area_valida(area)
    try:
        ctl.excluir(area, id)
    except RegraDeNegocio as erro:
        return ctl.lista(area, erro=str(erro))
    return redirect(f'/{area}')


if __name__ == '__main__':
    run(app, host=os.environ.get('BMVC_HOST', '127.0.0.1'), port=8080, debug=True)
