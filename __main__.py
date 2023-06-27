import logging
import argparse
from applog import LoggerFactory
from server import ServerTask
from client import SocketClient
from application import Application
from dnstest import DnsClientTask
__appname__ = "socket-eater"

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-tp", "--tcp-port", dest="tcp_port", type=int, default=55550, help="Server side TCP port")
    parser.add_argument("-up", "--udp-port", dest="udp_port", type=int, default=55550, help="Server side UDP port")
    parser.add_argument("-tcc","--tcp-client-count", dest="tcp_client_count", type=int, default=50, help="Number of tcp clients")
    parser.add_argument("-ucc","--udp-client-count", dest="udp_client_count", type=int, default=50, help="Number of udp clients")
    parser.add_argument("-d","--debug", dest="enable_debug", type=bool, default=False)
    return parser

if __name__ == "__main__":
    logger_name = __appname__
    log_file_name  = logger_name + ".log"
    log_handler = logging.FileHandler(log_file_name)
    log_formatter = logging.Formatter("%(asctime)s | %(process)d | %(thread)d | %(module)s | %(name)s| %(levelname)s | %(funcName)s | %(lineno)d | %(message)s")
    log_handler.setFormatter(log_formatter)
    logger = LoggerFactory.get(logger_name, log_handler)
    parser = setup_parser()
    args = parser.parse_args()
    if args.enable_debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.info("Starting a new session of {}".format(__appname__))
    server_tasks = [ServerTask(ServerTask.TYPE_TCP, args.tcp_port, "0.0.0.0"), ServerTask(ServerTask.TYPE_UDP, args.udp_port, "0.0.0.0")]
    tcp_client_tasks = [ SocketClient(SocketClient.TYPE_TCP, "127.0.0.1", args.tcp_port) for tt in range(args.tcp_client_count) ]
    udp_client_tasks = [ SocketClient(SocketClient.TYPE_UDP, "127.0.0.1", args.udp_port) for tt in range(args.udp_client_count) ]
    dns_resolver_tasks = [DnsClientTask(x) for x in ["www.google.com", "ns1.com","amazon.in"] ]
    tasks = server_tasks + tcp_client_tasks + udp_client_tasks + dns_resolver_tasks
    app = Application(logger, tasks)
    app()
    logger.info("Bye Bye!!")