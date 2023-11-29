import os
import time
from Шифр.lab2 import generate_prime
from Покер.player import Player
from Покер.cards import get_random_card, CardDeck, find_key, shuffle


def register_game():
    print("Введите имена игроков через пробел.\n"
          "Количество игроков должно находиться в диапазоне от 2 до 9:")
    names = input()
    names = names.split(" ")
    amount_of_players = len(names)
    if amount_of_players > 9 or amount_of_players < 2:
        return None
    return names


def initialization(names):
    p = generate_prime(bits=16)
    players = []
    for name in names:
        pl = Player(name)
        pl.generate_keys(p)
        players.append(pl)
        time.sleep(1)
    print("Игроки инициализированы.")
    time.sleep(1)
    print("##### NEXT STAGE ######")
    return players, p


def encrypt_hand(cards, c, p):
    i = 0
    for card in cards:
        u = pow(card, c, p)
        cards[i] = u
        i += 1
    return cards


def deal_cards(players, deck):
    for pl in players:
        hand = []
        card = get_random_card(deck)
        hand.append(card)
        del deck[0]
        card = get_random_card(deck)
        hand.append(card)
        del deck[1]
        pl.hand = hand


def decode_hand(target, players, p):
    for pl in players:
        if pl != target:
            hand = target.hand
            fc = pow(hand[0], pl.d, p)
            sc = pow(hand[1], pl.d, p)
            hand = [fc, sc]
            target.hand = hand
    hand = target.hand
    fc = pow(hand[0], target.d, p)
    sc = pow(hand[1], target.d, p)
    hand = [fc, sc]
    target.hand = hand


def table_card_deal(current_deck, players, p):
    bord = []
    for i in range(5):
        card = current_deck[0]
        del current_deck[0]
        for player in players:
            card = pow(card, player.d, p)
        card = find_key(CardDeck, card)
        bord.append(card)
    return bord


def start_poker(players, p):
    shuffled_cards = [x for x in range(2, 54)]
    # shuffle & encode for each
    for player in players:
        shuffled_cards = shuffle(shuffled_cards)
        shuffled_cards = encrypt_hand(shuffled_cards, player.c, p)
    # deal
    deal_cards(players, shuffled_cards)
    # decode for each
    for player in players:
        decode_hand(player, players, p)
        player.print_hand()
    # check bord
    bord = table_card_deal(shuffled_cards, players, p)
    # print info
    print("На столе: ", end="")
    for i in bord:
        print(f"{i} ", end="")
    print()


def game():
    names = register_game()
    while names is None:
        os.system("clear")
        print("Ошибка: попробуйте ввести имена еще раз!")
        names = register_game()
    print("##### NEXT STAGE ######")
    players, p = initialization(names)
    start_poker(players, p)
