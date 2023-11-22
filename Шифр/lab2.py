import math
import random

TEST = 12345
TO_FILE = -12345
IMG = 0


# Генерация случайного большого простого числа
def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num


# Проверка числа на простоту
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


# Расширенный алгоритм Евклида для нахождения модульного обратного
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)


# Генерация открытых и секретных ключей для отправителя и получателя
def generate_keys_sh(p):
    while True:
        C = random.randint(1, p - 1)
        gcd, D, _ = extended_gcd(C, p - 1)
        if gcd == 1:
            return C, D % (p - 1)


# Шифрование сообщения
def encrypt_sh(message, C, p):
    x1 = []
    for byte in message:
        # byte^C mod p
        x1.append(pow(byte, C, p))
    return x1


# Расшифрование сообщения
def decrypt_sh(x1, D_B, p):
    x2 = []
    for byte in x1:
        x2.append(pow(byte, D_B, p))
    return x2


def generate_params_eg():
    p = generate_prime(32)
    while not is_prime((p - 1) / 2):
        p = generate_prime(32)
    g = 2
    while pow(g, (int)((p - 1) / 2), p) == 1:
        g += 1
    return p, g


def generate_keys_eg(p, g):
    x = random.randint(2, p - 2)  # private - decrypt
    y = pow(g, x, p)  # public - encrypt
    return x, y


def encrypt_eg(p, g, y, msg):
    k = random.randint(2, p - 2)  # session key
    a = pow(g, k, p)
    b = []
    for byte in msg:
        b.append((pow(y, k, p) * byte) % p)
    return a, b


def decrypt_eg(p, x, a, b):
    m = []
    for byte in b:
        m.append((byte * pow(a, p - 1 - x, p)) % p)
    return m


def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def generate_keys_rsa(bits=16):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while not is_prime(q) and q >= p:
        q = generate_prime(bits)
    nb = p * q
    phi = (p - 1) * (q - 1)
    db = random.randrange(2, phi)
    while math.gcd(db, phi) != 1:
        db = random.randrange(2, phi)
    cb = mod_inverse(db, phi)
    return db, cb, nb


def encrypt_rsa(msg, keys_b, keys_a, state=TO_FILE):
    if state == TO_FILE:
        db, cb, nb = keys_b
        da, ca, na = keys_a
        msg_to_encode = [ord(c) for c in msg]
        encrypted_msg = [pow(char, cb, nb) for char in msg_to_encode]
        encrypted_msg = [pow(char, da, na) for char in encrypted_msg]
        return encrypted_msg
    elif state == IMG:
        db, cb, nb = keys_b
        da, ca, na = keys_a
        msg_to_encode = [int(b) for b in msg]
        encrypted_msg = [pow(char, cb, nb) for char in msg_to_encode]
        # encrypted_msg = [pow(char, da, na) for char in encrypted_msg]
        return encrypted_msg
    return None


def decrypt_rsa(enc_msg, keys_a, keys_b, state=TO_FILE):
    if state == TO_FILE:
        db, cb, nb = keys_b
        da, ca, na = keys_a
        decrypted_msg = [pow(char, ca, na) for char in enc_msg]
        decrypted_ms = [(pow(char, db, nb)) for char in decrypted_msg]
        msg = ""
        for c in decrypted_ms:
            msg += chr(c)
        return msg
    elif state == IMG:
        db, cb, nb = keys_b
        da, ca, na = keys_a
        # decrypted_msg = [pow(char, ca, na) for char in enc_msg]
        decrypted_msg = [chr(pow(char, db, nb)) for char in enc_msg]
        return decrypted_msg
    return None


def generate_keys_vernam(msg_len):
    return [random.randint(0, 255) for _ in range(msg_len)]


def encrypt_vn(msg, key):
    enc_msg = []
    for i in range(len(msg)):
        enc_msg.append(msg[i] ^ key[i])  # xor
    return enc_msg


def decrypt_vn(enc_msg, key):
    decr_msg = []
    for i in range(len(enc_msg)):
        decr_msg.append(enc_msg[i] ^ key[i])
    return decr_msg


