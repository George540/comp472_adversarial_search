# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
##########################################
## skeleton-titactoe.py (Mini-Assignment 2 COMP 472)
## This code contains the execution of the program's main and various methods to
## Implement an adversarial search algorithm for the game "Line 'em up"
## Created by Team Oranges
##########################################

import time

class Game:
	'''
	Let 
	
	Number of blocks on the board
		number_of_blocks = b

	Size of the board (n * n)
		board_size = n

	The amount of consecutive positions needed to win
		lineup_size = s
	'''
	# The variables class Game will use:
	# board_size
	# number_of_blocks
	# lineup_size

	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	
	def __init__(self, board_size=3, number_of_blocks=0, lineup_size=3, recommend = True):

		self.initialize_game()
		
		#Checking board_size values to be within 3 and 10.
		if(board_size >= 3 and board_size <= 10):
			self.board_size = board_size
		else:
			if(board_size < 3):
				print("The board size is too small, defaulting to 3...")
				self.board_size = 3
			elif(board_size > 10):
				print("The board size is too large, defaulting to 10...")
				self.board_size = 10
		
		#Checking the number of blocks b, to be within 0 and 2*n, where n is board_size
		if(number_of_blocks >= 0 and number_of_blocks <= (2 * self.board_size)):
			self.number_of_blocks = number_of_blocks
		else:
			if(number_of_blocks < 0):
				print("Block count is negative, setting to zero as default...")
				self.number_of_blocks = 0
			elif(number_of_blocks > (2 * self.board_size)):
				print("The number of blocks is too much, defaulting to", (2 * self.board_size), "blocks...")
				self.number_of_blocks = 2 * self.board_size

		#Checking the winning line-up size to be within 3 and n, where n is board_size
		if(lineup_size >= 3 and lineup_size <= self.board_size):
			self.lineup_size = lineup_size
		else:
			if(lineup_size < 3):
				print("Line up size is not enough, setting to 3 as default...")
				self.lineup_size = 3
			elif(lineup_size > self.board_size):
				print("The line up size is too big, defaulting to n=", (self.board_size))
				self.lineup_size = self.board_size
		
		#Recommend if the player should receive tips on what move to play next
		self.recommend = recommend
		
	def initialize_game(self):
		self.current_state = [['.','.','.'],
							  ['.','.','.'],
							  ['.','.','.']]
		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		print()
		for y in range(0, self.board_size):
			for x in range(0, self.board_size):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		'''
		Checks if player move is inside game bounds or on an empty slot
		'''
		if px < 0 or px > self.board_size-1 or py < 0 or py > self.board_size-1:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		'''
		Verifies if win condition vertical/horizontal/diagonal lineup_size is met
		'''
		# Vertical win
		pivot_v = '.'
		print("Vertical check:")
		for j in range(0, self.board_size): #iterate through columns first
			for i in range(0, self.board_size-self.lineup_size+1): #iterate through rows after (the arrays themselves)
				pivot_v = self.current_state[i][j]
				#print("[", i, "][", j,"] = ", pivot_v)
				hasFailed = False
				if (pivot_v != '.'):
					for k in range(1, self.lineup_size): #iterate through winning lineup size
						#print("k:", k)
						#print("[", i, "][", (j+k),"]")
						if ((j + k) == self.board_size or pivot_v != self.current_state[i][j+k]):
							hasFailed = True
							break
					if not hasFailed:return pivot_v #if the third loop iterates entirely, it means a lineup was found. Return the pivot
		# Horizontal win
		#Create what the winning line ups will look like horizontally in the form of a string
		#review: think it's supposed to be line_up size? not board size?
		print("Horizontal check:")
		horizontal_winX = 'X' * self.lineup_size
		horizontal_winO = 'O' * self.lineup_size
		for i in range(0, self.board_size):
			current_row = ''.join(self.current_state[i]) # turn array into string: for example, ['X', 'O', 'X'] -> 'XOX'
			print(self.current_state[i])
			print(current_row)
			if (horizontal_winX in current_row):return 'X'
			elif (horizontal_winO in current_row):return 'O'

		# Main diagonal win
		print("Main diag check:")
		pivot_d1 = '.'
		#iterate through rows first
		for i in range(0, self.board_size-self.lineup_size+1): # must consider a limit for the diagonal size
			for j in range(0, self.board_size-self.lineup_size+1):
				# print("i:", i, ",j:", j)
				# print("value:",self.current_state[i][j])
				pivot_d1 = self.current_state[i][j]
				hasFailed = False
				if (pivot_d1 != '.'):
					for k in range(1, self.lineup_size):
						# print(k)
						# print("[",i+k,"],[",j+k,"]")
						if (pivot_d1 != self.current_state[i+k][j+k]): #iterate diagonally
							hasFailed = True
							break
					if not hasFailed:return pivot_d1

		# Second diagonal win
		print("Second diag check:")
		decrement = self.board_size - 1
		previous = '.'
		count = 0
		for i in range(0 , self.board_size):
			if(i > (self.board_size - self.lineup_size) and count == 0):
				#(self.board_size - self.lineup_size) is the last possible index that the second diag win can be found given the value of self.lineup_size
				#ie second diag cannot be found here
				break
			if(self.current_state[i][decrement] != '.' and self.current_state[i][decrement] != '#'):
				if(self.current_state[i][decrement]=='X'):
					if(count == 0):
						count = count + 1
					elif(self.current_state[i][decrement] == previous):
						count = count + 1
					else:
						count = 0
					if(count == self.lineup_size):
						return 'X'
					previous = 'X'
				elif(self.current_state[i][decrement]=='O'):
					if(count == 0):
						count = count + 1
					elif(self.current_state[i][decrement] == previous):
						count = count + 1
					else:
						count = 0
					if(count == self.lineup_size):
						return 'O'
					previous = 'O'
				decrement = decrement - 1
			#if this forloop finishes then the second diagonal did not find a lineup_size win instance

		# George's algo below ( i don't think it works due to it starting at bottom right coner instead of top right)
		# pivot_d2 = '.'
		# for i in range(self.board_size-1, self.lineup_size-2, -1):
		# 	for j in range(self.board_size-1, self.lineup_size-2,-1):
		# 		pivot_d2 = self.current_state[i][j]
		# 		hasFailed = False
		# 		if (pivot_d2 != '.'):
		# 			for k in range(1, self.lineup_size+1):
		# 				if (pivot_d2 != self.current_state[i-k][j-k]):
		# 					hasFailed = True
		# 					break
		# 			if not hasFailed:return pivot_d2

		# Is whole board full?
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	# def check_end checks(self) checks if the game has finished, returns winner, tie message, or None if game is still on going
	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			#X is ◦ the white/hollow circle
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	#g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()

