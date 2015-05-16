aio.web
=======


Installation
------------

Install with:

``
  pip install aio.web
``

Configuration
-------------

Example configuration for a hello world server

``
[aio:commands]
run: aio.app.cmd.cmd_run

[server:test]
factory: aio.http.server.http_server
root: aio.web.root
address: 0.0.0.0
port: 7070

[web:test]
routes: GET / aio.web.tests.handle_hello_web_world
``


Running
-------

Run with the aio command

``
   aio run
``

See [aio.app](http://github.com/phlax/aio.app) for more information on the "aio run" command
