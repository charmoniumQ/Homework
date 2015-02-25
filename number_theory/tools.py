def divides(d, a):
    return a % d == 0

def mod(a, b, n):
    return divides(n, a - b)

def gcd(a1, b1, printing=True):
    a = max(abs(a1), abs(b1))
    b = min(abs(a1), abs(b1))
    q = a / b
    r = a % b
    if printing: print '{a} = {b} * {q} + {r}'.format(**locals())
    if r == 0:
        if printing: print 'gcd({a}, {b}) = {b} since {b}|{a}'.format(**locals())
        return b
    else:
        if printing: print 'gcd({a}, {b}) = gcd({b}, {r})'.format(**locals())
        return gcd(b, r, printing)

def coprime(a, b):
    return gcd(a, b) == 1

def division(m, n):
    q = m / n
    r = m - n*q
    assert 0 <= r < n
    return q, r

def linear_diophantine(a, b, c):
    j = 0
    x = 0
    while j % b != c:
        j += a
        x += 1
    y = a * x / b
    #print j, x, y, a * x, b * y
    return a, b
        
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for x in range(3, int(n**.5 + 1), 2):
        if n % x == 0:
            return False
    return True
