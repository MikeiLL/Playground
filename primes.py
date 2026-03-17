# source https://stackoverflow.com/a/19498432/2223106
"""
usage primes(50)
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
  print(ps[start], " x ", ps[end], " = ", ps[start] * ps[end])
  if ps[start] * ps[end] == goal:
    print(ps[start], " x ", ps[end], " = ", goal)
  if end == len(ps) -1:
    start += 1
    end = start
  else: end += 1
