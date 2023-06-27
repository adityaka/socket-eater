import socket
import select
from task_interface import RunTask
from applog import LoggerFactory

class SocketClient(RunTask):
    ALLOWED_TYPES=(0, 1)
    TYPE_TCP=0
    TYPE_UDP=1

    def __init__(self, type: int, s_address: str, s_port: int, **kwargs) -> None:
        self._logger = LoggerFactory.get("SocketClient")
        
        if not type  in SocketClient.ALLOWED_TYPES:
            raise ValueError("Invalid Protocol should TCP:0 or UDP:1")
        self._type = type
        self._socket = None
        self._s_address = s_address
        self._s_port = s_port
        super().__init__(**kwargs)

    def _initialize_socket(self):
        self._socket = socket.socket(socket.AF_INET,
                                     socket.SOCK_STREAM if self._type == SocketClient.TYPE_TCP else socket.SOCK_DGRAM,
                                     socket.IPPROTO_TCP if self._type == self.TYPE_TCP else socket.IPPROTO_UDP)
        if self._type == SocketClient.TYPE_TCP:
            try:
                self._socket.connect_ex((self._s_address, self._s_port))
            except Exception as e:
                self._socket.close()
                self._logger.error(str(e))
                self.shutdown()
                raise e

    def send(self):
        buffer= b"Sending Dummy Data from client"
        try:
            if self._type == SocketClient.TYPE_TCP:
                self._socket.sendall(buffer)
            else:
                self._socket.sendto(buffer, (self._s_address, self._s_port))
        except Exception as e:
            client_type =  "tcp" if self._type == SocketClient.TYPE_TCP else "udp"
            self._logger.error("Error while sending data {} ClientType : {}".format(str(e),client_type))
            self.shutdown()

    def recv(self):
        buffer= None
        try:
            if self._type == SocketClient.TYPE_TCP:
                buffer = self._socket.recv(512)
            else:
                buffer = self._socket.recvfrom(512)
        except Exception as e:
            self._logger.error(str(e))
        self._logger.debug("Received data from server {}".format(str(buffer)))
                

    def __call__(self):
        while(not self.shutdown_event.is_set()):
            if not self._socket:
                self._initialize_socket()
            r,w,e = select.select([self._socket],[], [],5)
            if w:
                self.send()
            if r:
                self.recv
            if e:
                self._logger.error("Socket error at client")
        self._socket.close()
    
                  

    

