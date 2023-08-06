from asyncio import create_task
from blacksheep import WebSocket
from functools import wraps
from typing import Callable, Coroutine

from kikiutils.aes import AesCrypt

from utils.blacksheep import get_ip


class ServiceWebsocketConnection:
    code: str = ''

    def __init__(
        self,
        aes: AesCrypt,
        exter_headers: dict,
        ip: str,
        websocket: WebSocket
    ):
        self.aes = aes
        self.exter_headers = exter_headers
        self.ip = ip
        self.ws = websocket

    async def emit(self, event: str, *args, **kwargs):
        await self.send_text(self.aes.encrypt([event, args, kwargs]))

    async def send_text(self, text: str):
        await self.ws.send_text(text)

    async def recv_data(self) -> list:
        return self.aes.decrypt(await self.ws.receive_text())


class ServiceWebsockets:
    def __init__(self, aes: AesCrypt, service_name: str):
        self.aes = aes
        self.connections: dict[
            str,
            dict[str, ServiceWebsocketConnection]
        ] = {}

        self.event_handlers: dict[str, Callable[..., Coroutine]] = {}
        self.service_name = service_name

    def _add_connection(
        self,
        group_name: str,
        connection: ServiceWebsocketConnection
    ):
        if group_name in self.connections:
            self.connections[group_name][connection.code] = connection
        else:
            self.connections[group_name] = {connection.code: connection}

    def _del_connection(
        self,
        group_name: str,
        connection: ServiceWebsocketConnection
    ):
        if group_name in self.connections:
            self.connections[group_name].pop(connection.code, None)

            if not self.connections[group_name]:
                self.connections.pop(group_name, None)

    async def _listen(self, connection: ServiceWebsocketConnection):
        while True:
            event, args, kwargs = await connection.recv_data()

            if event in self.event_handlers:
                create_task(
                    self.event_handlers[event](
                        connection,
                        *args,
                        **kwargs
                    )
                )

    async def accept_and_listen(
        self,
        group_name: str,
        websocket: WebSocket,
        extra_headers: dict = {}
    ):
        await websocket.accept()
        ip = get_ip(websocket)
        connection = ServiceWebsocketConnection(
            self.aes,
            extra_headers,
            ip,
            websocket
        )

        data = None

        try:
            data = await connection.recv_data()

            if data[0] != 'init' or 'code' not in data[2]:
                raise ValueError('')

            connection.code = data[2]['code']
            self._add_connection(group_name, connection)
            await self._listen(connection)
        except:
            pass

        if connection.code:
            self._del_connection(group_name, connection)

    async def emit_to_all(self, event: str, *args, **kwargs):
        data = self.aes.encrypt([event, args, kwargs])

        for group in self.connections.values():
            for c in group.values():
                await c.send_text(data)

    async def emit_to_group(
        self,
        group_name: str,
        event: str,
        *args,
        **kwargs
    ):
        if group_name in self.connections:
            data = self.aes.encrypt([event, args, kwargs])

            for c in self.connections[group_name].values():
                await c.send_text(data)

    def on(self, event: str):
        """Register event handler."""

        def decorator(view_func):
            @wraps(view_func)
            async def wrapped_view(*args, **kwargs):
                await view_func(*args, **kwargs)
            self.event_handlers[event] = wrapped_view
            return wrapped_view
        return decorator
