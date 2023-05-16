#!/usr/bin/env python3
"""
    An example python file that simulates an EUT controller device
    This script can receive events from RadiMation and respond to the EUTINFO? request
"""
__author__ = "Raditeq"
__copyright__ = "Copyright (C) 2023 Raditeq"
__license__ = "MIT"

import socket
import threading

responses = {
    "Humidity": "70%",
    "Temperature": "20c",
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

        print(f"Server started on {self.host}:{self.port}...")

        # Accept incoming connections
        self.is_running = True

        while self.is_running and self.server_socket:
            try:
                conn, addr = self.server_socket.accept()
                print(f"Connected by {addr}")

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
        data = ""
        data_size = 1

        while data_size > 0:
            data = self.readline(conn)
            data_size = len(data)
          
            # Check if data was received
            if data_size > 0 and data:
                if "TESTINFO?" in data:
                    # remove newline characters
                    data = data.strip("\n").strip("\r")
                    
                    # send the response back for the TESTINFO? request
                    response = ""
                    for key, value in responses.items():
                        response = f"{key}={value}\r\n"
                        if len(response) > 0:
                            print(f"sending: {response}")
                            conn.send(response.encode())
                else:
                    # process the data from here
                    print("Received data:", data)

            data = ""

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
    
    # Keep the main thread running to prevent the script from exiting
    while True:
        try:
            pass
        except KeyboardInterrupt:
            server.stop()
            break
        except Exception:
            break
            
    input("press any key")
