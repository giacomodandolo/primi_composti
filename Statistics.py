import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from math import sqrt

class Statistics:
  """
  Allows to store all the statistics needed for the analysis
  of the game, namely:
  - number of played games;
  - payoff of each played game;
  - how many times each player moves first;
  - how many wins and ties for each player.

  This will allow us to calculate:
  - mean, standard deviation, variance of the payoffs;
  - win, tie and lose percentage;
  - going first percentage for each player.

  Lastly, we can print the stats, plot the normal distribution
  of the payoff for each game using normal_distribution() and
  plot the evolution of payoffs over turn using payoff_over_turns().
  """

  def __init__(self, strategies:list[str]):
    """
    Initializes the Statistics object.

    Parameters
      strategies (list[str]): list of strategies' names.
    """
    # payoff
    self.n = 0
    self.payoffs = []
    self.mean = 0
    self.std_dev = 0
    self.variance = 0
    self.average_advantage_turn = []

    # wins/ties
    self.first_moves = [0, 0]
    self.wins = [0, 0]
    self.ties = 0

    # percentages
    self.win_percentage = [0, 0]
    self.tie_percentage = 0
    self.first_percentage = [0, 0]

    # needed for titles
    self.strategies = strategies


  def __str__(self):
    """
    Show all the statistics when printing the object.

    Returns
      str: statistics in text.
    """
    return \
      f"--- Statistics of {self.strategies[0]} VS {self.strategies[1]} ---\n"\
      f"Number of simulations = {self.n}\n"\
      f"Player A win percentage (going first {self.first_percentage[0]}% of times) = {self.win_percentage[0]}%\n"\
      f"Player B win percentage (going first {self.first_percentage[1]}% of times) = {self.win_percentage[1]}%\n"\
      f"Tie percentage = {self.tie_percentage}%\n\n"\
      f"--- Payoff ---\n"\
      f"Mean = {self.mean}\n"\
      f"Standard deviation = {self.std_dev}\n"\
      f"Variance = {self.variance}"


  def update(self, first:int, winner:int, payoff:int, payoffs_turn:list[int]):
    """
    Update the statistics after a single iteration of a game.

    Parameters
      first (int): who played first in the game.
      winner (int): who won the game.
      payoff (int): final payoff of the game.
      payoffs_turn (list[int]): list of each turn's payoff.
    """
    self.n = self.n + 1
    self.payoffs.append(payoff)

    self.first_moves[first] = self.first_moves[first] + 1
    if winner == -1:
      self.ties = self.ties + 1
    else:
      self.wins[winner] = self.wins[winner] + 1

    if len(self.average_advantage_turn) == 0:
      self.average_advantage_turn = payoffs_turn
    else:
      for i in range(len(payoffs_turn)):
        self.average_advantage_turn[i] = self.average_advantage_turn[i] + payoffs_turn[i]


  def calculate(self):
    """
    Calculate the statistics.
    """
    if self.n == 0:
      return

    self.mean = 0
    self.std_dev = 0
    self.variance = 0

    # mean
    self.mean = round(sum(self.payoffs)/self.n, 3)

    # standard deviation and variance
    for i in range(self.n):
      self.variance = self.variance + (self.payoffs[i] - self.mean)**2
    self.variance = round(self.variance / self.n, 3)
    self.std_dev = round(sqrt(self.variance), 3)

    # percentages
    self.win_percentage[0] = round(self.wins[0] / self.n * 100, 2)
    self.win_percentage[1] = round(self.wins[1] / self.n * 100, 2)
    self.tie_percentage = round(self.ties / self.n * 100, 2)
    self.first_percentage[0] = round(self.first_moves[0] / self.n * 100)
    self.first_percentage[1] = round(self.first_moves[1] / self.n * 100)

    for i in range(len(self.average_advantage_turn)):
      self.average_advantage_turn[i] = self.average_advantage_turn[i] / self.n


  def normal_distribution(self):
    """
    Show the normal distribution of the statistics.
    """
    x = np.linspace(self.mean - 3*self.variance, self.mean + 3*self.variance, 1000)
    plt.plot(x, stats.norm.pdf(x, self.mean, self.variance))
    plt.title(f"Normal Distribution: {self.strategies[0]} VS {self.strategies[1]}")
    plt.xlabel("Payoff")
    plt.ylabel("PDF")
    plt.show()


  def estimate_coef(self, x:np.ndarray, y:np.ndarray) -> list[float, float]:
    """
    Estimate the coefficients for regression.

    Parameters
      x (NDArray): x values.
      y (NDArray): y values.

    Returns
      list[float, float]: returns b_0, b_1 coefficients.
    """
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x

    return (b_0, b_1)


  def payoff_over_turns(self):
    """
    Show the graph representing the evolution of mean payoffs over turns.
    """
    x = np.arange(len(self.average_advantage_turn))
    y = self.average_advantage_turn
    plt.scatter(x, y, marker = 'o')

    b = self.estimate_coef(x, y)
    y_pred = b[0] + b[1] * x
    plt.plot(x, y_pred, color = 'red')

    plt.title(f"Mean Payoff over turns: {self.strategies[0]} VS {self.strategies[1]}")
    plt.xlabel("Turn")
    plt.ylabel("Mean Payoff")
    plt.show()