def rsa_test(message, state):
    if state == TEST:
        print(">>>>>>>>>> Шифр RSA <<<<<<<<<<")
        keys_b = generate_keys_rsa(bits=32)
        keys_a = generate_keys_rsa(bits=32)
        print("Original Message:", message)
        encrypted_message = encrypt_rsa(message, keys_b, keys_a)
        print("Encrypted Message:", encrypted_message)
        decrypted_message = decrypt_rsa(encrypted_message, keys_a, keys_b)
        print("Decrypted Message:", decrypted_message)
    elif state == TO_FILE:
        keys_b = generate_keys_rsa(bits=16)
        keys_a = generate_keys_rsa(bits=16)
        encrypted_message = encrypt_rsa(message, keys_b, keys_a)
        decrypted_message = decrypt_rsa(encrypted_message, keys_a, keys_b)
        with open("Шифр/encrypted_msg_rsa.txt", "w", encoding="utf-8") as efile:
            for byte in encrypted_message:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_msg_rsa.txt", "w", encoding="utf-8") as defile:
            defile.write(decrypted_message)
    elif state == IMG:
        keys_b = generate_keys_rsa(bits=16)
        keys_a = generate_keys_rsa(bits=16)
        encrypted_message = encrypt_rsa(message, keys_b, keys_a, state=IMG)
        decrypted_message = decrypt_rsa(encrypted_message, keys_a, keys_b, state=IMG)
        with open("Шифр/encrypted_img_rsa.txt", "w", encoding="utf-8") as efile:
            for byte in encrypted_message:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_img_rsa.png", "wb") as defile:
            for byte in decrypted_message:
                defile.write(ord(byte).to_bytes(1, byteorder="big"))


def vernam_test(msg, state):
    if state == TEST:
        print(">>>>>>>>>> Шифр Вернама <<<<<<<<<<")
        print("Original Message:", msg)
        msg_bytes = [ord(char) for char in msg]
        key = generate_keys_vernam(len(msg_bytes))
        encrypted_msg = encrypt_vn(msg_bytes, key)
        decrypted_msg = decrypt_vn(encrypted_msg, key)
        print("Зашифрованное сообщение:", encrypted_msg)
        print("Расшифрованное сообщение:", ''.join(chr(byte) for byte in decrypted_msg))
    elif state == TO_FILE:
        msg_bytes = [ord(char) for char in msg]
        key = generate_keys_vernam(len(msg_bytes))
        encrypted_msg = encrypt_vn(msg_bytes, key)
        decrypted_msg_bytes = decrypt_vn(encrypted_msg, key)
        decrypted_msg = ''.join(chr(byte) for byte in decrypted_msg_bytes)
        with open("Шифр/encrypted_msg_vn.txt", "w", encoding="utf-8") as efile:
            for byte in encrypted_msg:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_msg_vn.txt", "w", encoding="utf-8") as defile:
            defile.write(decrypted_msg)
    elif state == IMG:
        msg_bytes = [ord(chr(byte)) for byte in msg]
        key = generate_keys_vernam(len(msg_bytes))
        encrypted_msg = encrypt_vn(msg_bytes, key)
        decrypted_msg_bytes = decrypt_vn(encrypted_msg, key)
        with open("Шифр/encrypted_img_vn.txt", "w", encoding="utf-8") as efile:
            for byte in encrypted_msg:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_img_vn.png", "wb") as defile:
            for byte in decrypted_msg_bytes:
                defile.write(byte.to_bytes(1, byteorder="big"))


