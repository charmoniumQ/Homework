from __future__ import print_function, division
from math import *
from itertools import *
from operator import *
from functools import reduce
from tools_extra import memoize_generator, memoize_iterator

NaN = None

def sgn(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    if x < 0:
        return -1

def cmod(a, n):
    '''Returns c such that $a \equiv c \pmod{n}$ and $0 \leq c < n$
    this c is the remainder in the division algorithm
    c is also in the canonical complete residue system
    WLOG n > 0'''
    n = abs(n)
    return ((a % n) + n) % n

def first(n, iterator):
    return (next(iterator) for _ in range(n))

def divides(d, a):
    '''Returns true if $d | a$'''
    return cmod(a, d) == 0

def mod(a, b, n):
    '''Returns true if $a \equiv b \pmod{n}$'''
    return divides(n, a - b)

def gcd(a1, b1, printing=False):
    '''Returns the greatest common multiple'''
    # WLOG a > b > 0
    a = max(abs(a1), abs(b1))
    b = min(abs(a1), abs(b1))
    r = cmod(a, b)
    if r == 0:
        if printing: print('$\gcd({a}, {b}) = {b}$ since ${b}|{a}$'.format(**locals()))
        return b
    else:
        if printing: print('$\gcd({a}, {b}) = gcd({b}, {r})$ since ${a} = {b} * {q} + {r}$'.format(**locals()))
        return gcd(b, r, printing)

def lcm(a, b):
    '''Returns the least common positive multiple'''
    return abs(a * b) / gcd(a, b)

def coprime(a, b):
    '''Returns True if a and b are coprime'''
    return gcd(a, b) == 1

def division(m, n):
    '''Returns the q and r where $n = mq + r$ and $0 \leq r < n$'''
    r = cmod(m, n)
    q = (m - r) / n
    assert 0 <= r < abs(n), r
    assert q == int(q), q
    return int(q), r

@memoize_generator
def primes():
    '''Return a generator of primes'''
    yield 2
    all_primes = [2]
    i = all_primes[-1]
    while True:
        i = i + 1
        for prime in all_primes:
            if divides(prime, i):
                break
        else:
            all_primes.append(i)
            yield i

def prime_factorization(n):
    '''Returns the prime factorization of any natural n'''
    if n < 0:
        return [-1] + prime_factorization(-n)
    elif n == 1:
        return []
    elif n == 0:
        return [0]
    else:
        for prime in takewhile(lambda prime: prime <= abs(n), primes()):
            if divides(prime, n):
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
    return reduce(mul, first(n + 1, primes()), 1)

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
            if divides(hilbert_prime, h):
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
            if divides(hilbert_prime, n):
                quotient = int(n / hilbert_prime)
                factorizations = hilbert_prime_factorization(quotient, prefix + [hilbert_prime])
                possibilities = possibilities.union(factorizations)
        return possibilities

def linear_diophantine(a, b, c):
    '''Returns (x0, y0), (xi, yi) where $ax + by = c$
    when $x = x_0 + n x_$i and $y = y_0 + n y_i$'''
    g = gcd(a, b)
    if c == g:
        for x in count():
                # Loop over this with x = {0, 1, 2, 3 ...}
            if mod(a * x, g, b):
                # the above line means $a \cdot x \equiv g \pmod{b}$
                y = (g - a*x) / b
                # at this point $ax + by = g$
                # therefore return from loop
                return (x, y), (int(b / g), int(-a / g))
    elif divides(g, c):
        # solve a simplier diophantine equation first
        (u_0, v_0), (u_i, v_i) = linear_diophantine(a, b, g)
        # at this point $u_0 a + v_0 b = g$
        # multiplying both sides by $\frac{c}{g}$ gives
        # $u_0 \frac{c}{g} a + v_0 \frac{c}{g} b = g \frac{c}{g} = c$
        (x_0, y_0) = (int(u_0 * c / g), int(v_0 * c / g))
        (x_i, y_i) = (u_i, v_i)
        return(x_0, y_0), (x_i, y_i)
    else:
        raise ValueError('no solutions')

def linear_congruence(a, b, n):
    '''Returns x_0, n where $ax \equiv b \pmod{n}$ when $x \equiv x_0 \pmod{n}$'''
    # Returns x_0, n where $ax \equiv b \pmod{n}$ when $x \equiv x_0 \pmod{n}$
    # this function relies on the linear_diophantine function,
    # because why reinvent the wheel?
    (x_0, y_0), (x_i, y_i) = linear_diophantine(a, -n, b)
    return cmod(x_0, x_i), abs(x_i)

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
                if printing: print('\\\\ \(x\) satisfies \({a} x \equiv {b} \pmod {{{n}}}\) and all previous equations when \(x = {x0} + j \cdot {xi}\) \\\\'.format(**locals()))
                break
        else:
            raise ValueError('no solutions')
    if printing: print('\(x = \{\)' + ''.join(map(lambda xn: '\({xn}\), '.format(**locals()), list(map(lambda j: x0 + j * xi, xrange(0, 3 * j + 3))))) + '\(\dots\}\) \\\\')
    return x0, xi

def mod_exp(a1, r, n, printing=True):
    '''Returns the k in $a^r \equiv k \pmod{n}$ where $0 \leq k < r$ using algorithm 3.6'''
    # WLOG a < n
    if printing: print(r'$ {a1}^{{{r}}} \equiv '.format(**locals()), end='')
    a = cmod(a1, n) # reduce a if possible
    a2 = cmod(a * a, n)
    if not a1 == a:
        if printing: print(r'{a}^{{{r}}} \equiv ', end='')
    r2 = int(floor(r / 2))
    if r == 1:
        # Base case
        if printing: print(r'{a} \pmod {{{n}}} $ \\'.format(**locals()))
        return a
    if divides(2, r):
        # $(a^2)^{r/2}$
        if printing: print(r'({a}^2)^{{{r}/2}} \equiv {a2}^{{{r2}}} \pmod{{{n}}} $ \\'.format(**locals()))
        k = mod_exp(a2, r2, n, printing)
        k = cmod(k, n)
        return k
    else:
        # $(a^2)^{(r-1)/2} \cdot a$
        if printing: print(r'({a}^2)^{{({r}-1)/2}} \cdot {a} \equiv {a2}^{{{r2}}} \cdot {a} \pmod{{{n}}} $ \\'.format(**locals()))
        k = mod_exp(a2, r2, n, printing)
        ka = cmod(k * a, n)
        if printing: print(r'$ {k} \cdot {a} \equiv {ka} \pmod {{{n}}} $ \\'.format(**locals()))
        return ka

def order(a, n):
    '''Calculate k where $a^k \equiv 1 \pmod n$'''
    if gcd(a, n) != 1:
        return None
    for k in count(1): # count up from one
        # if $a^k \pmod n \equiv 1$
        if mod_exp(a, k, n, printing=False) == 1:
            # $k = ord_n(a)$
            return k

def main():
    # Question: is n! + 1 prime for all n?
    # we know that there exists a prime between n and n! + 1
    # but is it n! + 1?
    for i in count(1):
        f = factorial(i) + 1
        if is_composite(f):
            prime_fac = ' * '.join(map(str, prime_factorization(f)))
            print('$n! + 1$ is composite:')
            print('{i}! + 1 = {f} = {prime_fac}'.format(**locals()))
            break
    print('')

    # Question: is the 1 plus the primorial of n prime for all n?
    # This is like a possible 'fix' for the negative answer of the previous question
    for i in count(1):
        p = primorial(i) + 1
        if is_composite(p):
            factorization_minus_one = ' * '.join(map(str, first(i, primes())))
            factorization = ' * '.join(map(str, prime_factorization(p)))
            print ('nth primorial plus one is composite:')
            print('{p} = {factorization_minus_one} + 1\n{p} = {factorization}'.format(**locals()))
            break
    print('')

    # Question: what are the first ten hilbert primes?
    print('Hilbert primes:')
    print(list(first(10, hilbert_primes())))
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

    # Task: 3.4 to 3.6
    print('Modular exponentiation')
    print(r'\begin{tabular}[t]{l}')
    mod_exp(9, 453, 12, True)
    print(r'\end{tabular}', end='\n\n')
    print(r'\begin{tabular}[t]{l}')
    mod_exp(17, 48, 39, True)
    print(r'\end{tabular}', end='\n\n')
    print(r'\begin{tabular}[t]{l}')
    mod_exp(5, 24, 39, True)
    print(r'\end{tabular}')

    # Task: write a program that solves linear diophantine equations
    # this makes the exercises much easier
    print('Linear diophantine solutions:')
    a, b, c = 7, 8, 100
    (x0, y0), (xi, yi) = linear_diophantine(a, b, c)
    x1, y1 = x0 + xi, y0 + yi
    print('${a} \cdot {x0} + {b} \cdot {y0} = {c}$'.format(**locals()))
    print(a*x0 + b*y0 == c)
    print('${a} \cdot {x1} + {b} \cdot {y1} = {c}$'.format(**locals()))
    print(a*x1 + b*y1 == c)
    print('')

    print('Systems of linear congruence solutions:')
    linear_congruence_system([(1, 3, 17), (1, 10, 16), (1, 0, 15)], True)
    print('')
    linear_congruence_system([(1, 1, 2), (1, 2, 3), (1, 3, 4), (1, 4, 5), (1, 5, 6), (1, 0, 7)], True)
    # I am not going to test this. I know it works.
    # (famous last words)
    print('')

    print('Fermat\'s little theorem examples')
    for p in first(10, primes()):
        print(r'\(\pmod {{{p}}}\)'.format(**locals()))
        print('')
        print(r'\begin{tabular}[t]{l}')
        for a in range(0, p):
            # $ 0 \leq a < p$
            e = p - 1
            c = mod_exp(a, e, p, False)
            print(r'${a}^{{{e}}} \equiv {c} \pmod {{{p}}}$ \\'.format(**locals()))
        print(r'\end{tabular}')
        print('')

    print('')

if __name__ == '__main__':
    pass
    main()
