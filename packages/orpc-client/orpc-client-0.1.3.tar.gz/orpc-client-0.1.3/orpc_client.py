#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import struct
import socket

import msgpack
from zenutils import errorutils
from zenutils import packutils
from zenutils import funcutils
from zenutils import hashutils
from pooling import PoolBase

EVENT_FIELD = "event"
ARGS_FIELD = "args"
KWARGS_FIELD = "kwargs"

class OrpcConnectionPool(PoolBase):

    def do_session_create(self, *create_args, **create_kwargs):
        return OrpcConnection(*create_args, **create_kwargs)

    def do_session_destory(self, real_session):
        return real_session.close()

class OrpcConnection(object):

    def __init__(
            self,
            host="localhost",
            port=8392,
            username=None,
            password=None,
            password_hash_method=None,
            login_event=None,
            auto_login=False,
            buffer_size=4096,
            rfile_buffer_size=None,
            wfile_buffer_size=None,
            auto_connect=True,
            auto_reconnect=True,
            **options
            ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.password_hash_method = password_hash_method
        self.login_event = login_event
        self.auto_login = auto_login
        self.options = options
        self.buffer_size = buffer_size
        self.rfile_buffer_size = rfile_buffer_size or self.buffer_size
        self.wfile_buffer_size = wfile_buffer_size or self.buffer_size
        self.result_packer = packutils.RcmPacker()
        self.auto_connect = auto_connect
        self.auto_reconnect = auto_reconnect
        self._connection_closed = True
        self.__server = None
        self.__rfileobj = None
        self.__wfileobj = None
        if self.auto_connect:
            self.connect()
        if self.auto_login:
            self.login()

    def connect(self):
        if not self.__server:
            self.__server = socket.socket()
            self.__server.connect((self.host, self.port))
            self.__rfileobj = self.__server.makefile("rb", self.rfile_buffer_size)
            self.__wfileobj = self.__server.makefile("wb", self.wfile_buffer_size)
            self._connection_closed = False

    def close(self):
        if self.__server:
            self.__server.close()
        self._connection_closed = True

    def reconnect(self):
        self.close()
        self.connect()
        if self.auto_login:
            self.login()

    def login(self):
        if not self.username:
            raise errorutils.MissingConfigItem(item="username")
        if not self.password:
            raise errorutils.MissingConfigItem(item="password")
        if not self.login_event:
            raise errorutils.MissingConfigItem(item="login_event")
        if self.password_hash_method:
            password = hashutils.get_password_hash(self.password, self.password_hash_method)
        else:
            password = hashutils.get_password_hash(self.password)
        return self._execute(self.login_event, args=tuple([self.username, password]))

    def execute(self, method, args=None, kwargs=None):
        last_error = None
        if self._connection_closed:
            self.reconnect()
        for _ in range(2):
            try:
                return self._execute(method, args, kwargs)
            except (errorutils.SendRequestToServerError, errorutils.RecvServerResponseError, errorutils.ServerGoneAwayError) as error:
                last_error = error
                self.reconnect()
        raise last_error

    def _execute(self, method, args=None, kwargs=None):
        args = args or []
        kwargs = kwargs or {}
        request = {
            EVENT_FIELD: method,
            ARGS_FIELD: args,
            KWARGS_FIELD: kwargs,
        }
        request_bytes = msgpack.dumps(request)
        request_size = len(request_bytes)
        request_size_bytes = struct.pack(">I", request_size)
        try:
            self.__wfileobj.write(request_size_bytes)
            self.__wfileobj.write(request_bytes)
            self.__wfileobj.flush()
        except Exception as error:
            self._connection_closed = True
            raise errorutils.SendRequestToServerError("send request to server error: error_message={error}...".format(error=error))
        try:
            response_size_bytes = self.__rfileobj.read(4)
        except Exception as error:
            self._connection_closed = True
            raise errorutils.RecvServerResponseError("recv response length error: error_message={error}...".format(error=error))
        if not response_size_bytes:
            self._connection_closed = True
            raise errorutils.ServerGoneAwayError()
        response_size = struct.unpack(">I", response_size_bytes)[0]
        try:
            response_bytes = self.__rfileobj.read(response_size)
        except Exception as error:
            self._connection_closed = True
            raise errorutils.RecvServerResponseError("recv response body error: error_message={error}...".format(error=error))
        if not response_bytes:
            self._connection_closed = True
            raise errorutils.ServerGoneAwayError()
        response = msgpack.loads(response_bytes)
        return self.result_packer.unpack(response)

    def __getattr__(self, name):
        return funcutils.ChainableProxy(name, self._proxy_execute)
    
    def _proxy_execute(self, path, *args, **kwargs):
        return self.execute(path, args=args, kwargs=kwargs)
