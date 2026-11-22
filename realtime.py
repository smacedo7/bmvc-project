"""Entrada ASGI do nível 4: Bottle HTTP + WebSocket autenticado."""

import asyncio
from http.cookies import SimpleCookie
from urllib.parse import urlsplit

from asgiref.wsgi import WsgiToAsgi
import uvicorn

from app.realtime import hub
import route


class ServidorBMVC:
    def __init__(self):
        self.http = WsgiToAsgi(route.app)

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'websocket':
            await self.websocket(scope, receive, send)
        else:
            await self.http(scope, receive, send)

    async def websocket(self, scope, receive, send):
        if scope.get('path') != '/ws':
            await send({'type': 'websocket.close', 'code': 4404})
            return
        cabecalhos = {chave.lower(): valor for chave, valor in scope.get('headers', [])}
        origem = cabecalhos.get(b'origin', b'').decode()
        host = cabecalhos.get(b'host', b'').decode()
        if not origem or urlsplit(origem).netloc != host:
            await send({'type': 'websocket.close', 'code': 4403})
            return
        cookies = SimpleCookie()
        cookies.load(cabecalhos.get(b'cookie', b'').decode())
        token = cookies['bmvc_session'].value if 'bmvc_session' in cookies else None
        if not await asyncio.to_thread(route.ctl.auth.identificar, token):
            await send({'type': 'websocket.close', 'code': 4401})
            return
        evento = await receive()
        if evento['type'] != 'websocket.connect':
            return
        await send({'type': 'websocket.accept'})
        fila = hub.registrar()
        try:
            while True:
                entrada = asyncio.create_task(receive())
                saida = asyncio.create_task(fila.get())
                concluidas, pendentes = await asyncio.wait(
                    (entrada, saida), return_when=asyncio.FIRST_COMPLETED)
                for tarefa in pendentes:
                    tarefa.cancel()
                await asyncio.gather(*pendentes, return_exceptions=True)
                if entrada in concluidas:
                    recebido = entrada.result()
                    if recebido['type'] == 'websocket.disconnect':
                        break
                if saida in concluidas:
                    if not await asyncio.to_thread(route.ctl.auth.identificar, token):
                        await send({'type': 'websocket.close', 'code': 4401})
                        break
                    await send({'type': 'websocket.send', 'text': saida.result()})
        finally:
            hub.remover(fila)


asgi_app = ServidorBMVC()


if __name__ == '__main__':
    import os
    uvicorn.run(asgi_app, host=os.getenv('BMVC_HOST', '127.0.0.1'), port=8080,
                lifespan='off', workers=1)
