# source https://stackoverflow.com/a/19498432/2223106
"""
usage primes(50)

RSA Encryption

# Generate the priv/pub key pair:
1. Generate two prime numbers p and q.
2. Calculate n, which is the value of p*q
3. Calculate values d and e such that:
  d * e = 1 mod (p-1)(q-1)
4. The public key consists of n and e and the private
key consists of d, p and q

# Encrypt the message
1. Convert the plaintext message into an integer, m
2. Encrypt the message to obtain the ciphertext c,
where c = m**e (mod n)

# Decrypt the message
1. Calculate the plaintext message m,
where m = c**d (mod n)
"""
def primes(n): # simple sieve of multiples
   odds = range(3, n+1, 2)
   sieve = set(sum([list(range(q*q, n+1, q+q)) for q in odds], []))
   return [2] + [p for p in odds if p not in sieve]

ps=primes(50)
start=0
end=0
goal=1079
while start <= len(ps) - 1:
  #print(ps[start], " x ", ps[end], " = ", ps[start] * ps[end])
  if ps[start] * ps[end] == goal:
    print(ps[start], " x ", ps[end], " = ", goal)
  if end == len(ps) -1:
    start += 1
    end = start
  else: end += 1
