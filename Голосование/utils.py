import random
import math


def is_prime(p: int, trials: int = 20) -> bool:
    if p == 2 or p == 3:
        return True

    if p < 2 or not (p & 1):
        return False

    for _ in range(trials):
        a = random.randint(2, p - 1)
        if exp_mod(a, (p - 1), p) != 1 or math.gcd(p, a) > 1:
            return False
    return True


def get_prime(left: int, right: int) -> int:
    while True:
        p = random.randint(left, right)
        if is_prime(p):
            return p


def get_mut_prime(p):
    while True:
        if math.gcd(p, b := random.randrange(2, p)) == 1:
            return b


def exp_mod(a: int, x: int, p: int) -> int:
    if p == 0:
        raise ValueError("Mod cannot be equals 0")
    if x < 0:
        raise ValueError("X cannot be < 0")
    result = 1
    a = a % p
    if a == 0:
        return 0
    while x > 0:
        if x & 1 == 1:
            result = (result * a) % p
        a = (a ** 2) % p
        x >>= 1
    return result


def gen_evklid(a: int, b: int) -> list[int, int, int]:

    if a <= 0 or b <= 0:
        raise ValueError("Number should be natural")
    if a > b:
        a, b = b, a
    u = [a, 1, 0]
    v = [b, 0, 1]
    while v[0] != 0:
        q = u[0] // v[0]
        t = [u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2]]
        u, v = v, t
    return u


def inverse(n, p):
    gcd, inv, _ = gen_evklid(n, p)
    assert gcd == 1
    if inv < 0 :
        inv += p
    return inv
