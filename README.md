# socket-eater

Can be used as an example of threaded socket server and client and also to exhast 
all client ports on a linux machine. 

## Usage
```
git clone https://github.com/adityaka/socket-eater
python3 <path>/socket-eater (the directory)
```
```
usage: socket-eater [-h] [-tp TCP_PORT] [-up UDP_PORT] [-tcc TCP_CLIENT_COUNT] [-ucc UDP_CLIENT_COUNT] [-d ENABLE_DEBUG]

optional arguments:
  -h, --help            show this help message and exit
  -tp TCP_PORT, --tcp-port TCP_PORT
                        Server side TCP port
  -up UDP_PORT, --udp-port UDP_PORT
                        Server side UDP port
  -tcc TCP_CLIENT_COUNT, --tcp-client-count TCP_CLIENT_COUNT
                        Number of tcp clients
  -ucc UDP_CLIENT_COUNT, --udp-client-count UDP_CLIENT_COUNT
                        Number of udp clients
  -d ENABLE_DEBUG, --debug ENABLE_DEBUG
```