def shamir_test(message, state):
    if state == TEST:
        print(">>>>>>>>>> Шифр Шамира <<<<<<<<<<")
        # Генерация большого случайного простого числа
        p = generate_prime(16)  # Выберите более большое значение для более надежной защиты
        # Генерация ключей для отправителя и получателя // c - public, d - private //
        C_A, D_A = generate_keys_sh(p)
        C_B, D_B = generate_keys_sh(p)
        # Сообщение для шифрования
        message_bytes = [ord(char) for char in message]
        print("Исходное сообщение:", message)
        # Шифрование сообщения
        encrypted_message = encrypt_sh(message_bytes, C_A, p)
        encrypted_message = encrypt_sh(encrypted_message, C_B, p)
        encrypted_message = encrypt_sh(encrypted_message, D_A, p)
        decrypted_message_bytes = decrypt_sh(encrypted_message, D_B, p)
        decrypted_message = ''.join(chr(byte) for byte in decrypted_message_bytes)
        print("Зашифрованное сообщение:", encrypted_message)
        # Расшифрование сообщения для абонента B (Боба)
        print("Расшифрованное сообщение:", decrypted_message)
    elif state == TO_FILE:
        p = generate_prime(16)
        C_A, D_A = generate_keys_sh(p)
        C_B, D_B = generate_keys_sh(p)
        message_bytes = [ord(char) for char in message]
        encrypted_message = encrypt_sh(message_bytes, C_A, p)
        encrypted_message = encrypt_sh(encrypted_message, C_B, p)
        encrypted_message = encrypt_sh(encrypted_message, D_A, p)
        decrypted_message_bytes = decrypt_sh(encrypted_message, D_B, p)
        decrypted_message = ''.join(chr(byte) for byte in decrypted_message_bytes)
        with open("Шифр/encrypted_msg_sh.txt", "w", encoding="utf-8") as efile:
            for byte in encrypted_message:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_msg_sh.txt", "w", encoding="utf-8") as defile:
            defile.write(decrypted_message)
    elif state == IMG:
        p = generate_prime(16)
        C_A, D_A = generate_keys_sh(p)
        C_B, D_B = generate_keys_sh(p)
        msg_bytes = [ord(chr(byte)) for byte in message]
        encrypted_message = encrypt_sh(msg_bytes, C_A, p)
        encrypted_message = encrypt_sh(encrypted_message, C_B, p)
        encrypted_message = encrypt_sh(encrypted_message, D_A, p)
        decrypted_message_bytes = decrypt_sh(encrypted_message, D_B, p)
        with open("Шифр/encrypted_img_sh.txt", "w", encoding="utf-8") as efile:
            for byte in encrypted_message:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_img_sh.png", "wb") as defile:
            for byte in decrypted_message_bytes:
                defile.write(byte.to_bytes(1, byteorder="big"))


def el_gamal_test(message, state):
    if state == TEST:
        print(">>>>>>>>>> Шифр Эль-Гамаля <<<<<<<<<<")
        p, g = generate_params_eg()
        x, y = generate_keys_eg(p, g)
        msg_bytes = [ord(char) for char in message]
        print("Исходное сообщение:", message)
        a, b = encrypt_eg(p, g, y, msg_bytes)
        print("Зашифрованные значения (a, b):", a, b)
        decrypted_msg = decrypt_eg(p, x, a, b)
        print("Расшифрованное значение:", ''.join(chr(byte) for byte in decrypted_msg))
    elif state == TO_FILE:
        p, g = generate_params_eg()
        x, y = generate_keys_eg(p, g)
        msg_bytes = [ord(char) for char in message]
        a, b = encrypt_eg(p, g, y, msg_bytes)
        decrypted_msg_bytes = decrypt_eg(p, x, a, b)
        decrypted_msg = ''.join(chr(byte) for byte in decrypted_msg_bytes)
        # first symbol in file - a, other - b
        with open("Шифр/encrypted_msg_eg.txt", "w", encoding="utf-8") as efile:
            efile.write(f'{a} ')
            for byte in b:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_msg_eg.txt", "w", encoding="utf-8") as defile:
            defile.write(decrypted_msg)
    elif state == IMG:
        p, g = generate_params_eg()
        x, y = generate_keys_eg(p, g)
        msg_bytes = [ord(chr(byte)) for byte in message]
        a, b = encrypt_eg(p, g, y, msg_bytes)
        decrypted_msg_bytes = decrypt_eg(p, x, a, b)
        with open("Шифр/encrypted_img_eg.txt", "w", encoding="utf-8") as efile:
            efile.write(f'{a} ')
            for byte in b:
                efile.write(f'{str(byte)} ')
        with open("Шифр/decrypted_img_eg.png", "wb") as defile:
            for byt in decrypted_msg_bytes:
                defile.write(byt.to_bytes(1, byteorder="big"))


def lab2():
    # shamir_test("Hello!", state=TEST)
    # el_gamal_test("Hello!", state=TEST)
    # rsa_test("Hello!", state=TEST)
    with open("Шифр/input.txt", "r", encoding="utf-8") as input_file:
        strrr = input_file.read()
        # shamir_test(message=strrr, state=TO_FILE)
        # el_gamal_test(message=strrr, state=TO_FILE)
        # rsa_test(message=strrr, state=TO_FILE)
        # vernam_test(msg=strrr, state=TO_FILE)
    with open("Шифр/test.png", "rb") as img:
        bin_data = img.read()
        # el_gamal_test(bin_data, IMG)
        # shamir_test(bin_data, IMG)
        # vernam_test(bin_data, IMG)
        rsa_test(bin_data, IMG)

