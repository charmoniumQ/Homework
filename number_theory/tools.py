from __future__ import print_function
from math import *
from itertools import *
from operator import *
from functools import reduce
from collections import Counter
from tools_extra import memoize_generator, memoize_iterator

def first(n):
    return lambda iterator: (next(iterator) for _ in range(n))

def divides(d, a):
    return a % d == 0

def mod(a, b, n):
    return divides(n, a - b)

def gcd(a1, b1, printing=True):
    a = max(abs(a1), abs(b1))
    b = min(abs(a1), abs(b1))
    q = a / b
    r = a % b
    if r == 0:
        if printing: print('gcd({a}, {b}) = {b} since {b}|{a}'.format(**locals()))
        return b
    else:
        if printing: print('gcd({a}, {b}) = gcd({b}, {r}) since {a} = {b} * {q} + {r}'.format(**locals()))
        return gcd(b, r, printing)

def coprime(a, b):
    return gcd(a, b) == 1

def division(m, n):
    q = m / n
    r = m - n*q
    assert 0 <= r < n
    return q, r

def linear_diophantine(a, b, c):
    for x in count():
        if a * x % b == c:
            break
    return x, (a*x - c) / b

@memoize_generator
def primes():
    # absolutely no optimization here
    all_primes = [2]
    i = all_primes[-1]
    yield all_primes[-1]
    while True:
        i = i + 1
        for prime in all_primes:
            if i % prime == 0:
                break
        else:
            all_primes.append(i)
            yield i

def prime_factorization(n):
    if n == 1:
        return []
    else:
        for prime in takewhile(lambda prime: prime <= n, primes()):
            if n % prime == 0:
                return [prime] + prime_factorization(n / prime)

def is_prime(n):
    return prime_factorization(n) == [n]

def is_composite(n):
    return len(prime_factorization(n)) > 1

def hilbert_set():
    h = 1
    while True:
        yield h
        h = h + 4

@memoize_generator
def hilbert_primes():
    hilbert_primes = [5]
    h = hilbert_primes[-1]
    yield h
    while True:
        h = h + 4
        for hilbert_prime in hilbert_primes:
            if h % hilbert_prime == 0:
                break
        else:
            hilbert_primes.append(h)
            yield h

def is_hilbert_prime(h):
    larger_hilbert_primes = dropwhile(lambda x: x < h, hilbert_primes())
    if next(larger_hilbert_primes) == h:
        return True
    else:
        return False

def hilbert_prime_factorization(n, printing=False):
    if n == 1:
        return [[]]
    else:
        if is_hilbert_prime(n):
            return [[n]]
        else:
            possibilities = []
            if printing: print('factors of {n} less-than-or-equal-to {0}'.format(sqrt(n), **locals()))
            for hilbert_prime in takewhile(lambda x: x <= sqrt(n), hilbert_primes()):
                if n % hilbert_prime == 0:
                    continuation = hilbert_prime_factorization(n / hilbert_prime, printing)
                    possibilities.append([hilbert_prime, continuation])
            return possibilities

def hilbert_prime_factorization(n, prefix=None):
    if prefix is None:
        prefix = []
    if is_hilbert_prime(n):
        factorizations = [sorted(prefix + [n])]
        return factorizations
    else:
        possibilities = []
        hilbert_primes_truncated = takewhile(lambda x: x <= sqrt(n), hilbert_primes())
        for hilbert_prime in hilbert_primes_truncated:
            if n % hilbert_prime == 0:
                quotient = int(n / hilbert_prime)
                factorizations = hilbert_prime_factorization(quotient, prefix + [hilbert_prime])
                for factorization in factorizations:
                    if factorization not in possibilities:
                        possibilities.append(factorization)
        return possibilities

def primorial(n):
    return reduce(mul, first(n)(primes()), 1)

def main():
    # Question: is n! + 1 prime for all n?
    # we know that there exists a prime between n and n! + 1
    # but is it n! + 1?
    for i in count(1):
        f = factorial(i) + 1
        if is_composite(f):
            prime_fac = ' * '.join(map(str, prime_factorization(f)))
            print('n! + 1 is composite:')
            print('{i}! + 1 = {f} = {prime_fac}'.format(**locals()))
            break
    print('')

    # Question: is the 1 plus the primorial of n prime for all n?
    # This is like a possible 'fix' for the negative answer of the previous question
    for i in count(1):
        p = primorial(i) + 1
        if is_composite(p):
            factorization_minus_one = ' * '.join(map(str, first(i)(primes())))
            factorization = ' * '.join(map(str, prime_factorization(p)))
            print ('nth primorial plus one is composite:')
            print('{p} = {factorization_minus_one} + 1\n{p} = {factorization}'.format(**locals()))
            break
    print('')

    # Question: what are the first ten hilbert primes?
    print('Hilbert primes:')
    print(list(first(10)(hilbert_primes())))
    print('')

    # Question: what are the five ten hilbert numbers with multiple prime factorizations
    # or equivalently: Could Harrelson have used a smaller number than 693?
    print('Numbers with multiple hilbert factorizations:')
    numbers = []
    for h in hilbert_set():
        hpf = hilbert_prime_factorization(h)
        if len(hpf) > 1:
            numbers.append(h)
            print(h, hpf)
        if len(numbers) > 10:
            break

if __name__ == '__main__':
    pass
    main()
