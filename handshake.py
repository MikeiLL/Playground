import socket
import ssl
import pprint
"""
https://docs.python.org/3.12/library/ssl.html
"""

hostname = 'www.python.org'
#context = ssl.create_default_context()

# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
ssl.get_server_certificate((hostname,443))

""" with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version()) """
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# probabaly installed via openssl and/or homebrew
context.load_verify_locations('/usr/local/etc/openssl@3/certs/cacert.pem')
sock=socket.create_connection((hostname, 443))
ssock=context.wrap_socket(sock, server_hostname=hostname) # <- asymmetric handshake happens here. session key agreed upon
print('version: ', ssock.version())
print('cypher: ', ssock.cipher())
pprint.pprint(ssock.getpeercert())
# interesting? https://medium.com/@cumulus13/building-bulletproof-ssl-tls-connections-in-python-a-developers-guide-to-secure-socket-4cb1c2d9544e

# Send an HTTP GET request
request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
ssock.sendall(request.encode('utf-8')) # fully encrypted symmetrically with session key
#response = ssock.recv(1048)  # Buffer size of 1048 bytes 2**10 (2**12 = 4096)
#print(response.decode('utf-8'))
#NOTE: When the connect completes, the socket s can be
#used to send in a request for the text of the page.
# The same socket will read the reply, and then be destroyed.
# That’s right, destroyed. Client sockets are normally only
# used for one exchange (or a small set of sequential exchanges).
#   https://docs.python.org/3.15/howto/sockets.html

#buf=bytearray(1024)
#bytes_received = ssock.recv_into(buf)
#print(f'Received {bytes_received} bytes: {buf[:bytes_received].decode()}')
buf=b''
# While we don't have "\r\n\r\n" in the buffer:
while not b"\r\n\r\n" in buf:
  buf+=ssock.recv(2**12)

summary, buf = buf.split(b"\r\n", 1) # get just first line with HTTP\ status
header, buf = buf.split(b"\r\n\r\n", 1) # rnrn indicates end of header
headers = {}
for h in header.split(b"\r\n"):
  key, val = h.split(b": ", 1) # MAXSPLIT 1 same as above
  key = key.decode()
  try: val = val.decode()
  except UnicodeDecodeError: pass
  headers[key.lower()] = val

contentlength = int(headers["content-length"])
# Read more text from socket and append to buffer
# Then split buffer on "\r\n\r\n", taking what's before
# it as the headers, and what's after it as the buffer
# Look for "Content-Length" header
# Read until the buffer has that many bytes
# That is your body
while len(buf) < contentlength:
  buf+=ssock.recv(2**12) # up to this month

#In theory you could clear the buffer and make another request eg
#body, buf = buf[:contentlength], buf[contentlength:]
#notice header "connection" likely to be "keep-alive" (or Keep-Alive)
import bs4 # Beautiful Soup
soup = bs4.BeautifulSoup(buf)

# note that closing the SSLSocket will also close the underlying socket
ssock.close()

# openssl ciphers -V
