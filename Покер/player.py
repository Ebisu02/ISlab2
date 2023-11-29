import random
from Покер.utils import egcd, gen_evklid_u
from Покер.cards import find_key, CardDeck


class Player:
    def __init__(self, name) -> None:
        self.__name = name
        # gen keys
        self.__c = 2
        self.__d = 2
        self.__hand = [0, 0]
        print(f"Добавлен игрок {name}!")

    @property
    def name(self):
        return self.__name

    @property
    def hand(self):
        return self.__hand

    @property
    def c(self):
        return self.__c

    @property
    def d(self):
        return self.__d

    @hand.setter
    def hand(self, hand):
        if hand[0] > 0 and hand[1] > 0:
            self.__hand = hand
        else:
            print("Ошибка: такой карты не существует!")

    def print_hand(self):
        hand = self.__hand
        fc = find_key(CardDeck, hand[0])
        sc = find_key(CardDeck, hand[1])
        print(f"{self.__name}:\t{fc} {sc}")

    def print_keys(self):
        return f"{self.__name}:\nC = {self.__c}\tD = {self.__d}"

    def generate_keys(self, p):
        c = self.__c
        d = self.__d
        while (c * d) % (p - 1) != 1:
            while True:
                c = random.randint(1, p - 1)
                if egcd(p - 1, c) == 1:
                    break
            u = gen_evklid_u(p - 1, c)
            d = u[2]
            if d < 0:
                d += p
        self.__c = c
        self.__d = d
