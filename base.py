#!/usr/bin/python3

import copy
import numpy as np
from enum import Enum
from abc import ABC
from abc import abstractmethod

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


class CardTypes(Enum):
    SHIP = 0
    TAX = 1
    ADVENTURE = 2
    WORKER = 3



class Player(ABC):

    @abstractmethod
    def StartGame(self, game):
        """Notify player that the game is starting."""
        pass

    @abstractmethod
    def StartDraw(self, game):
        """Notify player that they are about to draw."""
        pass

    @abstractmethod
    def DrawCard(self, game_state, card)->DrawActions:
        """Ask player to decide on a draw action."""
        pass

class RealPlayer(Player):
    def __init__(self, name, player_index):
        self.name = "%d" % player_index
        self.player_index = player_index

    def StartGame(self, game_state):
        self.name = input ("Enter name for player %d ->" % self.player_index)

    def StartDraw(self, game_state):
        print ("Player %s drawing." % self.name)

    def DrawCard(self, game_state, card)->DrawActions:
        print ("Current table:")
        print (game_state.table)
        print ("Drew card: %s" % card)
        possible_actions = game.GetPossibleDrawActions(self.player_index)
        for idx, action in enumerate(possible_actions):
            print("  %d: %s" % (idx, action))
        while True:
            action = input ("Select action (0-%d) ->" % 
                    len(possible_actions)-1)
            try:
                return possible_actions[action]
            except [TypeError, IndexError]:
                print("Invalid input.")

    def StartTurn (self, game_state):
        print ("Player %s's turn." % self.name)



def _OthersInList(objs, idx):
    return [objs[i] for i in (np.array(range(1, len(objs))) + idx) % len(objs)]


class GameState(object):
    def __init__(self):
        self.table = []

    def GetDrawResults(self):
        return self.table, self.discarded_ships

    def GetPossibleDrawActions(self, player_index):
        return [KEEP_CARD_AND_STOP]

    def GetPossibleTurns(self, player_index):
        return [END_TURN]

    def ApplyTurn(self, player_index, turn):
        self.table 

class Game(object):
    def __init__(self, players):
        self.player_states = []
        self.adventure = []
        self.table = []
        self.drawn = []
        self._discard = []
        self._deck = []
        self._players = []
        for idx, player in enumerate(players):
            self.player_states.append(PlayerState(idx))
            self._players.append(player(idx))
    
    def GetPlayerState(self, player_index):
        return self._player_states[player_index]

    def Ended(self)->bool:
        return any([player.GetVictoryPoints() > 12 for player in self.players])

    def PlayRound(self):
        for idx, player_state in enumerate(self.player_states):
            self.drawn = []
            self._discard += np.random.shuffle(self.table)
            self.table = []

            player_state.player.StartDraw()


        for other_player_state in _OthersInList(self.players, idx):
            other_player_state.PlayTurn()


class PlayerState(object):
    def __init__(self):
        self.coins = 3
        self.cards = []

    def GetVictoryPoints(self)->int:
        return np.sum([card.victory_points for card in cards])


deck = list(range(100))
np.random.shuffle(deck)
print(deck)
