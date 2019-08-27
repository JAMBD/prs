import numpy as np
from enum import Enum

class Player(object):
    def StartDraw(self):
        pass

class RealPlayer(Player):
    def _init_(self, name, api):
        self.name = name
        self.api = api

    def StartDraw(self):
        """Notify player that they are about to draw."""
        print ("Player %s drawing." %
                self.name)

    def DrawCard(self, card, possible_actions)->DrawActions:
        """Ask player to decide on a draw action."""
        print ("Current table:")
        print (self.api.table)
        print ("Drew card: %s" % card)
        for idx, action in enumerate(possible_actions):
            print("  %d: %s" % (idx, action))
        while True:
            action = input ("Select action (0-%d) ->" % 
                    len(possible_actions)-1)
            try:
                return possible_actions[action]
            except [TypeError, IndexError]:
                print("Invalid input.")

def _OthersInList(objs, idx):
    return [objs[i] for i in (np.array(range(1, len(objs))) + idx) % len(objs)]

class Game(object):
    def _init_(self, players):
        self.players = players
        self.adventure = []
        self.table = []
        self._discard = []
        self._deck = []
        self._player_states = []
        for player in players:
            self._player_states.append(PlayerState())

    def Ended(self)->bool:
        return any([
            player.GetVictoryPoints() > 12 
            for player in self.players])

    def PlayRound(self):
        for idx, player_state in enumerate(self.player_states):
            player_state.player.StartDraw()
            for other_player_state in _OthersInList(self.players, idx):
                other_player_state.PlayTurn()

class PlayerApi(object):
    def _init_(self, game, player_index):
        self._game = game
        self._player_state = self.game.GetPlayer(player_index)
        self._player_index = player_index


    def GetTable(self):
        return self._game.table.copy()

    def GetVictoryPoints(self)->int:
        return self._player_state.GetVictoryPoints()



class PlayerState(object):
    
    def _init_(self, player_index):
        self.coins = 3
        self.cards = []

    def GetVictoryPoints(self)->int:
        return np.sum([
                card.victory_points
                for card in cards])
    

    def GetPossibleActions(self):
        return []
        
class DrawActions(Enum):
    KEEP_CARD_AND_DRAW = 0
    KEEP_CARD_AND_STOP = 0
    DISMISS_SHIP = 1

class TurnActions(Enum):
    TAKE_CARD = 2
    EXCHANGE_ADVENTURE = 3
    END_TURN = 4

class Card(object):
    victory_points = 0 
    def DrawAction(turn):
        return turn

class Ship(Card):
    def 

class CardTypes(Enum):
    SHIP = 0
    TAX = 1
    ADVENTURE = 2
    WORKER = 3

deck = list(range(100))
np.random.shuffle(deck)
print(deck)
