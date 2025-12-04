"""
An http request to rosuav.com
with a secure socket connection
 """
import socket
import ssl

ctx = ssl.create_default_context()
# sikorsky6 for IPv6 and sikorsky4 for IPv4
with socket.create_connection(("sikorsky6.mustardmine.com", 443)) as sock:
  with ctx.wrap_socket(sock, server_hostname="sikorsky6.mustardmine.com") as sock:
    # now we make an SSL handshake, (because cert-required is the default) checking
    # response encryption keys
    # against local ssl certificate authority file cacert.pem or something
    sock.send(b"GET /404 HTTP/1.0\r\n\r\n")
    print(sock.recv(1024).decode()) # get 1024 bytes (up to 1KB)
    """
    HTTP/1.0 404 No such file or directory.
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Private-Network: true
    Connection: close
    Link: <https://mustardmine.com/404>; rel="canonical"
    Content-Type: text/plain; charset="UTF-8"
    Content-Length: 14
    Server: Pike v9.0 release 10: HTTP Server module
    Date: Thu, 04 Dec 2025 15:18:53 GMT
    Last-Modified: Thu, 04 Dec 2025 15:18:53 GMT

    No such page.

    """
    """ This is a content length of 14 (after the headers)
    And an actually URL handling library would loop through larger content
    """
