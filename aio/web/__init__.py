__version__ = "0.0.1"

import os
import json
import asyncio

from zope.dottedname.resolve import resolve

from aio.core.exceptions import MissingConfiguration
import aio.app

import logging
log = logging.getLogger("aio.web")

apps = {}

@asyncio.coroutine
def setup_static(app):
    app['static'] = []
    for module in aio.app.modules:
        path = os.path.join(
            module.__path__[0], "static")
        if os.path.exists(path):
            app['static'].append((module.__name__, path))


@asyncio.coroutine
def setup_templates(app):
    import aiohttp_jinja2
    import jinja2

    templates = []
    for module in aio.app.modules:
        templates.append(os.path.join(module.__path__[0], "templates"))
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(templates))


@asyncio.coroutine
def root(app):
    apps[app['name']] = app
    yield from setup_templates(app)
    yield from setup_static(app)

    app_config = "web:%s" % app['name']

    try:
        conf = aio.app.config[app_config]
    except KeyError:
        raise MissingConfiguration("No configuration for: %s" % app_config)


    for route in [r.strip() for r in conf['routes'].split("\n")]:
        parts = route.split(' ')
        log.debug('adding route: %s' % route)
        app.router.add_route(parts[0], parts[1], resolve(parts[2]))

    if "static_url" in conf and "static_dir" in conf:
        log.debug('adding static routes')
        app.router.add_static(
            conf['static_url'],
            os.path.abspath(conf['static_dir']))

    if not conf.get('sockets'):
        return

    app['sockets'] = []

    @asyncio.coroutine
    def cb_sockets_emit(signal, msg):
        yield from aio.app.signals.emit('sockets-emitted', ['emit', msg])
        for socket in app['sockets']:
            socket.send_str(json.dumps(msg))

    @asyncio.coroutine
    def cb_sockets_info(signal, msg):
        yield from aio.app.signals.emit('sockets-emitted', ['info', msg])
        for socket in app['sockets']:
            socket.send_str(
                json.dumps({'info': msg}))

    @asyncio.coroutine
    def cb_sockets_error(signal, msg):
        yield from aio.app.signals.emit('sockets-emitted', ['error', msg])
        for socket in app['sockets']:
            socket.send_str(
                json.dumps({'error': msg}))

    aio.app.signals.listen('sockets-info', cb_sockets_info)
    aio.app.signals.listen('sockets-error', cb_sockets_error)
    aio.app.signals.listen('sockets-emit', cb_sockets_emit)


def clear():
    import aio.web
    aio.web.apps = {}
