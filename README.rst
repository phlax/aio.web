aio.web
=======

Web server for the aio_ asyncio framework

.. _aio: https://github.com/phlax/aio



Build status
------------

.. image:: https://travis-ci.org/phlax/aio.web.svg?branch=master
	       :target: https://travis-ci.org/phlax/aio.web


Installation
------------
Install with:

.. code:: bash

	  pip install aio.web


Configuration
-------------

Example configuration for a hello world web page

.. code:: ini

	  [aio:commands]
	  run = aio.app.cmd.cmd_run

	  [server:test]
	  factory = aio.http.server
	  protocol = aio.web.protocol_factory
	  port = 8080

	  [web:test]
	  routes: GET / my.example.handler


And the corresponding handler

.. code:: python

	  import asyncio
	  import aiohttp

	  @asyncio.coroutine
	  def hello_world_handler(request):
	      return aiohttp.web.Response(body=b"Hello, web world")


Running
-------

Run with the aio command

.. code:: bash

	  aio run

