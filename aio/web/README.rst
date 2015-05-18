aio.web usage
-------------


Configuration
-------------

Let's create a config defining a factory method and using the aio.web.protocol_factory for the protocol

We can define routes for the web server in a corresponding [web:{name}] section

  >>> import asyncio
  >>> import aiohttp
  
  >>> def hello_world_handler(request):
  ...     return aiohttp.web.Response(body=b"Hello, web world")    

  >>> import aio.web
  >>> aio.web.tests._test_hello_world_handler = asyncio.coroutine(hello_world_handler)
  
  >>> config = """
  ... [aio:commands]
  ... run: aio.app.cmd.cmd_run
  ... 
  ... [server:test]
  ... factory: aio.http.server
  ... protocol: aio.web.protocol_factory
  ... port: 7070
  ... 
  ... [web:test]
  ... routes: GET / aio.web.tests._test_hello_world_handler
  ... """  

  >>> from aio.app.runner import runner  

  >>> def run_future_app():
  ...     yield from runner(['run'], config_string=config)
  ... 
  ...     @asyncio.coroutine
  ...     def _test_http():
  ...         result = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", "http://localhost:7070")).read()
  ... 
  ...         print(result)
  ... 
  ...     return _test_http

And run the test

  >>> from aio.testing import aiofuturetest
  >>> aiofuturetest(run_future_app, timeout=1, sleep=1)()  
  b'Hello, web world'

  
Accessing web apps
------------------

You can access a webapp by name

  >>> import aio.web
  >>> aio.web.apps['test']
  <Application>

  >>> aio.web.apps['test']['name']
  'test'

Let's clear the web apps

  >>> aio.web.clear()
  >>> aio.web.apps
  {}

  >>> import aio.app  
  >>> aio.app.clear()
  >>> del aio.web.tests._test_hello_world_handler  
  
  
Static directory
----------------

  >>> config_static = """
  ... [aio:commands]
  ... run: aio.app.cmd.cmd_run
  ... 
  ... [server:test]
  ... factory: aio.http.server
  ... protocol: aio.web.protocol_factory
  ... port: 7070
  ... 
  ... [web:test]
  ... static_url: /static
  ... static_dir: /tmp/test_static/  
  ... """

  >>> import os  
  >>> os.mkdir("/tmp/test_static")

  >>> with open("/tmp/test_static/test.css", 'w') as cssfile:
  ...    res = cssfile.write("body {}")
  
  >>> def run_future_app():
  ...     yield from runner(['run'], config_string=config_static)
  ... 
  ...     @asyncio.coroutine
  ...     def _test_web():
  ...         result = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", "http://localhost:7070/static/test.css")).read()
  ... 
  ...         print(result)
  ... 
  ...     return _test_web
  
  >>> aiofuturetest(run_future_app, timeout=1, sleep=1)()  
  b'body {}'
   
  >>> import shutil
  >>> shutil.rmtree("/tmp/test_static")
  >>> aio.web.clear()
  >>> aio.app.clear()
  

Templates
---------

Templates are found by searching the the __path__s of aio.app.modules folders named "templates"

  >>> import aiohttp_jinja2

  >>> def template_handler(request):
  ...     return {
  ...         'message': 'Hello, world'}

  >>> aio.web.tests._test_template_handler = (
  ...     aiohttp_jinja2.template('test_template.html')(template_handler))

  >>> config_template = """
  ... [aio]
  ... modules = aio.web.tests
  ... 
  ... [aio:commands]
  ... run: aio.app.cmd.cmd_run
  ... 
  ... [server:test]
  ... factory: aio.http.server
  ... protocol: aio.web.protocol_factory
  ... port: 7070
  ... 
  ... [web:test]
  ... routes: GET / aio.web.tests._test_template_handler
  ... """

  >>> def run_future_app():
  ...     yield from runner(['run'], config_string=config_template)
  ... 
  ...     @asyncio.coroutine
  ...     def _test_web():
  ...         result = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", "http://localhost:7070/")).read()
  ... 
  ...         print(result)
  ... 
  ...     return _test_web
  
  >>> aiofuturetest(run_future_app, timeout=1, sleep=1)()
  b'<html>\n  <body>\n    Hello, world\n  </body>\n</html>'

We can get the associated templates for the web app

  >>> webapp = aio.web.apps['test']

  >>> import aiohttp_jinja2
  >>> aiohttp_jinja2.get_env(webapp).list_templates()
  ['test_template.html']

  >>> aio.web.clear()
  >>> aio.app.clear()
  >>> del aio.web.tests._test_template_handler

