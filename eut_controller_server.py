#!/usr/bin/env python3
"""
    An example python file that simulates an EUT controller device
    This script can receive events from RadiMation and respond to the TESTINFO? request
"""
__author__ = "Raditeq"
__copyright__ = "Copyright (C) 2023 Raditeq"
__license__ = "MIT"

import socket
import threading

responses = {
    "Humidity": "70%",
    "Temperature": "21.3 degrees Celcius",
    "Pressure": "1013.25 hPa",
    "Operating Mode": "Data from eut controller server",
    "Company": "Raditeq",
    "Version": "1.0",
}

class TCPServer:
    def __init__(self, host='', port=58426):
        """Constructor for the TCPServer"""
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False

    def start(self):
        """Start a server socket and listen for incoming connections"""

        # Create a TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the host and port
        self.server_socket.bind((self.host, self.port))

        # Start listening for incoming connections
        self.server_socket.listen()

        host, port = self.server_socket.getsockname()
        print(f"Server started on {host}:{port}.")

        # Accept incoming connections
        self.is_running = True

        try:
            while self.is_running and self.server_socket:
                conn, addr = self.server_socket.accept()
                print(f"Connected from {addr[0]}:{addr[1]}.")

                # Create a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client_request, args=(conn,addr))
                client_thread.start()
        except:
            pass

    def stop(self):
        """Stop the server socket"""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            
        print("Server stopped by user.")

    def handle_client_request(self, conn, addr):
        """This method will handle the client request"""
        data = self.readline(conn)
        while data:
            # Data was received
            # remove newline characters
            data = data.strip("\r\n")
            # process the data from here
            print(f"Received data: {data}")
            if "TESTINFO?" in data:
                # send the response back for the TESTINFO? request
                for key, value in responses.items():
                    response = f"TESTINFO {key}={value}"
                    print(f"Sending data: {response}")
                    conn.send((response + '\n').encode())
            # Read new data
            data = self.readline(conn)

    def readline(self, conn):
        """Read a single line from the socket connection"""
        data = ""
        # We do not clear the data
        # we append every character, and once we found a match
        # we will clear the data
        foundTerminator = False
        while not foundTerminator:
            try:
                read_data = conn.recv(1)
                if len(read_data) == 0:
                    # No data received
                    # ending the connection
                    foundTerminator = True
                else:
                    data += read_data.decode()
                    if read_data.decode() == '\n':
                        foundTerminator = True
            except socket.error:
                data = ""
                foundTerminator = True

        return data

if __name__ == '__main__':
    # Create a new instance of the TCPServer class
    server = TCPServer()

    # Start the server on a new thread
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    
    try:
        input("\nPress [Enter] to close.\n\n")
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
    finally:
        server.stop()
