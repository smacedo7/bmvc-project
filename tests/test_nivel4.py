"""Verifica o handshake e o broadcast WebSocket sem servidor externo."""

import asyncio
import os
import unittest

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

from app.controllers.application import Application
from app.models.entities import Base
from app.models.repository import Repositorio
from app.realtime import hub

TEST_URL = os.getenv('TEST_DATABASE_URL')


@unittest.skipUnless(TEST_URL, 'Configure TEST_DATABASE_URL para testar com PostgreSQL.')
class WebSocketTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        if not make_url(TEST_URL).database.endswith('_test'):
            raise RuntimeError('Use um banco descartável terminado em _test.')
        self.engine = create_engine(TEST_URL)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.repo = Repositorio(TEST_URL)
        import route
        self.anterior = route.ctl
        route.ctl = Application(self.repo)

    def tearDown(self):
        import route
        route.ctl = self.anterior
        self.anterior.repositorio.fechar()
        self.repo.fechar()
        self.engine.dispose()

    async def test_recusa_visitante_e_notifica_usuario(self):
        from realtime import asgi_app
        import route
        scope = {'type': 'websocket', 'path': '/ws', 'headers': [
            (b'host', b'localhost:8080'), (b'origin', b'http://localhost:8080')]}
        saida = []
        async def enviar(evento):
            saida.append(evento)
        async def receber_conexao():
            return {'type': 'websocket.connect'}
        await asgi_app.websocket(scope, receber_conexao, enviar)
        self.assertEqual(saida[0]['code'], 4401)

        route.ctl.auth.criar_usuario('teste_ws', 'senha-forte-123')
        token = route.ctl.auth.entrar('teste_ws', 'senha-forte-123')
        scope['headers'].append((b'cookie', f'bmvc_session={token}'.encode()))
        entrada = asyncio.Queue()
        eventos = asyncio.Queue()
        await entrada.put({'type': 'websocket.connect'})
        async def receber():
            return await entrada.get()
        async def enviar_fila(evento):
            await eventos.put(evento)
        tarefa = asyncio.create_task(asgi_app.websocket(scope, receber, enviar_fila))
        aceito = await asyncio.wait_for(eventos.get(), 2)
        self.assertEqual(aceito['type'], 'websocket.accept')
        hub.publicar()
        aviso = await asyncio.wait_for(eventos.get(), 2)
        self.assertEqual(aviso['text'], 'dados-atualizados')
        await entrada.put({'type': 'websocket.disconnect', 'code': 1000})
        await asyncio.wait_for(tarefa, 2)
