import asyncio
import aiohttp


@asyncio.coroutine
def handle_hello_web_world(request):
    return aiohttp.web.Response(body=b"Hello, web world")
