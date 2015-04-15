from __future__ import print_function
from math import *
from itertools import *
from operator import *
from functools import reduce
from collections import Counter
from tools_extra import memoize_generator, memoize_iterator

NaN = None

def first(n):
    return lambda iterator: (next(iterator) for _ in range(n))

def divides(d, a):
    '''Returns true if d | a'''
    return a % d == 0

def mod(a, b, n):
    '''Returns true if a = b mod n'''
    return divides(n, a - b)

def gcd(a1, b1, printing=False):
    '''Returns the greatest common multiple'''
    # WLOG a > b > 0
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

def lcm(a, b):
    '''Returns the least common positive multiple'''
    return abs(a * b) / gcd(a, b)

def coprime(a, b):
    '''Returns if a and b are coprime'''
    return gcd(a, b) == 1

def division(m, n):
    '''Returns the q and r from the dividion algorithm for'''
    q = m / n
    r = m - n*q
    #assert 0 <= r < n
    return q, r

def cmod(a, n):
    '''Returns a = c mod n where 0 <= c < n'''
    return division(a, n)[1]

@memoize_generator
def primes():
    '''Return a generator of primes'''
    yield 2
    all_primes = [2]
    i = all_primes[-1]
    while True:
        i = i + 1
        for prime in all_primes:
            if i % prime == 0:
                break
        else:
            all_primes.append(i)
            yield i

def prime_factorization(n):
    '''Returns the prime factorization of any integer n'''
    # for natural numbers
    if n < 0:
        return [-1] + prime_factorization(-n)
    if n == 1:
        return []
    else:
        for prime in takewhile(lambda prime: prime <= abs(n), primes()):
            if n % prime == 0:
                return [prime] + prime_factorization(n / prime)
            
def is_prime(n):
    '''Returns true if n is prime for any natural n'''
    larger_primes = dropwhile(lambda x: x < n, primes())
    if next(larger_primes) == n:
        return True
    else:
        return False

def is_composite(n):
    '''Returns true if n is composite for any natural n'''
    return n != 1 and not is_prime(n)

def primorial(n):
    return reduce(mul, first(n + 1)(primes()), 1)

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

def hilbert_prime_factorization(n, prefix=None):
    '''Returns a set tuples, where each tuple is a possible hilbert factorizations for any natural number n'''
    if prefix is None:
        prefix = []
    if is_hilbert_prime(n):
        factorization = [tuple(sorted(prefix + [n])), ]
        return factorization
    else:
        possibilities = set()
        hilbert_primes_truncated = takewhile(lambda x: x <= sqrt(n), hilbert_primes())
        for hilbert_prime in hilbert_primes_truncated:
            if n % hilbert_prime == 0:
                quotient = int(n / hilbert_prime)
                factorizations = hilbert_prime_factorization(quotient, prefix + [hilbert_prime])
                possibilities = possibilities.union(factorizations)
        return possibilities

def linear_diophantine(a, b, c):
    '''Return (x0, y0), (xi, yi) where (x0 + n * xi) * a + (y0 + n * yi) * b = c for integer n'''
    g = gcd(a, b)
    if not divides(g, c):
        return None
    for x in count():
        if a * x % b == g:
            break
    y = (g - a*x) / b
    return (x * c / g, y * c / g), (b / g, -a / g)

def linear_congruence(a, b, n):
    '''Return x0, xi where a * (x0 + n * xi) = b mod n for integer n'''
    # ax = b mod n
    # b = ax mod n
    # n|(b - ax)
    # yn = b - ax
    # ax + yn = b
    (x0, y0), (xi, yi) = linear_diophantine(a, n, b)
    return x0, xi

def linear_congruence_system(eqns, printing=False):
    # if x = x0 + j * xi, then x = all whole numbers
    # therefore start with x0 = 0, xi = 1
    x0, xi = 0, 1
    for a, b, n in eqns:
        for j in count():
            if mod(a * (x0 + j*xi), b, n):
                if printing: print('\(x = \{\)' + ''.join(map(lambda xn: '\({xn}\), '.format(**locals()), list(map(lambda j: x0 + j * xi, xrange(0, 3 * j + 3))))) + '\(, \dots\}\) \\\\')
                x0 = x0 + j * xi
                xi = lcm(xi, n)
                if printing: print('\\\\ \(x\) satisfies \({a} x \equiv {b} \pmod {{{n}}}\) and all previous equations'.format(**locals()))
                if printing: print('when \(x = {x0} + j \cdot {xi}\) \\\\'.format(**locals()))
                break
        else:
            print('death')
    return x0, xi

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
    print('')

    # Task: write a program that solves linear diophantine equations
    # this makes the exercises much easier
    print('Linear diophantine solutions:')
    a, b, c = 7, 8, 100
    (x0, y0), (xi, yi) = linear_diophantine(a, b, c)
    x1, y1 = x0 + xi, y0 + yi
    print('{a}*{x0} + {b}*{y0} = {c}'.format(**locals()))
    print(a*x0 + b*y0 == c)
    print('{a}*{x1} + {b}*{y1} = {c}'.format(**locals()))
    print(a*x1 + b*y1 == c)
    print('')

    print('Systems of linear congruence solutions:')
    linear_congruence_system([(1, 3, 17), (1, 10, 16), (1, 0, 15)], True)
    print('')
    linear_congruence_system([(1, 1, 2), (1, 2, 3), (1, 3, 4), (1, 4, 5), (1, 5, 6)], True)
    # I am not going to test this. I know it works.
    # (famous last words)
    print('')

if __name__ == '__main__':
    pass
    main()
