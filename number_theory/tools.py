def divides(d, a):
    return a % d == 0

def mod(a, b, n):
    return divides(n, a - b)

def gcd(a, b):
	if a == 0:
		return b
        else:
		return gcd(b % a, a)

def coprime(a, b):
    return gcd(a, b) == 1
