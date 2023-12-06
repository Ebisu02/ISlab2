from Голосование.server import Server
from Голосование.client import Client
from Голосование.vote import Vote


def simulate():
    server = Server()

    client = Client(server, 'Alice')
    client.vote(Vote.YES)

    client = Client(server, 'Bob')
    client.vote(Vote.ABSTAIN)

    client = Client(server, 'Tom')
    client.vote(Vote.NO)

    server.get_voting_result()
