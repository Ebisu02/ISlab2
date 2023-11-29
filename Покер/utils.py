def egcd(a, b):
    while b != 0:
        res = a % b
        a = b
        b = res
    return a


def gen_evklid_u(a, b):
    if b > a:
        a, b = b, a
    u = [a, 1, 0]
    v = [b, 0, 1]
    while int(v[0]) != 0:
        q = int(u[0]) // int(v[0])
        t = [u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2]]
        u = v
        v = t
    return u
