import os
import asyncio

import aiohttp

from aio.testing import aiotest, aiofuturetest
from aio.app.testing import AioAppTestCase
from aio.signals import Signals
import aio.app
import aio.web
from aio.app.runner import runner

CONFIG = """
[aio:commands]
run: aio.app.cmd.cmd_run

[server:test]
factory: aio.http.server.http_server
root: aio.web.root
address: 0.0.0.0
port: 7070

[web:test]
sockets: False
routes: GET / aio.web.tests.test_web_server.handle_http
"""


@asyncio.coroutine
def handle_http(request):
    return aiohttp.web.Response(body=b"Hello, world")    


class WebServerTestCase(AioAppTestCase):

    @aiofuturetest
    def test_web_server(self):
        yield from runner(
            ['run'], config_string=CONFIG)

        @asyncio.coroutine
        def _test():
            pass

        return _test

    @aiofuturetest
    def test_web_root(self):
        yield from runner(
            ['run'], config_string=CONFIG)
        app = aiohttp.web.Application()
        app['name'] = 'test'
        web = yield from aio.web.root(app)
        
        @asyncio.coroutine
        def _test():
            self.assertTrue(True)

        return _test
