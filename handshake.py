import socket
import ssl
import pprint
"""
https://docs.python.org/3.12/library/ssl.html
"""

hostname = 'www.python.org'
#context = ssl.create_default_context()

""" with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version()) """
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# probabaly installed via openssl and/or homebrew
context.load_verify_locations('/usr/local/etc/openssl@3/certs/cacert.pem')
sock=socket.create_connection((hostname, 443))
ssock=context.wrap_socket(sock, server_hostname=hostname)
print(ssock.version())
# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname

ssl.get_server_certificate((hostname,443))

pprint.pprint(ssock.getpeercert())
# note that closing the SSLSocket will also close the underlying socket
ssock.close()

# openssl ciphers -V
