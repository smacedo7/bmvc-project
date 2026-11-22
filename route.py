"""Ponto de entrada e rotas HTTP do BMVC."""

import os
from bottle import Bottle, abort, redirect, request, run, static_file

from app.controllers.application import Application, AREAS
from app.models.entities import RegraDeNegocio

app = Bottle()
ctl = Application()


def area_valida(area):
    if area not in AREAS:
        abort(404, 'Página não encontrada.')
    return area


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
