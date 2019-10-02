import requests
import os
from Crypto.Util.number import *
import threading


"""
Original code:
https://github.com/perfectblue/ctf-writeups/blob/master/csaw-ctf-2019-quals/timelie-150/solve.py

This framework can be used to crack a Shamir Sharing scheme
If the key is split into multiple parts, it is probably a Shamir Scheme

Given S = key, S is divided into n pieces Sn
Knowing k pieces allows the reconstruction of S.
This is based on the idea that  2 points are needed for a line, 3 for parab, etc
For any curve, you need k-1 points to define the curve where k = order

Curve is constructed with f(x) = a_0 + a_1x + ... + a_(k-1)x^(k-1)
k is the number of parts you would need to reconstruct the curve
a_0 = Secret = S
Take integers i such that i is an integer and f(i) = integer, these are the pieces
Coefficients are found for the curve using interpolation.
"""

"""
USAGE:
Write something to gather shares.  Send array of shares to recover_secret()
"""

def _eval_at(poly, x, prime):
    '''evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    '''
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum

def _extended_gcd(a, b):
    '''
    division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    '''
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a%b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y

def _divmod(num, den, p):
    '''compute num / den modulo prime p
    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    '''
    inv, _ = _extended_gcd(den, p)
    return num * inv

def _lagrange_interpolate(x, x_s, y_s, p):
    '''
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order
    '''
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"
    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p

def recover_secret(shares, prime):
    '''
    Recover the secret from share points
    (x,y points on the polynomial)
    '''
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)


#Input prime used for shamir scheme
P = 101109149181191199401409419449461491499601619641661691809811881911

#Input shares as a array of tuples
shares = [(1, 1494), (2, 1942), (3,2578)]

#Get secret
print(recover_secret(shares, P))

print("DONE")
