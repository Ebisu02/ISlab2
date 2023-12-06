from Голосование.utils import *
from Голосование.vote import Vote

import hashlib
import sys
import logging


def log_function():
    open('vote.log', 'w').close()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='vote.log')
    global logger
    logger = logging.getLogger(__name__)


class Server:
    def __init__(self):
        p = q = gen_prime(1 << 1023, (1 << 1024) - 1)
        while p == q:
            q = gen_prime(1 << 1023, (1 << 1024) - 1)
        phi = (p - 1) * (q - 1)

        self.n = p * q
        self.d = gen_mutually_prime(phi)  # Открытый ключ
        self._c = inverse(self.d, phi)  # Закрытый ключ
        self._voted = set()
        self.votes = list()
        log_function()
        logger.info(f' p = {p}')
        logger.info(f' q = {q}')
        logger.info(f' phi = {phi}')
        logger.info(f' n = {self.n}')
        logger.info(f' d = {self.d}')
        logger.info(f' c = {self._c}')
        print(
            '*' * 30,
            "[SERVER] Сервер запущен",
            sep='\n'
        )

    def get_blank(self, name: str, hh: int) -> int:
        print(f"[SERVER] Пришел запрос на получение бюллетеня от {name}")
        if name in self._voted:
            print(f"[SERVER] Пользователь {name} уже проголосовал")
            return None
        else:
            print(f"[SERVER] Пользователю {name} отправлен бюллетень")
            self._voted.add(name)
            return exponentiation_modulo(hh, self._c, self.n)

    def set_blank(self, n: int, s: int) -> bool:
        print(f"[SERVER] Получен бюллетень")

        hash = hashlib.sha3_512(n.to_bytes(math.ceil(n.bit_length() / 8), byteorder=sys.byteorder))
        hash_16 = hash.hexdigest()
        hash_10 = int(hash_16, base=16)

        if hash_10 == exponentiation_modulo(s, self.d, self.n):
            self.votes.append((n, s))
            print(f'[SERVER] Полученный бюллетень успешно прошел проверку и был принят')
            return True
        else:
            print(f'[SERVER] Полученный бюллетень не прошел проверку и был отклонён')
            print(f"\t{hash_10 = }", f"\t{exponentiation_modulo(s, self.d, self.n) = }", sep='\n')
            return False

    def get_voting_result(self):
        votes = dict([(i, 0) for i in Vote])
        for n, s in self.votes:
            votes[Vote(n & (~((~0) << len(Vote) - 1)))] += 1
        print("[SERVER] Текущие итоги голосования:")
        print(*(f"\t{key.name} = {value}" for key, value in votes.items()), sep='\n')