#!/usr/bin/env python3

# -- BEGIN LICENSE BLOCK ----------------------------------------------
# Copyright 2021 Universal Robots A/S
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# All source code contained in and/or linked to in this message (the “Source Code”) is subject to the copyright of
# Universal Robots A/S and/or its licensors. THE SOURCE CODE IS PROVIDED “AS IS” WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING – BUT NOT LIMITED TO – WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR
# NONINFRINGEMENT. USE OF THE SOURCE CODE IS AT YOUR OWN RISK AND UNIVERSAL ROBOTS A/S AND ITS LICENSORS SHALL, TO THE
# MAXIMUM EXTENT PERMITTED BY LAW, NOT BE LIABLE FOR ANY ERRORS OR MALICIOUS CODE IN THE SOURCE CODE, ANY THIRD-PARTY
# CLAIMS, OR ANY OTHER CLAIMS AND DAMAGES, INCLUDING INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL OR PUNITIVE DAMAGES,
# OR ANY LOSS OF PROFITS, EXPECTED SAVINGS, OR REVENUES, WHETHER INCURRED DIRECTLY OR INDIRECTLY, OR ANY LOSS OF DATA,
# USE, GOODWILL, OR OTHER INTANGIBLE LOSSES, RESULTING FROM YOUR USE OF THE SOURCE CODE. You may make copies of the
# Source Code for use in connection with a Universal Robots or UR+ product, provided that you include (i) an
# appropriate copyright notice (“©  [the year in which you received the Source Code or the Source Code was first
# published, e.g. “2021”] Universal Robots A/S and/or its licensors”) along with the capitalized section of this notice
# in all copies of the Source Code. By using the Source Code, you agree to the above terms. For more information,
# please contact legal@universal-robots.com.
# -- END LICENSE BLOCK ------------------------------------------------

# A simple python 3 server to test the External Control URCap
# The server answer request from the URCap with the context of the given file

import socket
import socketserver
import threading
import argparse

parser = argparse.ArgumentParser(description='Simple External Control server')
parser.add_argument("file", type=str, help="Path to the UR script file, which will be send to the robot")
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
