import discord
from Card import cards,card_5
class User:
    def __init__(self, identifier):
        self.identifier = identifier
        self.deck = cards.copy()
        self.power_inhand = 0
