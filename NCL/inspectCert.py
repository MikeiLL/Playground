"""
Utilize these commands or modify file as needed to inspect Cert Authority certificate files and get info.
"""

from OpenSSL import crypto
import sys

cert_file = './ca.crt'
try:
    open(cert_file)
except FileNotFoundError:
    print("Coudn't open certificate file. Check the path.")
    sys.exit()
cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert_file).read())
subject = cert.get_subject()
issued_to = subject.CN    # the Common Name field
issuer = cert.get_issuer()
issued_by = issuer.CN
print(f"Certificate info Issued to: {subject.CN} by {issuer.CN}")
print("Copy ideas from the file to work interactively in the Python repl.")
