#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import uuid
import logging

import msgpack
from zenutils import errorutils
from zenutils import socketserverutils
from zenutils import packutils

from gevent.server import StreamServer
from daemon_application import SimpleRpcApplication
from orpc_client import EVENT_FIELD
from orpc_client import ARGS_FIELD
from orpc_client import KWARGS_FIELD


_logger = logging.getLogger(__name__)


class OrpcExchangeProtocol(socketserverutils.NStreamExchangeProtocolBase):

    def setup(self):
        socketserverutils.NStreamExchangeProtocolBase.setup(self)
        self.result_packer = packutils.RcmPacker()
        self.authenticated = False
        self.authentication_enabled = self.config.select("authentication.enable", False)
        self.authentication_event = self.config.select("authentication.event", None)

    def get_request(self):
        request_bytes = socketserverutils.NStreamExchangeProtocolBase.get_request(self)
        try:
            request = msgpack.loads(request_bytes)
        except Exception as error:
            raise errorutils.InformalRequestError("Informal request, error={error}".format(error=error))
        if not isinstance(request, dict):
            raise errorutils.InformalRequestError("Request type error...")
        return request

    def dispatch(self, request):
        _logger.debug("dispatching request, request={request}...".format(request=request))
        logid = uuid.uuid4().hex
        event = request.get(EVENT_FIELD, None)
        args = tuple(request.get(ARGS_FIELD, []))
        kwargs = request.get(KWARGS_FIELD, {})
        try:
            if not event:
                raise errorutils.InformalRequestError("Missing {field} field...".format(field=EVENT_FIELD))
            if (not self.authenticated) and self.authentication_enabled and (self.authentication_event != event):
                raise errorutils.AuthenticationRequired()
            func = self.server_engine.get_service(event)
            if not func:
                raise errorutils.EventNotRegistered(event=event)
            if self.authentication_event == event:
                kwargs["_protocol_instance"] = self
            _logger.debug("orpc event start: logid={logid}, event={event}, args={args}, kwargs={kwargs}...".format(logid=logid, event=event, args=args, kwargs=kwargs))
            result = func(*args, **kwargs)
            _logger.debug("orpc event done: logid={logid}, result={result}.".format(logid=logid, result=result))
            return self.result_packer.pack_result(result)
        except Exception as error:
            _logger.info("orpc do event failed: logid={logid}, event={event}, args={args}, kwargs={kwargs}, error={error}...".format(
                logid=logid,
                event=event,
                args=args,
                kwargs=kwargs,
                error=error
            ))
            return self.result_packer.pack_error(error)

    def send_response(self, response):
        response_bytes = msgpack.dumps(response)
        return socketserverutils.NStreamExchangeProtocolBase.send_response(self, response_bytes)


class OrpcServerEngine(socketserverutils.ServerEngineBase):

    def make_core_server(self):
        listen = self.config.select("server.listen", None)
        port = self.config.select("server.port", None)
        if not listen:
            raise errorutils.MissingConfigItem(item="server.listen")
        if not port:
            raise errorutils.MissingConfigItem(item="server.port")
        backlog = self.config.select("server.backlog", 8192)
        self.server_handle = socketserverutils.ServerHandle(self, self.config, OrpcExchangeProtocol)
        return StreamServer((listen, port), handle=self.server_handle, backlog=backlog)


class SimpleOrpcApplication(SimpleRpcApplication):
    default_server_port = 8392
    default_server_engine_class = "orpc.OrpcServerEngine"


simple_orpc_application = SimpleOrpcApplication().get_controller()


if __name__ == "__main__":
    simple_orpc_application()
