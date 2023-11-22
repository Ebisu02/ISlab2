import random
import hashlib


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    while k > 0:
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
        k -= 1
    return True


def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p


def generate_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break

    d = modinv(e, phi)
    return ((n, e), (n, d))


def encrypt(message, public_key):
    n, e = public_key
    return pow(message, e, n)


def decrypt(ciphertext, private_key):
    n, d = private_key
    return pow(ciphertext, d, n)


def sign_file(file_path, private_key):
    with open(f'TEST_DATA/{file_path}', 'rb') as file:
        file_content = file.read()
        hash_value = int(hashlib.md5(file_content).hexdigest(), 16)

    signature = encrypt(hash_value, private_key)

    with open(f'obj/{file_path}.rsa.sig', 'wb') as signature_file:
        signature_file.write(signature.to_bytes((signature.bit_length() + 7) // 8, 'big'))


def verify_signature(file_path, public_key):
    with open(f'TEST_DATA/{file_path}', 'rb') as file:
        file_content = file.read()
        hash_value = int(hashlib.md5(file_content).hexdigest(), 16)

    with open(f'obj/{file_path}.rsa.sig', 'rb') as signature_file:
        signature = int.from_bytes(signature_file.read(), 'big')

    decrypted_signature = decrypt(signature, public_key)

    if hash_value == decrypted_signature:
        print("Подпись верна.")
    else:
        print("Подпись неверна.")



def rsa_sign():
    bits = 1024
    public_key, private_key = generate_keypair(bits)


    filename = 'input.txt'
    img = '14.png'

    with open("obj/public_key.rsa.pem", 'w') as public_key_file:
        public_key_file.write(f"{public_key[0]}\n{public_key[1]}")

    with open("obj/private_key.rsa.pem", 'w') as private_key_file:
        private_key_file.write(f"{private_key[0]}\n{private_key[1]}")

    sign_file(filename, private_key)

    pbfake = [2**1024, 2**256]

    verify_signature(filename, pbfake)
