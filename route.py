"""Ponto de entrada do BMVC: rotas Bottle e arquivos estáticos."""

import os
from bottle import Bottle, run, static_file
from app.controllers.application import Application

app = Bottle()
ctl = Application()


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


@app.route('/helper')
def helper():
    return ctl.render('helper')


@app.route('/')
def inicio():
    return ctl.render('inicio')


if __name__ == '__main__':
    run(app, host=os.environ.get('BMVC_HOST', '127.0.0.1'), port=8080, debug=True)
