#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import ClientSession
from websockets import connect
from urllib.parse import urlparse, urlunparse, urlencode
from json import loads
from .lib.digest import DigestAuth

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

def robusdk(url, username, password, accept='application/json'):
    def __init__(application):
        for case in switch(application):
            if case('rpc') or case('pipeline'):
                class Client:
                    def __enter__(self):
                        return self
                    def __exit__(self, *args):
                        pass
                    def __call__(self, prop):
                        class Callable:
                            async def connection(self):
                                try:
                                    async with ClientSession() as session:
                                        response = await DigestAuth(username, password, session).request('get', f'''{url}api/token''')
                                        if response.status == 200:
                                            url_parts = list(urlparse(url))
                                            url_parts[0] = 'ws'
                                            if type(prop).__name__ == 'list':
                                                url_parts[2] = f'/websocket/{application}/'
                                                url_parts[4] = urlencode({'q[]': prop}, True)
                                            async with connect(urlunparse(url_parts), extra_headers={
                                                'authorization': f'Bearer {await response.json()}',
                                                'accept': accept,
                                            }) as websocket:
                                                yield websocket
                                        else:
                                            raise response.raise_for_status()
                                except Exception as error:
                                    raise error
                            async def __aiter__(self):
                                async for websocket in self.connection():
                                    async for message in websocket:
                                        yield loads(message)
                                    await websocket.wait_closed()
                        return Callable()

                    def __getattr__(self, prop):
                        class Callable:
                            def __init__(self, *args, **kwargs):
                                self.current = True
                                self.args = args
                                self.kwargs = kwargs

                            def __aiter__(self):
                                return self

                            async def __anext__(self):
                                while self.current:
                                    self.current = False
                                    async with ClientSession() as session:
                                        method = {
                                            'rpc': 'post',
                                            'pipeline': 'get',
                                        }[application]
                                        response = await DigestAuth(username, password, session).request(method, f'''{url}api/{application}/{prop}''', json=[*self.args, self.kwargs], headers={
                                            'accept': accept,
                                        })
                                        for case in switch(True):
                                            if case(response.status == 200 and response.content_type == 'application/json'):
                                                return await response.json()
                                            elif case(response.status == 200 and response.content_type == 'application/octet-stream'):
                                                return await response.content.read()
                                            elif case(response.status == 504) or case(response.status == 501) or case(response.status == 500):
                                                result = await response.json()
                                                response.reason = result.get('message')
                                                raise response.raise_for_status()
                                            else:
                                                raise response.raise_for_status()
                                raise StopAsyncIteration
                        return Callable
                return Client()

    return __init__
