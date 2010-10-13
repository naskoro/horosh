WebHelpers 1.2 - не грузится форма логина:

::
    ----------------------------------------
    Exception happened during processing of request from ('127.0.0.1', 43439)
    Traceback (most recent call last):
      File "/home/naspeh/.virtualenvs/horosh2/lib/python2.6/site-packages/paste/httpserver.py", line 1068, in process_request_in_thread
        self.finish_request(request, client_address)
      File "/usr/lib/python2.6/SocketServer.py", line 322, in finish_request
        self.RequestHandlerClass(request, client_address, self)
      File "/usr/lib/python2.6/SocketServer.py", line 617, in __init__
        self.handle()
      File "/home/naspeh/.virtualenvs/horosh2/lib/python2.6/site-packages/paste/httpserver.py", line 442, in handle
        BaseHTTPRequestHandler.handle(self)
      File "/usr/lib/python2.6/BaseHTTPServer.py", line 329, in handle
        self.handle_one_request()
      File "/home/naspeh/.virtualenvs/horosh2/lib/python2.6/site-packages/paste/httpserver.py", line 437, in handle_one_request
        self.wsgi_execute()
      File "/home/naspeh/.virtualenvs/horosh2/lib/python2.6/site-packages/paste/httpserver.py", line 290, in wsgi_execute
        self.wsgi_write_chunk(chunk)
      File "/home/naspeh/.virtualenvs/horosh2/lib/python2.6/site-packages/paste/httpserver.py", line 150, in wsgi_write_chunk
        self.wfile.write(chunk)
      File "/usr/lib/python2.6/socket.py", line 310, in write
        data = str(data) # XXX Should really reject non-string non-buffers
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 270-273: ordinal not in range(128)
    ----------------------------------------
