from Голосование.vote import Vote
from Голосование.server import Server
from Голосование.utils import *

import hashlib
import sys


class Client:
    def __init__(self, server: Server, name: str = 'Client'):
        self.server = server
        self.name = name

    def vote(self, vote: Vote):
        # Хэширование голоса и запрос бюллетеня
        rnd = gen_prime(1 << 511, (1 << 512) - 1)
        n = rnd << 512 | vote.value

        r = gen_mutually_prime(self.server.n)

        hash = hashlib.sha3_512(n.to_bytes(math.ceil(n.bit_length() / 8), byteorder=sys.byteorder))
        hash_16 = hash.hexdigest()
        hash_10 = int(hash_16, base=16)

        hh = hash_10 * exponentiation_modulo(r, self.server.d, self.server.n) % self.server.n
        ss = self.server.get_blank(self.name, hh)

        if ss:
            # Вычисление подписи бюллетеня
            s = ss * inverse(r, self.server.n) % self.server.n
            # Отправка голоса на сервер
            if self.server.set_blank(n, s):
                print(f"[CLIENT] {self.name}, Ваш бюллетень принят")
            else:
                print(f"[CLIENT] {self.name}, Ваш бюллетень не прошел проверку на сервере и не был принят")
        else:
            print(f"[CLIENT] {self.name}, Вы уже проголосовали")