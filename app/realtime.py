"""Hub de eventos para uma instância local do BMVC IV."""

import asyncio


class Hub:
    def __init__(self):
        self._clientes = set()
        self._loop = None

    def registrar(self):
        self._loop = asyncio.get_running_loop()
        fila = asyncio.Queue(maxsize=10)
        self._clientes.add(fila)
        return fila

    def remover(self, fila):
        self._clientes.discard(fila)

    def publicar(self):
        if self._loop is None or self._loop.is_closed():
            return
        self._loop.call_soon_threadsafe(self._entregar)

    def _entregar(self):
        for fila in tuple(self._clientes):
            if fila.full():
                fila.get_nowait()
            fila.put_nowait('dados-atualizados')


hub = Hub()
