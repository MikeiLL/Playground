# Identifying Cryptographic Hash Types by Sight

original source: [pete on software com](https://www.peteonsoftware.com/index.php/2024/10/03/identifying-cryptographic-hashes)

## Hash lengths:

- MD5: 32 hexadecimal characters (128 bits).
- SHA-1: 40 hexadecimal characters (160 bits).
- SHA-256: 64 hexadecimal characters (256 bits).
- SHA-512: 128 hexadecimal characters (512 bits).
- bcrypt: Typically around 60 characters (includes a salt).

## Formatting Signature

### bcrypt hashes often start with $2a$, $2b$, or $2y$.

In a Linux `/etc/shadow` passwd file the prefix format is: `$id$salt$hashed`

- `$1$` is MD5
- `$2a$` is Blowfish
- `$2y$` is Blowfish
- `$5$` is SHA-256
- `$6$` is SHA-512
- `$y$` is yescrypt

**NOTE**: Bcrypt is a password-hashing function _based on_ the Blowfish cipher, designed to securely store passwords by incorporating salting and a computationally intensive process to resist brute-force attacks. While Blowfish is a general-purpose encryption algorithm, bcrypt specifically focuses on password security.

- **MD5** is typically a straightforward 32-character hexadecimal string.
- **NTLM** (used in Windows environments) often has a 32-character hexadecimal format similar to MD5 but with a central colon `:` is distinct in purpose. They are susciptable to rainbow table bruteforcing with a tool like ophcrack.

## Context

**Password Databases**: If you’re analyzing a password database, it’s common to find hashes like bcrypt, PBKDF2, or even older ones like MD5.
**File Integrity Checks**: If the hash is related to file integrity checks (e.g., software downloads), SHA-256 or SHA-512 is often used.
**Certificates and Signatures**: Digital certificates or signatures may use SHA-256 or SHA-1, although SHA-1 has been largely deprecated.

## Distinctive markers at specific points in the hash.
Some hash functions, particularly those used for passwords (like bcrypt, PBKDF2, and Argon2) employ _salting_ and _iterations_ to increase security. The salt is a random value added to the input to ensure identical passwords don’t produce identical hashes. Hashes with salts often have longer lengths and may include markers or delimiters in the format, like the way you might find a Bcrypt hash that starts with `$2a$10$…` where `10` is the _cost factor_, meaning it hashed and rehashed ten times.

For a hash like `$2y$12$EXRkfkdmXn2gzds2SSituJWMqp3hPFO4lH/vqFhD8aJL.lfwBby4a` from a penetration test and the $2y$ indicates algorithm is bcrypt and 12 indicates the number of iterations (also called the cost factor). You can then use a tool like John the Ripper or Hashcat with your favorite wordlists, specifying bcrypt as the algorithm.

Python's `bcrypt` module provides methods for hashing and checking passwords:

```python
>>> import bcrypt

>>> bcrypt.hashpw("PASSWD".encode('utf-8'), bcrypt.gensalt(4)).decode('utf-8')
'$2b$04$4aUdoXc5aPXQBkWGpHZiS.OhmMOMqTEUp7O9FV.RGrQRCClpHypcS'

>>> bcrypt.hashpw("PASSWD".encode('utf-8'), bcrypt.gensalt(15)).decode('utf-8')
'$2b$15$tTGjZ5RztX4neMM8y0.vu.YsuJ8/BCnEYGOG07INUZRXlZEtOOVkK'
```
