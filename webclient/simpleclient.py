"""
Barebones http request
run something locally on port 4000
 """
import socket

sock = socket.socket()
sock.connect(("127.0.0.1", 4000))
sock.send(b"GET / HTTP/1.0\r\n\r\n")
""" to send headers send before the blank line
indicated by \n\r\n
eg
GET / HTTP/1.0\r\nHost: sitename.com\r\n\r\n
 """
print(sock.recv(1024).decode())
