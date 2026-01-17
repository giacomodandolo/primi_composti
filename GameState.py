from Player import Player
from copy import deepcopy

class GameState:
  """
  Allows to store all the information for a single game state, including
  which set gets played and the payoff of the played set.

  This class is used for the minimax strategy.
  """

  def __init__(self, players:list[Player, Player], table:set[int], u:int, turn:int, current:int, playable_sets:dict[set[int], int], played_set:set[int], played_payoff:int):
    """
    Initializes the GameState object.

    Parameters
      players (list[Player, Player]): list containing players' information.
      table (set[int]): set of cards on the table.
      u (int): current payoff of the game.
      turn (int): current turn of the game.
      current (int): current player.
      playable_sets (dict[set[int], int]): current playable sets of cards.
      played_set (set[int]): played set in the game state.
      played_payoff (int): payoff of the played set.
    """
    self.players = deepcopy(players)
    self.table = table.copy()
    self.u = u
    self.turn = turn
    self.current = current
    self.playable_sets = deepcopy(playable_sets)
    self.played_set = played_set.copy()
    self.played_payoff = played_payoff


  def get_players(self) -> list[Player, Player]:
    """
    Obtain players' state.

    Returns
      list[Player, Player]: players in the game state.
    """
    return self.players


  def get_table(self) -> set[int]:
    """
    Obtain table's state.

    Returns
      set[int]: cards on the table in the game state.
    """
    return self.table


  def get_payoff(self) -> int:
    """
    Obtain the payoff of the game state.

    Returns
      int: payoff in the game state.
    """
    return self.u


  def get_turn(self) -> int:
    """
    Obtain the turn of the game state.

    Returns
      int: turn in the game state.
    """
    return self.turn


  def get_current(self) -> int:
    """
    Obtain the current player of the game state.

    Returns
      int: current player in the game state.
    """
    return self.current


  def get_playable_sets(self) -> dict[set[int], int]:
    """
    Obtain playable sets' state.

    Returns
      dict[set, int]: playable sets in the game state.
    """
    return self.playable_sets


  def get_played_set(self) -> set[int]:
    """
    Obtain played set.

    Returns
      set[int]: played set in the game state.
    """
    return self.played_set


  def get_played_payoff(self) -> int:
    """
    Obtain payoff of the played set.

    Returns
      int: payoff of the played set in the game state.
    """
    return self.played_payoff