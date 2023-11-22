import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


def sign_file(private_key, file_path):
    # Чтение файла
    with open(file_path, 'rb') as f:
        data = f.read()

    # Вычисление хэша
    hasher = hashes.Hash(hashes.SHA256(), default_backend())
    hasher.update(data)
    digest = hasher.finalize()

    # Подпись хэша
    signature = private_key.sign(digest, ec.ECDSA(hashes.SHA256()))
    return signature

def sign_file_fake(private_key, file_path):
    # Чтение файла
    with open(file_path, 'rb') as f:
        data = f.read()

    # Вычисление хэша
    hasher = hashes.Hash(hashes.SHA256(), default_backend())
    hasher.update(data)
    digest = hasher.finalize()
    digest = digest[:-1]

    # Подпись хэша
    signature = private_key.sign(digest, ec.ECDSA(hashes.SHA256()))
    return signature


def verify_signature(public_key, file_path, signature):
    # Чтение файла
    with open(file_path, 'rb') as f:
        data = f.read()

    # Вычисление хэша
    hasher = hashes.Hash(hashes.SHA256(), default_backend())
    hasher.update(data)
    digest = hasher.finalize()

    # Проверка подписи
    try:
        public_key.verify(signature, digest, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False


def save_private_key(private_key, filename):
    with open(filename, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))


def load_private_key(filename):
    with open(filename, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def save_public_key(public_key, filename):
    with open(filename, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def load_public_key(filename):
    with open(filename, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return public_key


def save_signature(signature, filename):
    with open(filename, 'wb') as f:
        f.write(signature)


def load_signature(filename):
    with open(filename, 'rb') as f:
        signature = f.read()
    return signature


def gost_sign():
    private_key, public_key = generate_key_pair()

    file_path = "TEST_DATA/input.txt"

    # Подписываем файл
    signature = sign_file(private_key, file_path)
    signatureF = sign_file_fake(private_key, file_path)

    # Сохраняем ключи
    save_private_key(private_key, "obj/private_key.gost.pem")
    save_public_key(public_key, "obj/public_key.gost.pem")

    # Сохраняем подпись
    save_signature(signature, "obj/signature.gost.bin")

    # Загружаем ключи
    loaded_private_key = load_private_key("obj/private_key.gost.pem")
    loaded_public_key = load_public_key("obj/public_key.gost.pem")

    # Загружаем подпись
    loaded_signature = load_signature("obj/signature.gost.bin")

    # Проверяем подпись
    if verify_signature(loaded_public_key, file_path, signatureF):
        print("Подпись верна.")
    else:
        print("Подпись неверна.")
