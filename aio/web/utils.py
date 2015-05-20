import os
import asyncio
import subprocess

from aio import app

import logging
log = logging.getLogger('aio.web')


def _collectstatic():

    for s in app.config.sections():
        if s.startswith("web/"):
            section = app.config[s]
            if 'static_dir' in section:
                static_dir = os.path.abspath(section['static_dir'])
                for module in app.modules:
                    src = os.path.join(module.__path__[0], 'static')
                    if os.path.exists(src):
                        log.warn("copying %s --> %s" % (src, static_dir))
                        subprocess.getoutput(
                            'cp -a %s/* %s' % (
                                src.rstrip('/'), static_dir))


@asyncio.coroutine
def collectstatic():
    log.debug('web collecting static resources')
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _collectstatic)
