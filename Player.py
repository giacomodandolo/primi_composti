import random as rand
from util import is_prime

class Player:
  """
  Allows to store and operate on all the information needed for a player, namely:
  - the player's hand;
  - the primes' and composites' stacks.
  """

  # scores of cards
  PRIME_SCORE = 2
  COMPOSITE_SCORE = 1


  def __init__(self):
    """
    Create the Player object, which contains the player's hand, the
    primes' stack and the composites' stack.
    """
    self.hand = set()
    self.primes = list()
    self.composites = list()


  def __str__(self) -> str:
    """
    Show hand, primes' stack and composites' stack when trying to print
    the object.

    Returns
      str: hand, primes' stack and composites' stack in text.
    """
    return f"Hand = {self.hand}\nPrime Stack = {self.primes}\nComposites Stack = {self.composites}"


  ## hand
  def hand_list(self) -> list[int]:
    """
    Return the player's hand as a list instead of as a set.

    Returns
      list[int]: hand of player as a list.
    """
    return list(self.hand)


  def add_hand(self, card:int):
    """
    Add a card to the hand.

    Parameters
      card (int): number related to the card to add.
    """
    self.hand.add(card)


  def remove_hand(self, card:int):
    """
    Remove a card from the hand (if present).

    Parameters:
      card (int): number related to the card to remove.
    """
    if card in self.hand:
      self.hand.remove(card)


  def min_hand(self) -> int:
    """
    Find the minimum in the hand of the player.

    Returns
      int: minimum card value in the hand.
    """
    return min(self.hand)


  def is_hand_empty(self) -> bool:
    """
    Understand if the hand of the player is empty.

    Returns
      bool: if empty return True, otherwise False.
    """
    return len(self.hand) == 0


  def get_random_card(self) -> int:
    """
    Get a random card from the hand.

    Returns
      int: number of the random card.
    """
    return rand.choice(list(self.hand))


  def can_play_move(self, move:set) -> bool:
    """
    Find out if the player can play the move.

    Parameters
      move (set): set of cards defining a move.

    Returns
      bool: True if it can be played, false otherwise.
    """
    return len(self.hand.intersection(move)) != 0


  ## stacks
  def add_stacks(self, card:int):
    """
    Add a card to its respective stack.

    Parameters
      card (int): card to add to the stack.
    """
    # if it's prime
    if is_prime(card):
      if self.prime_contains(card):
        self.remove_prime(card)
      self.add_prime(card)
    # if it's a composite
    else:
      if self.composite_contains(card):
        self.remove_composite(card)
      self.add_composite(card)


  def remove_stacks(self, card:int):
    """
    Remove a card from its respective stack (if present).

    Parameters
      card (int): card to remove from the stack.
    """
    if is_prime(card) and self.prime_contains(card):
      self.remove_prime(card)
    elif not is_prime(card) and self.composite_contains(card):
      self.remove_composite(card)


  ## prime stack
  def add_prime(self, card:int):
    """
    Add a card into the primes' stack.

    Parameters
      card (int): card to add into the primes' stack.
    """
    self.primes.append(card)


  def remove_prime(self, card:int):
    """
    Remove a card from the primes' stack (if present).

    Parameters
      card (int): card to remove from the primes' stack.
    """
    if self.prime_contains(card):
      i = self.primes.index(card)
      self.primes.pop(i)


  def prime_contains(self, card:int) -> bool:
    """
    Check if a card is contained in the primes' stack.

    Returns
      bool: if contained True, otherwise False
    """
    return card in self.primes


  def obtain_last_prime(self) -> int:
    """
    Obtain the last prime put into the primes' stack (if present).

    Returns
      int: last prime if present, otherwise -1.
    """
    if len(self.primes) != 0:
      return self.primes[-1]
    return -1


  ## composite stack
  def add_composite(self, card:int):
    """
    Add a card into the composites' stack.

    Parameters
      card (int): card to add into the composites' stack.
    """
    self.composites.append(card)


  def remove_composite(self, card:int):
    """
    Remove a card from the composites' stack (if present).

    Parameters
      card (int): card to remove from the composites' stack.
    """
    if self.composite_contains(card):
      i = self.composites.index(card)
      self.composites.pop(i)


  def composite_contains(self, card:int) -> bool:
    """
    Check if a card is contained in the composites' stack.

    Returns
      bool: if contained True, otherwise False
    """
    return card in self.composites


  def obtain_last_composite(self) -> int:
    """
    Obtain the last composite put into the composites' stack (if present).

    Returns
      int: last composite if present, otherwise -1.
    """
    if len(self.composites) != 0:
      return self.composites[-1]
    return -1
