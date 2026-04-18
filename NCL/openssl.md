# OpenSSL and Pentesting Web

Looking at [hacktricks](https://hacktricks.wiki) came across this [pentesting-web post](https://hacktricks.wiki/en/network-services-pentesting/pentesting-web/index.html).

Here's a request to port 80:
```
nc -v obliteration.com 80
```
That is the `nc` utility:
```
NAME
     nc – arbitrary TCP and UDP connections and listens

DESCRIPTION
     The nc (or netcat) utility is used for just about anything under the sun
     involving TCP or UDP.  It can open TCP connections, send UDP packets,
     listen on arbitrary TCP and UDP ports, do port scanning, and deal with
     both IPv4 and IPv6.  Unlike telnet(1), nc scripts nicely, and separates
     error messages onto standard error instead of sending them to standard
     output, as telnet(1) does with some.

     Common uses include:

           •   simple TCP proxies
           •   shell-script based HTTP clients and servers
           •   network daemon testing
           •   a SOCKS or HTTP ProxyCommand for ssh(1)
           •   and much, much more
     ```

Here you can begin an ssl handshake from the commandline:
```
openssl s_client -connect obliteration.com:443
```

The `openssl` utility:

```
NAME
       openssl - OpenSSL command line program

DESCRIPTION
       OpenSSL is a cryptography toolkit implementing the Secure Sockets Layer
       (SSL) and Transport Layer Security (TLS) network protocols and related
       cryptography standards required by them.

       The openssl program is a command line program for using the various
       cryptography functions of OpenSSL's crypto library from the shell.  It
       can be used for

        o  Creation and management of private keys, public keys and parameters
        o  Public key cryptographic operations
        ```
