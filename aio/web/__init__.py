import os
import json
import asyncio

from zope.dottedname.resolve import resolve

import aio.app
import aio.http

import logging
log = logging.getLogger("aio.web")

apps = {}


@asyncio.coroutine
def setup_static(webapp):
    webapp['static'] = []
    for module in aio.app.modules:
        path = os.path.join(
            module.__path__[0], "static")
        if os.path.exists(path):
            webapp['static'].append((module.__name__, path))


@asyncio.coroutine
def setup_templates(webapp):
    import aiohttp_jinja2
    import jinja2

    templates = []
    for module in aio.app.modules:
        templates.append(os.path.join(module.__path__[0], "templates"))
    aiohttp_jinja2.setup(
        webapp,
        loader=jinja2.FileSystemLoader(templates))


@asyncio.coroutine
def protocol(name):
    import aio.web

    protocol = yield from aio.http.protocol_factory(name)
    webapp = protocol._app
    aio.web.apps[name] = webapp
    yield from setup_templates(webapp)
    yield from setup_static(webapp)

    app_config = "web:%s" % name

    try:
        conf = aio.app.config[app_config]
    except KeyError:
        return protocol

    routes = conf.get('routes', None)
    if routes:
        for route in [r.strip() for r in routes.split("\n")]:
            parts = route.split(' ')
            log.debug('adding route: %s' % route)
            webapp.router.add_route(parts[0], parts[1], resolve(parts[2]))

    if "static_url" in conf and "static_dir" in conf:
        log.debug('adding static routes')
        webapp.router.add_static(
            conf['static_url'],
            os.path.abspath(conf['static_dir']))

    if not conf.get('sockets'):
        return protocol

    webapp['sockets'] = []

    @asyncio.coroutine
    def cb_sockets_emit(signal, msg):
        yield from aio.app.signals.emit('sockets-emitted', ['emit', msg])
        for socket in webapp['sockets']:
            socket.send_str(json.dumps(msg))

    @asyncio.coroutine
    def cb_sockets_info(signal, msg):
        yield from aio.app.signals.emit('sockets-emitted', ['info', msg])
        for socket in webapp['sockets']:
            socket.send_str(
                json.dumps({'info': msg}))

    @asyncio.coroutine
    def cb_sockets_error(signal, msg):
        yield from aio.app.signals.emit('sockets-emitted', ['error', msg])
        for socket in webapp['sockets']:
            socket.send_str(
                json.dumps({'error': msg}))

    aio.app.signals.listen('sockets-info', cb_sockets_info)
    aio.app.signals.listen('sockets-error', cb_sockets_error)
    aio.app.signals.listen('sockets-emit', cb_sockets_emit)

    return protocol


def clear():
    import aio.web
    aio.web.apps = {}
