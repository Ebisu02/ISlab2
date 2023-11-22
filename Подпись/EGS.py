import hashlib
import math
import random
from sympy import mod_inverse

from Шифр.lab2 import generate_prime, is_prime


# Функция для вычисления хэша файла
def calculate_hash(file_path):
    hash_object = hashlib.sha256()
    with open(file_path, "rb") as file:
        # Чтение файла блоками для оптимизации
        for chunk in iter(lambda: file.read(4096), b""):
            hash_object.update(chunk)
    return int(hash_object.hexdigest(), 16)


# Функция для генерации случайных чисел k и поиска обратного по модулю
def generate_k(P):
    k = random.randint(2, P - 2)
    while not (1 < k < P - 1) or math.gcd(k, P - 1) != 1:
        k = random.randint(2, P - 2)
    return k


# Функция для генерации подписи
def generate_signature(file_path, P, g, x):
    h = calculate_hash(file_path)
    k = generate_k(P)

    r = pow(g, k, P)
    u = (h - x * r) % (P - 1)
    s = (mod_inverse(k, P - 1) * u) % (P - 1)

    return r, s


# Функция для проверки подписи
def verify_signature(file_path, signature, P, g, y):
    r, s = signature
    h = calculate_hash(file_path)

    left_side = (pow(y, r, P) * pow(r, s, P)) % P
    right_side = pow(g, h, P)

    return left_side == right_side


def generate_params_eg(bits):
    p = generate_prime(bits)
    while not is_prime((p - 1) / 2):
        p = generate_prime(bits)
    g = 2
    while pow(g, (int)((p - 1) / 2), p) == 1:
        g += 1
    return p, g


def el_gamal_sign():
    # Задаем параметры P, g, x, которые должны быть известны Алисе и тем, кто будет проверять подпись
    p, g = generate_params_eg(32)

    # Секретный ключ
    x = random.randint(1, p - 1)

    # Вычисляем открытый ключ y
    y = pow(g, x, p)

    # Пример использования для подписи файла
    file_to_sign = "TEST_DATA/input.txt"
    signature = generate_signature(file_to_sign, p, g, x)

    with open(file_to_sign, 'a') as f:
        f.write('abc')

    # Сохраняем подпись в отдельном файле
    with open("obj/signature_eg.txt", "w") as signature_file:
        signature_file.write(f"{signature[0]}\n{signature[1]}")

    # Пример использования для проверки подписи
    is_valid = verify_signature(file_to_sign, signature, p, g, y)

    if is_valid:
        print("Подпись верна.")
    else:
        print("Подпись недействительна.")
