aio.web usage
-------------


Configuration
-------------

Let's create a config defining a factory method and using the aio.web.protocol for the protocol

We can define routes for the web server in a corresponding [web/{name}] section

  >>> web_server_config = """
  ... [aio]
  ... log_level: ERROR
  ... 
  ... [server/test]
  ... factory = aio.http.server
  ... protocol = aio.web.protocol
  ... port: 7070
  ... 
  ... [web/test]
  ... routes: GET / aio.web.tests._example_handler
  ... """  

  >>> import asyncio
  >>> import aiohttp
  >>> import aio.web.tests
  >>> from aio.app.runner import runner    
  >>> from aio.testing import aiofuturetest

  >>> def handler(request):
  ...     return aiohttp.web.Response(body=b"Hello, web world")    

  >>> aio.web.tests._example_handler = asyncio.coroutine(handler)
  
  >>> def run_web_server(config, request_page="http://localhost:7070"):
  ...     yield from runner(['run'], config_string=config)
  ... 
  ...     @asyncio.coroutine
  ...     def call_web_server():
  ...         result = yield from (
  ...             yield from aiohttp.request(
  ...                "GET", request_page)).read()
  ... 
  ...         print(result.decode())
  ... 
  ...     return call_web_server

  >>> aiofuturetest(run_web_server, sleep=1)(web_server_config)  
  Hello, web world

  
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
  
  
Static directory
----------------

The "web/" section takes a static_url and a static_dir option for hosting static files

  >>> config_static = """
  ... [aio]
  ... log_level: ERROR
  ... 
  ... [server/test]
  ... factory: aio.http.server
  ... protocol: aio.web.protocol
  ... port: 7070
  ... 
  ... [web/test]
  ... static_url: /static
  ... static_dir: /tmp/test_static/  
  ... """

  >>> import os  
  >>> os.mkdir("/tmp/test_static")

  >>> with open("/tmp/test_static/test.css", 'w') as cssfile:
  ...    res = cssfile.write("body {}")
  
  >>> aiofuturetest(run_web_server, sleep=1)(
  ...     config_static,"http://localhost:7070/static/test.css")  
  body {}

And clear up...

  >>> import shutil
  >>> shutil.rmtree("/tmp/test_static")
  >>> aio.web.clear()
  >>> aio.app.clear()
  

Templates
---------

aio.web uses jinja2 templates

Add any modules containing templates to the [aio] modules option

  >>> config_template = """
  ... [aio]
  ... modules = aio.web.tests
  ... log_level: ERROR
  ... 
  ... [server/test]
  ... factory: aio.http.server
  ... protocol: aio.web.protocol
  ... port: 7070
  ... 
  ... [web/test]
  ... routes: GET / aio.web.tests._example_template_handler
  ... """

  >>> import aiohttp_jinja2

  >>> def template_handler(request):
  ...     return {
  ...         'message': 'Hello, world'}

  >>> aio.web.tests._example_template_handler = (
  ...     aiohttp_jinja2.template('test_template.html')(template_handler))
  
  >>> aiofuturetest(run_web_server, sleep=1)(config_template)
  <html>
    <body>
      Hello, world
    </body>
  </html>
	
We can get the associated templates for the web app

  >>> webapp = aio.web.apps['test']

  >>> import aiohttp_jinja2
  >>> aiohttp_jinja2.get_env(webapp).list_templates()
  ['test_template.html']

  >>> aio.web.clear()
