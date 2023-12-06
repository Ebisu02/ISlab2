from Голосование.utils import *
from Голосование.vote import Vote

import hashlib
import sys


class Server:
    def __init__(self):
        p = q = get_prime(1 << 1023, (1 << 1024) - 1)
        while p == q:
            q = get_prime(1 << 1023, (1 << 1024) - 1)
        phi = (p - 1) * (q - 1)

        self.n = p * q
        # Public key
        self.d = get_mut_prime(phi)
        # Private key
        self._c = inverse(self.d, phi)
        self._voted = set()
        self.votes = list()
        print("[LOG] Server variables:")
        print(f"{p = }",
              f"{q = }",
              f"{phi = }",
              f"{self.n = }",
              f"Public key = {self.d}",
              f"Private key = {self._c}",
              sep='\n')
        print("[SERVER] Server Started!")

    def check_and_send_blank(self, name: str, hh: int) -> int:
        print(f"[SERVER] Get request to get blank from {name}")
        if name in self._voted:
            print(f"[SERVER] User [{name}] already voted")
            return None
        else:
            print(f"[SERVER] Blank sended to {name}")
            self._voted.add(name)
            return exp_mod(hh, self._c, self.n)

    def send_and_verify_blank(self, n: int, s: int) -> bool:
        print(f"[SERVER] Get a blank")
        hash = hashlib.sha3_512(n.to_bytes(math.ceil(n.bit_length() / 8), byteorder=sys.byteorder))
        hash_16 = hash.hexdigest()
        hash_10 = int(hash_16, base=16)
        if hash_10 == exp_mod(s, self.d, self.n):
            self.votes.append((n, s))
            print(f'[SERVER] Blank verified!')
            return True
        else:
            print(f'[SERVER] Verification failed, this blank is fake!')
            print(f"\t{hash_10 = }", f"\t{exp_mod(s, self.d, self.n) = }", sep='\n')
            return False

    def get_voting_result(self):
        votes = dict([(i, 0) for i in Vote])
        for n, s in self.votes:
            votes[Vote(n & (~((~0) << len(Vote) - 1)))] += 1
        print("[SERVER] Vote result:")
        print(*(f"\t{key.name} = {value}" for key, value in votes.items()), sep='\n')