import argparse
import asyncio

from aio.web import utils
from aio.core.utils import exit_on_error


@asyncio.coroutine
def cmd_web(argv):
    loop = asyncio.get_event_loop()

    choices = ['collectstatic']

    parser = argparse.ArgumentParser(
        prog="aio web",
        description='aio app runner')
    parser.add_argument(
        "command",
        choices=choices,
        help="other command to run")

    try:
        parsed = parser.parse_args(argv)
    except (SystemExit, IndexError):
        parser.print_help()
        loop.stop()
        loop.close()
        return
    except:
        import traceback
        traceback.print_exc()
        loop.stop()
        loop.close()
        return

    if parsed.command == 'collectstatic':
        import traceback
        yield from exit_on_error(
            utils.collectstatic(),
            on_error=traceback.print_exc)
        loop.stop()
