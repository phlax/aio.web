from aio.app.testing import AioAppTestCase

import aio.web


class AioWebAppTestCase(AioAppTestCase):

    def tearDown(self):
        super(AioWebAppTestCase, self).tearDown()
        aio.web.clear()
