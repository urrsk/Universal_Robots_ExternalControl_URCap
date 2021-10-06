# A simple python 3 server to test the External Control URCap
# The server answer request from the URCap with the context of the given file

import socket
import socketserver
import threading
import argparse

parser = argparse.ArgumentParser(description='Simple External Control server')
parser.add_argument("file", type=argparse.FileType(
    'w', encoding='latin-1'), help="UR script file to host")
parser.add_argument("-p", "--port", type=int,
                    default=50002, help="Port number to use")

args = parser.parse_args()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


class FileHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')
        file = open(args.file, "r")
        while True:
            data = file.read()

            print(data)
            if not data:
                break
            self.wfile.write(data.encode('utf-8'))
        print(f'Closed: {client}')


with ThreadedTCPServer(('', args.port), FileHandler) as server:
    print(f'The Simple External Control server is running on port', args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
