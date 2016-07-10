# these is a funciton from the standard library
# count() -> {0, 1, 2, 3, ...}
from itertools import count
# floor(1.2) -> 1
from math import floor

def cmod(a, n):
    # Returns c such that $a \equiv c \pmod{n}$ and $0 \leq c < n$ (WLOG $n > 0$)
    # this c is the remainder in the division algorithm
    # and c is in the canonical complete residue system
    n = abs(n)
    if a > 0:
        while a >= n:
            a = a - n
        return a
    else:
        while a < 0:
            a = a + n
        return a

def division(m, n):
    # Returns the q and r where $n = mq + r$ and $0 \leq r < n$
    r = cmod(m, n)
    q = (m - r) / n
    assert 0 <= r < abs(n), r
    assert q == int(q), q
    return int(q), r

def divides(d, a):
    # Returns true if $d | a$
    # (equivalent to if the remainder upon division is zero, return true)
    return cmod(a, d) == 0

def mod(a, b, n):
    # Returns true if $a \equiv b \pmod{n}$
    # (equivalent to $n | (b - a)$)
    return divides(n, b - a)

def gcd(a1, b1):
    # Returns the greatest common multiple
    # WLOG a > b > 0
    a = max(abs(a1), abs(b1))
    b = min(abs(a1), abs(b1))
    r = cmod(a, b)
    if r == 0:
        return b
    else:
        return gcd(b, r)

def linear_diophantine(a, b, c):
    # Returns (x0, y0), (xi, yi) where $ax + by = c$
    # when $x = x_0 + n x_i$ and $y = y_0 + n y_i$
    g = gcd(a, b)
    if c == g:
        for x in count():
            # Loop over this with x = {0, 1, 2, 3 ...}
            print x
            if mod(a * x, g, b):
                # execute this block if  $a \cdot x \equiv g \pmod{b}$
                y = (g - a*x) / b
                # at this point $ax + by = g$
                # therefore return from loop
                return (x, y), (b / g, -a / g)
    else:
        # solve a simpler diophantine equation first
        (u_0, v_0), (u_i, v_i) = linear_diophantine(a, b, g)
        # at this point $u_0 a + v_0 b = g$
        # multiplying both sides by $\frac{c}{g}$ gives
        # $u_0 \frac{c}{g} a + v_0 \frac{c}{g} b = g \frac{c}{g} = c$
        (x_0, y_0) = (u_0 * c / g, v_0 * c / g)
        (x_i, y_i) = (u_i, v_i)
        return(x_0, y_0), (x_i, y_i)

def linear_congruence(a, b, n):
    # Returns x_0, n where $ax \equiv b \pmod{n}$ when $x \equiv x_0 \pmod{n}$
    # this function relies on the linear_diophantine function,
    # because why reinvent the wheel?
    (x_0, y_0), (x_i, y_i) = linear_diophantine(a, -n, b)
    return x_0, x_i

def mod_exp(a1, r, n):
    # Returns the k in $a^r \equiv k \pmod{n}$ where $0 \leq k < r$
    # This algorithm is found in 3.6
    # WLOG a < n
    a = cmod(a1, n) # reduce a mod n if possible
    a_squared = cmod(a * a, n)
    r_halved, remainder = division(r, 2)
    if r == 1:
        # Base case
        return a
    if divides(2, r):
        # $(a^2)^{r/2}$
        k = mod_exp(a_squared, r_halved, n)
        k = cmod(k, n) # reduce k mod n
        return k
    else:
        # $(a^2)^{(r-1)/2} \cdot a$
        k = mod_exp(a_squared, r_halved, n)
        ka = cmod(k * a, n)
        return ka
