"""sumary_line this file contains a simple python application which can create
client or ephemeral port exhaustion

Keyword arguments:
argument -- description
Return: return_description
"""

import logging
import os.path as path
from typing import Type
import socketserver
from applog import LoggerFactory
from task_interface import RunTask 

class TCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        data = self.request.recv(4096)
        LoggerFactory.get("TCPRequestHandler").debug("Server Received Data {}".format(str(data.strip())))
        try:
            self.request.sendall(bytes("Got Data ".format(str(len(data))), "ascii", "none"))
        except Exception as e:
            LoggerFactory.get("TcpRequestHandler").error(str(e))
        #return super().handle()
    
class UDPRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self) -> None:
        data = self.request[0].strip()
        sock = self.request[1]
        LoggerFactory.get("UDPRequestHandler").debug("Server Received Data {}".format(str(data.strip())))
        try:
            sock.sendto(bytes("Got Data ".format(str(len(data))), "ascii","none"), self.client_address)
        except Exception as e:
            LoggerFactory.get("UDPRequestHandler").error(str(e))
        #return super().handler() 

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class ServerTask(RunTask):
    ALLOWED_TYPES = ("tcp", "udp")
    TYPE_TCP=0
    TYPE_UDP=1

    def __init__(self, type:int, port :int, listen_address :str=None,**kwargs):
        
        self._logger = LoggerFactory.get("ServerTask")
        if port < 0 or port > 65535:
            raise ValueError("{} is an invalid port".format(port))
        self._listen_on_address = ("0.0.0.0", self._port) if not listen_address else (listen_address, port)
        if type == self.TYPE_TCP:
            self._server = ThreadedTCPServer(self._listen_on_address, TCPRequestHandler)
        elif type == self.TYPE_UDP:
            self._server = ThreadedUDPServer(self._listen_on_address, UDPRequestHandler)
        else:
            raise ValueError("Protocol should be either TCP == 0 or UDP == 1")
        self._type = type
        self._logger.info("Created {} server listening on {} port {} ".format(self.ALLOWED_TYPES[type], listen_address, str(port)))
        super(ServerTask, self).__init__(**kwargs)

    def shutdown(self):
        self._logger.info("Shutting down server {}".format(self.ALLOWED_TYPES[self._type]))
        self._server.shutdown()
        super().shutdown()

    def __call__(self):
        try:
            self._logger.info("Serving for {} server".format(self.ALLOWED_TYPES[self._type]))
            self._server.serve_forever()
        except Exception as e:
            self._logger.error("Error occurred {}".format(str(e)))
            raise e




        




