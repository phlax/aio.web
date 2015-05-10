import os
import asyncio

import aiohttp

from aio.testing import aiotest, aiofuturetest
from aio.app.testing import AioAppTestCase
from aio.signals import Signals
import aio.app
import aio.web
from aio.app.runner import runner

TEST_DIR = os.path.dirname(__file__)

@asyncio.coroutine
def handle_http(request):
    return aiohttp.web.Response(body=b"Hello, world")    


class WebServerTestCase(AioAppTestCase):

    @aiofuturetest
    def test_web_server(self):
        yield from runner(
            ['run'],
            configfile=os.path.join(
                TEST_DIR,
                "resources", "test-1.conf"))

        @asyncio.coroutine
        def _test():
            pass

        return _test

    @aiotest
    def test_web_root(self):
        yield from runner(
            ['run'],
            configfile=os.path.join(
                TEST_DIR,
                "resources", "test-1.conf"))
        app = aiohttp.web.Application()     
        app['name'] = 'foo'
        web = yield from aio.web.root(app)
        



