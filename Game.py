from Player import Player
from Statistics import Statistics
from GameState import GameState
from util import is_prime
import random as rand
import sys

class Game:
  """
  Allows to play the two player game, either with a single simulation with
  simulate() or as multiple simulations with statistics with multiple_simulate().

  The strategies that can be played are random, greedy and minimax.
  Minimax can be played with a certain depth, which can be set.
  """

  # player indexes
  A = 0
  B = 1
  PLAYER_TAGS = ['A', 'B']

  # scores of cards
  PRIME_SCORE = 2
  COMPOSITE_SCORE = 1

  # possible strategies
  RANDOM = "random"
  GREEDY = "greedy"
  MINIMAX = "minimax"


  # game setting methods
  def __init__(self, num_cards:int, num_hand:int, num_table:int, change_first:bool = True, depth:int = 1):
    """
    Initialize the Game instance.

    Parameters
      num_cards (int): number of cards in the game.
      num_hand (int): number of cards in the hand of each player.
      num_table (int): number of cards left on the table at the end of dealing.
      change_first (bool): keep A as the first player (False) or change it based on the rules of the game (True).
      depth (int): depth for the minimax algorithm, if needed.
    """
    self.num_cards = num_cards
    self.num_hand = num_hand
    self.num_table = num_table
    self.change_first = change_first
    self.depth = depth
    if num_cards != num_hand*2 + num_table:
      print(f"The parameters given for the Game object are not coherent. ({num_cards} != 2*{num_hand} + {num_table})")
      sys.exit()
    self.reset()


  def reset(self):
    """
    Reset the status of the game.
    """
    self.turn = 1
    self.u = 0
    self.players = list([Player(), Player()])
    self.table = set()

    self.turn_payoffs = []
    self.deal_cards()
    self.find_first_player()
    self.find_playable_sets()


  def is_over(self) -> bool:
    """
    Check if the game is over. The game is over when both
    of the players have an empty hand.

    Returns
      bool: True if the game is over, False otherwise.
    """
    emptyA = self.players[self.A].is_hand_empty()
    emptyB = self.players[self.B].is_hand_empty()
    return emptyA and emptyB


  def get_winner(self) -> int:
    """
    Calculate the winner.

    Returns
      int: index of the winner, -1 in case of tie.
    """
    winner = -1
    if self.u > 0:
      winner = self.first
    elif self.u < 0:
      winner = (self.first + 1) % 2

    return winner


  # deal cards to players and table
  def deal_cards(self):
    """
    Deal cards to player's hands and on the table.
    """
    cards = list(range(2, self.num_cards + 2))
    rand.shuffle(cards)

    # deal to players
    for nh in range(self.num_hand):
      self.players[self.A].add_hand(cards.pop())
      self.players[self.B].add_hand(cards.pop())

    # put the rest on table
    self.table = set(cards)


  # find playable values for two cards on the table
  def find_playable_cards(self, c1:int, c2:int) -> list[int]:
    """
    Obtain the playable cards based on two cards on the table.

    Parameters
      c1 (int): first card picked from the table.
      c2 (int): second card picked from the table

    Returns
      list[int]: list of playable cards from having c1 and c2 on the table.
    """
    playable_cards = list()

    # addition
    if c1 + c2 > 1 and c1 + c2 < self.num_cards + 2:
      playable_cards.append(c1 + c2)

    # subtraction
    if abs(c1 - c2) > 1 and abs(c1 - c2) < self.num_cards + 2:
      playable_cards.append(abs(c1 - c2))

    # multiplication
    if c1 * c2 > 1 and c1 * c2 < self.num_cards + 2:
      playable_cards.append(c1 * c2)

    # integer division
    if (c1 // c2 > 1 and c1 // c2 < self.num_cards + 2) and c1 % c2 == 0:
      playable_cards.append(c1 // c2)
    if (c2 // c1 > 1 and c2 // c1 < self.num_cards + 2) and c2 % c1 == 0:
      playable_cards.append(c2 // c1)

    return playable_cards


  # calculate the payoff of a card_set
  def calculate_move_payoff(self, card_set:set[int]) -> int:
    """
    Calculate score based on obtained and stolen card sets.

    Parameters
      card_set (set[int]): set of 1 or 3 cards defining a playable card set.

    Returns
      int: single payoff of a single move.
    """
    if len(card_set) != 3:
      return 0

    payoff = 0
    # p1 is the current player, p2 is the other player
    p1 = self.players[self.current]
    p2 = self.players[(self.current + 1) % 2]

    for c in card_set:
      is_pr = is_prime(c)

      # obtained
      if is_pr and not p1.prime_contains(c):
        payoff = payoff + self.PRIME_SCORE
      elif not is_pr and not p1.composite_contains(c):
        payoff = payoff + self.COMPOSITE_SCORE

      # stolen
      if is_pr and p2.prime_contains(c):
        payoff = payoff + self.PRIME_SCORE
      elif not is_pr and p2.composite_contains(c):
        payoff = payoff + self.COMPOSITE_SCORE

    return payoff


  # find the playable cards set
  def find_playable_sets(self):
    """
    Obtain the playable sets of cards, calculating the relative payoff
    associated with each specific set of cards.
    """
    table_list = list(self.table)
    self.playable_sets = dict()

    for i in range(len(table_list)):
      for j in range(i+1, len(table_list)):
        # obtain table cards
        c1 = table_list[i]
        c2 = table_list[j]

        # find the playable cards based on the table cards
        playable_cards = self.find_playable_cards(c1, c2)
        for c3 in playable_cards:
          s = {c1, c2, c3}
          if len(s) == 3:
            self.playable_sets[frozenset(s)] = self.calculate_move_payoff(s)

    for c in self.players[self.current].hand_list():
      self.playable_sets[frozenset({c})] = 0


  # find who plays first
  def find_first_player(self):
    """
    Find the player who plays first in the game, if needed.
    """
    if self.change_first:
      minA = self.players[self.A].min_hand()
      minB = self.players[self.B].min_hand()
      self.first = self.A if minA < minB else self.B
      self.current = self.first
    else:
      self.first = self.A
      self.current = self.first


  # random play
  def random_play(self) -> list[set[int], int]:
    """
    Play a random card in hand.

    Returns
      list[set[int], int]: return the set of cards played and its payoff.
    """
    p = self.players[self.current]
    card = p.get_random_card()

    for k, v in self.playable_sets.items():
      if card in k:
        return k, v

    return {card}, 0


  # greedy play
  def greedy_play(self) -> list[set[int], int]:
    """
    Play a card using a greedy approach.

    Returns
      list[set[int], int]: return the set of cards played and its payoff.
    """
    p = self.players[self.current]
    max_payoff = 0
    max_move = {p.get_random_card()}

    for k, v in self.playable_sets.items():
      if p.can_play_move(k) and v > max_payoff:
        max_payoff = v
        max_move = k

    return max_move, max_payoff


  def update(self, move:set[int], payoff:int):
    """
    Update the game state after a move.

    Parameters
      move (set[int]): played move.
      payoff (int): payoff of the played move.
    """
    self.update_players(move)
    self.update_table(move)
    gain = 1 if self.first == self.current else -1
    self.u = self.u + gain * payoff
    self.turn = self.turn + 1
    self.current = self.B if self.current == self.A else self.A
    self.find_playable_sets()


  def rollback(self, game_state:GameState):
    """
    Rollbacks to a previous game state.

    Parameters
      game_state (GameState): previous game state.
    """
    self.players = game_state.get_players()
    self.table = game_state.get_table()
    gain = 1 if self.first == self.current else -1
    self.u = game_state.get_payoff()
    self.turn = game_state.get_turn()
    self.current = game_state.get_current()
    self.playable_sets = game_state.get_playable_sets()


  def minimax(self, game_states:list[GameState], alpha:int, beta:int) -> list[set[int], int]:
    """
    Apply minimax recursively until the required depth is reached. This uses
    Alpha-Beta Pruning to make the algorithm faster by not searching useless
    branches.

    Parameters
      game_states (list[GameState]): list of the game states until the current depth.
      alpha (int): alpha factor.
      beta (int): beta factor.

    Returns
      list[set[int], int]: return the set of cards played and its payoff.
    """

    # if the game is over or if the depth is reached, then we
    # have a terminal state and we return dummy values
    if self.is_over() or len(game_states) >= self.depth:
      minimax_move = {}
      minimax_payoff = 0
      return minimax_move, minimax_payoff

    minimax_payoff = 0
    minimax_move = {}
    maximizing_player = (self.turn % 2 == 0)

    # maximizing player
    if maximizing_player:
      minimax_payoff = float("-inf")
      for k, v in self.playable_sets.items():
        p = self.players[self.current]
        if p.can_play_move(k):
          # initialize with a playable move
          if len(minimax_move) == 0:
            minimax_move = k

          # add the current game state to the list of game states
          game_state = GameState(self.players, self.table, self.u, self.turn, self.current, self.playable_sets, k, v)
          game_states.append(game_state)

          # update the current state of the game
          self.update(k, v)

          # obtain the minimax move from the next player
          next_move, next_payoff = self.minimax(game_states, alpha, beta)

          # calculate the payoff of the current path and check if it's the maximum payoff
          payoff = next_payoff + v
          if payoff > minimax_payoff:
            minimax_payoff = payoff
            minimax_move = k

          # rollback the game state
          gs = game_states.pop()
          self.rollback(gs)

          # update alpha and apply pruning
          alpha = max(alpha, minimax_payoff)
          if beta <= alpha:
            break
    # minimizing player
    else:
      minimax_payoff = float("+inf")
      for k, v in self.playable_sets.items():
        p = self.players[self.current]
        if p.can_play_move(k):
          # initialize with a playable move
          if len(minimax_move) == 0:
            minimax_move = k

          # add the current game state to the game states
          game_state = GameState(self.players, self.table, self.u, self.turn, self.current, self.playable_sets, k, v)
          game_states.append(game_state)

          # update the current state of the game
          self.update(k, v)

          # obtain the max move from the next player
          next_move, next_payoff = self.minimax(game_states, alpha, beta)

          # calculate the payoff of the current path and check if it's the minimum payoff
          payoff = next_payoff - v
          if payoff < minimax_payoff:
            minimax_payoff = payoff
            minimax_move = k

          # rollback the game state
          gs = game_states.pop()
          self.rollback(gs)

          # update beta and apply pruning
          beta = min(beta, minimax_payoff)
          if beta <= alpha:
            break

    return minimax_move, minimax_payoff


  # minimax play
  def minimax_play(self) -> list[set[int], int]:
    """
    Play a card using a minimax approach.

    Returns
      list[set[int], int]: return the set of cards played and its payoff.
    """
    game_states = []
    minimax_move, _ = self.minimax(game_states, float("-inf"), float("+inf"))
    minimax_payoff = self.calculate_move_payoff(minimax_move)

    return minimax_move, minimax_payoff


  # update the players
  def update_players(self, cards:set[int]):
    """
    Update players after playing a set of cards.

    Parameters
      cards (set[int]): cards played during the turn.
    """
    # p1 is the current player, p2 is the other player
    p1 = self.players[self.current]
    p2 = self.players[(self.current + 1) % 2]

    # remove from the table the last prime and the
    # last composite of p1 (if present)
    last_prime = p1.obtain_last_prime()
    if last_prime != -1 and last_prime in self.table:
      self.table.remove(last_prime)

    last_composite = p1.obtain_last_composite()
    if last_composite != -1 and last_composite in self.table:
      self.table.remove(last_composite)

    # for each card played, remove cards from player stacks
    # (if present), and then remove from the current player's hand
    for c in cards:
      if len(cards) == 3:
        p1.remove_stacks(c)
        p2.remove_stacks(c)
      p1.remove_hand(c)

    # add cards to the stacks if the play was a combination
    if len(cards) == 3:
      for c in cards:
        p1.add_stacks(c)


  def update_table(self, cards:set[int]):
    """
    Update the table after playing a set of cards.

    Parameters
      cards (set[int]): cards played during the turn.
    """
    # p1 is the current player, p2 is the other player
    p1 = self.players[self.current]
    p2 = self.players[(self.current + 1) % 2]

    # if a card played was on the table, then remove it,
    # and add it again if it wasn't in a combination
    for c in cards:
      if c in self.table:
        self.table.remove(c)

      if len(cards) != 3:
        self.table.add(c)

    # add to the table the last prime and the
    # last composite of p1 (if present)
    last_prime = p1.obtain_last_prime()
    if last_prime != -1:
      self.table.add(last_prime)

    last_composite = p1.obtain_last_composite()
    if last_composite != -1:
      self.table.add(last_composite)

    # add to the table the last prime and the
    # last composite of p2 (if present)
    last_prime = p2.obtain_last_prime()
    if last_prime != -1:
      self.table.add(last_prime)

    last_composite = p2.obtain_last_composite()
    if last_composite != -1:
      self.table.add(last_composite)


  def simulate(self, strategies:list[str], enable_print:bool = True) -> list[int, int, int]:
    """
    Simulate the game using defined strategies.

    Parameters
      strategies (list[str]): list of strategies, ordered by player.
      enable_print (bool): enable printing the outputs.

    Returns
      list[int, int, int]: list with (in order) who went first,
                           who won and the final payoff of the game
    """
    while not self.is_over():
      player = self.PLAYER_TAGS[self.current]

      # print the state of the game before the turn
      if enable_print:
        print("-"*10, f"Turn {self.turn} > Player {player}", "-"*10)
        print(f"\n> Before")
        print(f"Table = {self.table}")
        print(f"{self.players[self.current]}")

      # find the move associated with the strategy of a player
      if strategies[self.current] == self.RANDOM:
        play, payoff = self.random_play()

      if strategies[self.current] == self.GREEDY:
        play, payoff = self.greedy_play()

      if strategies[self.current] == self.MINIMAX:
        play, payoff = self.minimax_play()

      # play the found move
      if enable_print:
        print(f"\nPlay = {set(play)}, {payoff}")
      self.update_players(play)
      self.update_table(play)

      # print the state of the game after the turn
      if enable_print:
        print(f"\n> After")
        print(f"Table = {self.table}")
        print(f"{self.players[self.current]}\n")

      # calculate the payoff of the game after the move
      # gain is used to determine if you should remove (-1)
      # or add (+1) the payoff obtained from the move
      gain = 1 if self.first == self.current else -1
      self.u = self.u + gain * payoff
      self.turn_payoffs.append(self.u)
      if enable_print:
        print(f"Current Payoff: {self.u}\n")

      # update turn, current player and playable sets
      self.turn = self.turn + 1
      self.current = self.B if self.current == self.A else self.A
      self.find_playable_sets()

    # print the winner
    winner = self.get_winner()
    if enable_print:
      print("-"*40)
      if winner == -1:
        print("The game ends in a tie!")
      else:
        print(f"Player {self.PLAYER_TAGS[winner]} wins!")

    return self.first, winner, self.u


  def multiple_simulate(self, n:int, strategies:list[str], enable_print:bool = False) -> Statistics:
    """
    Runs multiple simulations and calculates statistics using
    the Monte Carlo method.

    Parameters
      n (int): number of simulations.
      strategies(list[str]): list of strategies, ordered by player.

    Returns
      Statistics: statistics of the multiple simulations.
    """
    game_stats = Statistics(strategies)

    # run simulations
    for i in range(n):
      first, winner, u = self.simulate(strategies, enable_print)
      game_stats.update(first, winner, u, self.turn_payoffs)
      self.reset()

    # calculate stats
    game_stats.calculate()
    return game_stats
