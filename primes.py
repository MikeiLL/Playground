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

# Example

n = 1079
e = 43
c = 996 894 379 631 894 82 379 852 631 677 677 194 893


# Steps
d*e = 1 mod (p-1)(q-1)
d*43 = 1 mod (83-1)(13-1)
d=1/43 mod 984
  >>> pow(43, -1, 984)
  595

  ### More side notes
  From Wikipedia, the free encyclopedia
  In mathematics, particularly in the area of arithmetic, a
  modular multiplicative inverse of an integer a is an
  integer x such that the product ax is congruent to 1
  with respect to the modulus m.[1] In the standard
  notation of modular arithmetic this congruence is written as

    ax ≡ 1 (mod m)

  which is the shorthand way of writing the statement that m divides
  (evenly) the quantity ax − 1, or, put another way, the remainder
  after dividing ax by the integer m is 1. If a does have an
  inverse modulo m, then there is an infinite number of solutions
  of this congruence, which form a congruence class with respect
  to this modulus.

    https://en.wikipedia.org/wiki/Modular_multiplicative_inverse

  # Iterative python code to find it.
  """
def imod(a,n):
  i=1
  while True:
    c = n * i + 1
    if(c % a ==0):
      c = c/a
      break
    i = i+1

  return c
"""

d=595
  Rosuav notes:
  595 * 43 = 1 (mod 984)
  divmod(595 * 43, 984) ==> 26 remainder 1
  d * 43 = 1
  # these two are the same thing:
    d = 1 / 43
    d = 43**-1
"""
def primes(n): # simple sieve of multiples
   odds = range(3, n+1, 2)
   sieve = set(sum([list(range(q*q, n+1, q+q)) for q in odds], []))
   return [2] + [p for p in odds if p not in sieve]

ps=primes(50)
n = 1079
e = 43
c = [996, 894, 379, 631, 894, 82, 379, 852, 631, 677, 677, 194, 893]
p=False
q=False
d=False
start=0
end=0
goal=n
while start <= len(ps) - 1:
  #print(ps[start], " x ", ps[end], " = ", ps[start] * ps[end])
  if ps[start] * ps[end] == goal:
    print(ps[start], " x ", ps[end], " = ", goal)
    p = ps[start]
    q = ps[end]
    break
  if end == len(ps) -1:
    start += 1
    end = start
  else: end += 1

d = pow(e, -1, (p-1) * (q-1))
print(f'd is {d} ( the multiplicative inverse of {p-1} times {q-1} )')
