# Mastering Post-Handshake Client Verification in Python's SSL
## (src: https://runebook.dev/en/docs/python/library/ssl/ssl.SSLSocket.verify_client_post_handshake)

This method is part of Python's built-in `ssl` module, which provides a secure, encrypted network
communication layer over sockets (TLS/SSL).

Essentially, `verify_client_post_handshake()` is a function used by the server side of a TLS connection to check
the client's certificate after the initial SSL/TLS handshake is complete.

Normally, client certificate verification (where the server verifies the client's identity using a certificate)
is done during the initial handshake. However, there are a few reasons you might want to do it later

**Delayed Authentication (Opportunistic TLS)**:<br> The server might allow the connection to establish without a
client certificate initially, and then later request and verify one, perhaps only when the client tries to access
a restricted resource.

**Protocol-Level Negotiation**:<br> Some protocols or specific TLS extensions allow for a new handshake or certificate
request after the connection is running.

**Performance**:<br> Separating the certificate verification from the main handshake can sometimes streamline the
initial connection process.

This method explicitly asks the underlying TLS library (OpenSSL) to request and verify the client's certificate
at that moment in the already established secure connection.

Using this method can sometimes lead to tricky situations. Here are some common pitfalls

This is the most direct problem. If the client doesn't present a certificate, or the certificate it presents is
invalid, expired, or not trusted by the server's configured Certificate Authority (CA) bundle, this method will
raise an `ssl.SSLError`.

**Problem**:<br> The server fails to verify the client's certificate.

Fix Tip

**Check the Client**:<br> Ensure the client is configured to send its certificate (with a private key) and that the
server's `SSLContext` is set up correctly (e.g., `context.verify_mode` is set, and
`context.load_verify_locations()` trusts the client's CA).


**Certificate Validity**:<br> Check that the client certificate hasn't expired and that the clock on both the client
and server is correct.

If the client isn't expecting the server to suddenly request a certificate post-handshake, its own socket
handling might not be set up to respond correctly, leading to a hang or timeout on both sides.

**Problem**:<br> The client doesn't know how to respond to the server's certificate request.

**Fix Tip**:<br> Ensure the client-side logic anticipates and handles the post-handshake authentication request, which
might involve calling an equivalent function or simply having the necessary certificate material configured on its
socket.

The server's `SSLContext` must be prepared to request client certificates, even if the actual
verification is deferred.

**Problem**:<br> The server context isn't set up for client authentication.

**Fix Tip**:<br> You typically need to set the server's `SSLContext` with something like
`context.verify_mode = ssl.CERT_REQUIRED` and use `context.load_cert_chain()` for the
server's own certificate and `context.load_verify_locations()` to tell the server which CAs to trust
for client certificates.


For most standard applications, you often don't need post-handshake verification. The most common alternative is
to perform mandatory verification during the initial handshake, which is simpler and often preferred for strict
security.

If you always need client authentication, configure it in the `SSLContext` so verification happens
automatically during the initial connection.

This server code requires a client certificate during the initial handshake.

```python
import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

# 1. Create a secure context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

# 2. Load the server's certificate and private key
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# 3. Configure to require and verify the client certificate
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile="client_ca.crt") #   CA that signed client's cert

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.bind((HOST, PORT))
  sock.listen(5)
  print(f"Server listening on {HOST}:{PORT}")

while True:
  conn, addr = sock.accept()
  try:
    # Wrap the socket. Handshake (and client verification) happens here.
    ssock = context.wrap_socket(conn, server_side=True)

    # If verification failed, an SSLError would have been raised here.
    print(f"Secure connection established with client:{addr}")

    # Get the verified peer certificate
    client_cert = ssock.getpeercert()
    print("Client Certificate details:", client_cert.get('subject'))

    ssock.sendall(b"Hello, Verified Client!")

  except ssl.SSLError as e:
    print(f"SSL/TLS Error (Client Verification Failed): {e} ")
  finally:
    if 'ssock' in
      locals():
      ssock.close()
      conn.close()
```
___

If you do need to use the post-handshake feature, here's how you might integrate it on the server side

This server code allows the initial connection, but then explicitly calls the verification later.


```python
import socket
import ssl

HOST = '127.0.0.1'
PORT = 8444

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

# Load server cert/key
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Set the context to require client certs, but verification is NOT mandatory at handshake.
# This makes client auth possible, but we'll trigger it manually.
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile="client_ca.crt")
context.session_timeout = 300 # Often good practice

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.bind((HOST, PORT))
  sock.listen(5)
  print(f"Server listening for post-handshake auth on {HOST}:{PORT}")

  conn, addr = sock.accept()
  try:
  # Initial Handshake (verification not performed yet)
  ssock = context.wrap_socket(conn, server_side=True)
  print(f"Initial secure connection established with {addr}")

  # --- IMPORTANT STEP: Manual Post-Handshake Verification ---
  print("Requesting and verifying client certificate...")
  ssock.verify_client_post_handshake() # & --- This is the method in question!

  # If the line above succeeds, the client is verified.
  client_cert = ssock.getpeercert()
  print(" Client Verified Post-Handshake!")
  print("Client Certificate details:", client_cert.get('subject'))

  ssock.sendall(b"Access Granted. Hello, verified client!")

  except ssl.SSLError as e:
    print(f" Post-Handshake Verification Failed: {e}")
    ssock.sendall(b"Access Denied: Certificate check failed.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  finally:
    if 'ssock' in
      locals():
      ssock.close()
      conn.close()
```

Remember, for either of these examples to run, you'll need the necessary certificate files
(`server.crt`, `server.key`, `client_ca.crt`) which you'd typically generate
using tools like OpenSSL for testing.

NOTE: This also looks useful: [here](https://www.py4u.org/blog/python-requests-ssl-handshake-failure/) check output of the following:<br>
`openssl s_client -connect example.com:443 -tls1_3` the output will include
something like `Protocol: TLSv1.3` and `New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384`
then in Python you can:
```python
import ssl
client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
print(ssl.OPENSSL_VERSION, sboy.get_ciphers(), sep='\n')
client_context.minimum_version = ssl.TLSVersion.TLSv1_3
client_context.maximum_version = ssl.TLSVersion.TLSv1_3
cyphers = client_context.get_ciphers()
print(cyphers)
sslcontext.load_default_certs()
```
(TLS 1.3 uses a disjunct set of cipher suites. All AES-GCM and ChaCha20 cipher suites are enabled by default. The method SSLContext.set_ciphers() cannot enable or disable any TLS 1.3 ciphers yet, but SSLContext.get_ciphers() returns them. [python ssl docs](https://docs.python.org/3/library/ssl.html#tls-1-3))

The [python ssl class](https://docs.python.org/3/library/ssl.html) is a wrapper for [python socket](https://docs.python.org/3/library/socket.html) which is very interesting as well:<br>
```python
>>> import socket
>>> socket.getaddrinfo("wikipedia.org", 80, proto=socket.IPPROTO_TCP)
[(<AddressFamily.AF_INET6: 30>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('2620:0:861:ed1a::1', 80, 0, 0)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('208.80.154.224', 80))]
>>> socket.getaddrinfo("wikipedia.org", 443, proto=socket.IPPROTO_TCP)
[(<AddressFamily.AF_INET6: 30>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('2620:0:861:ed1a::1', 443, 0, 0)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('208.80.154.224', 443))]
```

```python
from pathlib import Path
import ssl

# Define paths relative to the current script file

CERT_DIR = Path(__file__).parent / "certs"
CERT_PATH = CERT_DIR / "server.pem"
KEY_PATH = CERT_DIR / "key.pem"

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
try:
  context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)
  print("Paths confirmed and files loaded.")
except FileNotFoundError as e:
  print(f"File not found. Check path: {e.filename}")
```

Get current path:

```python
from pathlib import Path
import os
os.getcwd()
#or
Path.cwd()
#or within a file
dir_path = os.path.dirname(os.path.realpath(__file__))

```

[Python cryptography library](https://cryptography.io/en/latest/) and its "dangerous" [serialization](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/) class look interesting
