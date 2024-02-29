# Name: Vihaan Mathur
# Date: 11/20/21
#This is a fully playable Othello application using various AI algorithms to build an AI bot for humans to play against.
#Algorithms: MiniMax Algorithm & Alpha/Beta

import random

class RandomBot:
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = 8
      self.y_max = 8

   def best_strategy(self, board, color):
      # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      
      ''' Your code goes here ''' 
      moves = list(self.find_moves(board, color))
      move = random.choice(moves)
      best_move = [move//8, move%8] # change this
      return best_move, 0

   def stones_left(self, board):
    # returns number of stones that can still be placed (empty spots)
      count = 0
      for x in board: 
         for pee in x:
            if(pee == '.'):
               count += 1
      return pee

   def find_moves(self, board, color):
    # finds all possible moves
      moves_found = {}
      for i in range(len(board)):
        for j in range(len(board[i])):
            flipped_stones = self.find_flipped(board, i, j, color)
            if len(flipped_stones) > 0:
                moves_found.update({i*self.y_max+j: flipped_stones})
      return moves_found

   def find_flipped(self, board, x, y, color):
    # finds which chips would be flipped given a move and color
      if board[x][y] != ".":
        return []
      if color == self.black:
        my_color = "@"
      else:
        my_color = "O"
      flipped_stones = []
      for incr in self.directions:
        temp_flip = []
        x_pos = x + incr[0]
        y_pos = y + incr[1]
        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if board[x_pos][y_pos] == ".":
                break
            if board[x_pos][y_pos] == my_color:
                flipped_stones += temp_flip
                break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
      return flipped_stones

class Best_AI_bot:

   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = 8
      self.y_max = 8

   def best_strategy(self, board, color):
    # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      
      best_move = self.alphabeta(board, color, 1, -999999, 9999999)
      return best_move, 0

   def minimax(self, board, color, search_depth):
    # returns best "value"
      return 1

   def negamax(self, board, color, search_depth):
    # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
    # returns best "value" while also pruning
      moves = self.find_moves(board, color)
      best_value = -999999999
      for n in moves:
         move = (n//8, n%8)
         new_board = self.make_move(board, color, n, self.find_flipped(board, n//8, n%8, color))

      new_value = self.min_value(new_board, self.opposite_color[color], search_depth, alpha, beta)
      if new_value > best_value:
         best_value = new_value 
         best_move = move
      return best_move
   
   def max_value(self, board, color, search_depth, alpha, beta):
   # return value and state: (val, state)
      if(self.stones_left(board) == 0 or len(self.find_moves(board, color)) == 0 or search_depth == 4):
         return self.evaluate(board, color, self.find_moves(board, color))
      v = -9999999999999
      for a in self.find_moves(board, color):
         v = max(v, self.min_value(self.make_move(board, color, a, self.find_flipped(board, a//8, a%8, color)), self.opposite_color[color], search_depth+1, alpha, beta), alpha, beta)
         if v > beta:
            return v
         alpha = max(alpha, v)
      return v

   
   def min_value(self, board, color, search_depth, alpha, beta):
      # return value and state: (val, state)
      if(self.stones_left(board) == 0 or len(self.find_moves(board, color)) == 0 or search_depth == 4):
         return self.evaluate(board, color, self.find_moves(board, color))
      v = 9999999999999
      for a in self.find_moves(board, color):
         v = min(v, self.max_value(self.make_move(board, color, a, self.find_flipped(board, a//8, a%8, color)), self.opposite_color[color], search_depth+1, alpha, beta), alpha, beta)
         if v < alpha:
            return v
         alpha = min(beta, v)
      return v

   def make_key(self, board, color):
    # hashes the board
      return 1

   def stones_left(self, board):
    # returns number of stones that can still be placed
      count = 0
      for x in board: 
         for pee in x:
            if(pee == '.'):
               count += 1
      return pee

   def make_move(self, board, color, move, flipped):
    # returns board that has been updated
      new_board = [x[::] for x in board]
      moving = [move//8, move%8] 
      new_board[moving[0]][moving[1]] = color
      for x in flipped:
         a = x[0]
         b = x[1]
         new_board[a][b] = self.opposite_color[color]
      return new_board

   def evaluate(self, board, color, possible_moves):
    # returns the utility value
      return (len(possible_moves))

   def score(self, board, color):
    # returns the score of the board 
      return 1

   def find_moves(self, board, color):
    # finds all possible moves
      moves_found = {}
      for i in range(len(board)):
        for j in range(len(board[i])):
            flipped_stones = self.find_flipped(board, i, j, color)
            if len(flipped_stones) > 0:
                moves_found.update({i*self.y_max+j: flipped_stones})
      return moves_found

   def find_flipped(self, board, x, y, color):
    # finds which chips would be flipped given a move and color
      if board[x][y] != ".":
        return []
      if color == self.black:
        my_color = "@"
      else:
        my_color = "O"
      flipped_stones = []
      for incr in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
        temp_flip = []
        x_pos = x + incr[0]
        y_pos = y + incr[1]
        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if board[x_pos][y_pos] == ".":
                break
            if board[x_pos][y_pos] == my_color:
                flipped_stones += temp_flip
                break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
      return flipped_stones
