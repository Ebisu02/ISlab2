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
        # Hash vote and blank request
        rnd = get_prime(1 << 511, (1 << 512) - 1)
        n = rnd << 512 | vote.value

        r = get_mut_prime(self.server.n)

        hash = hashlib.sha3_512(n.to_bytes(math.ceil(n.bit_length() / 8), byteorder=sys.byteorder))
        hash_16 = hash.hexdigest()
        hash_10 = int(hash_16, base=16)

        hh = hash_10 * exp_mod(r, self.server.d, self.server.n) % self.server.n
        ss = self.server.check_and_send_blank(self.name, hh)

        if ss:
            # Вычисление подписи бюллетеня
            s = ss * inverse(r, self.server.n) % self.server.n
            # Отправка голоса на сервер
            if self.server.send_and_verify_blank(n, s):
                print(f"[CLIENT] {self.name}, Blank accepted!")
            else:
                print(f"[CLIENT] {self.name}, Blank didnt verified and denied!")
        else:
            print(f"[CLIENT] {self.name}, You already voted!")