========
aio.http
========


Installation
------------

Install with:

  pip install aio.web

Configuration
-------------

Create a config defining a factory method and a root handler

We can define routes in a corresponding [web:{name}] section when using aio.web.root

  >>> CONFIG = """
  ... [aio:commands]
  ... run: aio.app.cmd.cmd_run
  ... 
  ... [server:test]
  ... factory: aio.http.server.http_server
  ... root: aio.web.root
  ... address: 0.0.0.0
  ... port: 7070
  ... 
  ... [web:test]
  ... routes: GET / aio.web.tests.handle_hello_web_world
  ... """

Running
-------

Run with the aio command

  # aio run


See http://github.com/phlax/aio.app for more information on the "aio run" command
  
Running the app
---------------

And define an object to collect the results

  >>> class Response:
  ...     body = None
  >>> response = Response()

Lets run an async test to get the default http response

  >>> import asyncio
  >>> import aiohttp
  >>> from aio.app.runner import runner  

  >>> def run_future_app():
  ...     yield from runner(['run'], config_string=CONFIG)
  ... 
  ...     @asyncio.coroutine
  ...     def _test_http():
  ...         response.body = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", "http://localhost:7070")).read()
  ... 
  ...     return _test_http

And run the test

  >>> from aio.testing import aiofuturetest
  >>> aiofuturetest(run_future_app, timeout=5, sleep=2)()  
  >>> response.body
  b'Hello, web world'


Static directory
----------------

  >>> CONFIG = """
  ... [aio:commands]
  ... run: aio.app.cmd.cmd_run
  ... 
  ... [server:test]
  ... factory: aio.http.server.http_server
  ... root: aio.web.root
  ... address: 0.0.0.0
  ... port: 7070
  ... 
  ... [web:test]
  ... routes: GET / aio.web.tests.handle_hello_web_world
  ... static_url: /static
  ... static_dir: /tmp/test_static/  
  ... """

  >>> import os  
  >>> os.mkdir("/tmp/test_static")

  >>> with open("/tmp/test_static/test.css", 'w') as cssfile:
  ...    res = cssfile.write("body {}")
  
  >>> def run_future_app():
  ...     yield from runner(['run'], config_string=CONFIG)
  ... 
  ...     @asyncio.coroutine
  ...     def _test_web():
  ...         response.body = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", "http://localhost:7070/static/test.css")).read()
  ... 
  ...     return _test_web
  
  >>> aiofuturetest(run_future_app, timeout=5, sleep=2)()  
  >>> response.body
  b'body {}'
   
  >>> import shutil
  >>> shutil.rmtree("/tmp/test_static")
  >>> import aio.app
  >>> aio.app.clear()

Templates
---------

Templates are found by searching the the __path__s of aio.app.modules folders named "templates"

  >>> CONFIG = """
  ... [aio]
  ... modules = aio.web.tests
  ... 
  ... [aio:commands]
  ... run: aio.app.cmd.cmd_run
  ... 
  ... [server:test]
  ... factory: aio.http.server.http_server
  ... root: aio.web.root
  ... address: 0.0.0.0
  ... port: 7070
  ... 
  ... [web:test]
  ... routes: GET / aio.web.tests.handle_hello_web_world
  ... """

  >>> def run_future_app():
  ...     yield from runner(['run'], config_string=CONFIG)

  >>> aiofuturetest(run_future_app, timeout=5, sleep=2)()

We can get the web app by name from the aio.web.apps var

  >>> import aio.web
  >>> webapp = aio.web.apps['test']
  >>> webapp
  <Application>

And use that to get the associated templates

  >>> import aiohttp_jinja2
  >>> aiohttp_jinja2.get_env(webapp).list_templates()
  ['test_template.html']


Aio web command
---------------

  >>> CONFIG = """
  ... [aio]
  ... modules = aio.web.tests
  ... 
  ... [aio:commands]
  ... web: aio.web.cmd.cmd_web
  ... """
  
With the above configuration you can run to collect static resources from listed modules

  # aio web static
