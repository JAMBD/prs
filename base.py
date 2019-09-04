#!/usr/bin/python3

import attr
import copy
import numpy as np
from enum import Enum, auto
from abc import ABC
from abc import abstractmethod


class GamePhase(Enum):
    DRAW = auto()
    ACTION = auto()


class DrawAction(Enum):
    DRAW = auto()
    STOP = auto()
    DISMISS_SHIP = auto()


class TurnActionType(Enum):
    TAKE_CARD = auto()
    EXCHANGE_ADVENTURE = auto()
    END_TURN = auto()

@attr.s
class TurnAction(object):
    action: TurnActionType = attr.ib()
    index: int = attr.ib()


class GameState(object):
    def __init__(self):
        self.table = []

    def GetDrawResults(self):
        return self.table, self.discarded_ships

    def GetPossibleDrawActions(self, player_index):
        return [DrawAction.STOP]

    def GetPossibleTurns(self, player_index):
        return [TurnActionType.END_TURN]

    def ApplyTurn(self, player_index, turn):
        self.table 


class Card(object):
    
    def __init__(self):
        self._victory_points = 0
        self._cost = 0

    @property
    def cost(self):
        return self._cost

    @property
    def victory_points(self):
        return self._victory_points

    def ApplyDrawChanges(game_state:GameState, acting_player_index)->GameState:
        """Apply any changed to the gamestate whenthe card is drawn."""
        pass

    def ApplyTakeChanges(game_state:GameState, acting_player_index)->GameState:
        """Apply changes when a player takes the card from the table."""
        pass

    def EnhancePlayerActions(game_state:GameState, acting_player_index)->GameState:
        """Update the list of possible player actions given the properties of the card."""
        pass



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
    def DrawCard(self, game_state, card)->DrawAction:
        """Ask player to decide on a draw action."""
        pass

    @abstractmethod
    def StartTurn (self, game_state):
        """Notify player that they are about to have a turn."""
        pass

    @abstractmethod
    def TurnAction(self, game_state:GameState)->[TurnAction]:
        """Ask player to decide on a list of turn actions."""
        pass



class RealPlayer(Player):
    def __init__(self, player_index):
        self.name = "%d" % player_index
        self.player_index = player_index

    def StartGame(self, game_state):
        self.name = input ("Enter name for player %d > " % self.player_index)

    def StartDraw(self, game_state):
        print ("Player %s is drawing." % self.name)

    def DrawCard(self, game_state):
        print ("Current table:")
        print (game_state.table)
        possible_actions = game_state.GetPossibleDrawActions(self.player_index)
        for idx, action in enumerate(possible_actions):
            print("  %d: %s" % (idx, action))
        while True:
            action = input ("Select action (0-%d) > " % 
                    (len(possible_actions)-1))
            try:
                return possible_actions[int(action)]
            except [TypeError, IndexError]:
                print("Invalid input.")

    def StartTurn (self, game_state):
        print ("Player %s's turn." % self.name)

    def TurnAction(self, game_state):
        return []




def _OthersInList(objs, idx):
    return [objs[i] for i in (np.array(range(1, len(objs))) + idx) % len(objs)]



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
            self.player_states.append(PlayerState())
            self._players.append(player(idx))
    
    def _GetState(self):
        return GameState()

    def StartGame(self):
        for player in self._players:
            player.StartGame(self._GetState())
    
    def GetPlayerState(self, player_index):
        return self._player_states[player_index]

    def Ended(self)->bool:
        return any([player_state.GetVictoryPoints() > 12 for player_state in self.player_states])

    def PlayRound(self):
        for idx, player in enumerate(self._players):
            self.drawn = []
            np.random.shuffle(self.table)
            self._discard += self.table
            self.table = []

            player.StartDraw(self._GetState())

            while self._GetState().GetPossibleDrawActions(idx):
                player.DrawCard(self._GetState())


        for other_player in _OthersInList(self._players, idx):
            other_player.StartTurn(self._GetState())


class PlayerState(object):
    def __init__(self):
        self.coins = 3
        self.cards = []

    def GetVictoryPoints(self)->int:
        return np.sum([card.victory_points for card in self.cards])

game = Game([RealPlayer, RealPlayer])
game.StartGame()
while not game.Ended():
    game.PlayRound()
