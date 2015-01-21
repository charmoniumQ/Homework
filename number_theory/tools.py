def divides(d, a):
    return a % d == 0

def mod(a, b, n):
    return divides(n, a - b)

def gcd(a1, b1):
    a = max(abs(a1), abs(b1))
    b = min(abs(a1), abs(b1))
    print a
    if b == 0:
        return a
    elif b == 1:
        return 1
    else:
        return gcd(a % b, b)

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
        

