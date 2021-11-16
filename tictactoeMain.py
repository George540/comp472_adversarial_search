# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
##########################################
## skeleton-titactoe.py (Mini-Assignment 2 COMP 472)
## This code contains the execution of the program's main and various methods to
## Implement an adversarial search algorithm for the game "Line 'em up"
## Created by Team Oranges
##########################################

import time
import random
from random import randrange
from typing import Counter
from collections import defaultdict

turn_start_time = 0
player_time_limit = 1000

total_evaluations_by_depth = {}
global_flag = False
evaluation_time = []
heuristic_evaluation = []
average_recusrion_depth = []
total_moves = []
eval_counter = 0
total_eval_counter_per_game = 0
total_evals_per_session = 0
total_moves_per_session = 0
total_wins_for_h1_PS = 0
total_wins_for_h2_PS = 0

def increment_Evaluation_Counter():
	global eval_counter
	eval_counter += 1

def reset_Evaluation_Counter():
	global eval_counter
	eval_counter = 0

def get_Evaluation_Counter():
	global eval_counter
	return eval_counter

def increment_Game_Eval_Counter(x):
	global total_eval_counter_per_game
	total_eval_counter_per_game += x

def get_Game_Eval_Counter():
	global total_eval_counter_per_game
	return total_eval_counter_per_game

def reset_Game_Eval_Counter():
	global total_eval_counter_per_game
	total_eval_counter_per_game = 0

def increment_Total_Eval_Counter_PS(x):
	global total_evals_per_session
	total_evals_per_session += x

def get_Total_Eval_Counter_PS():
	global total_evals_per_session
	return total_evals_per_session

def reset_Total_Eval_Counter_PS():
	global total_evals_per_session
	total_evals_per_session = 0

def increment_Moves_PS(x):
	global total_moves_per_session
	total_moves_per_session+= x

def get_Total_Moves_PS():
	global total_moves_per_session
	return total_moves_per_session

def reset_Moves_PS():
	global total_moves_per_session
	total_moves_per_session = 0

def increment_Win_For_H1():
	global total_wins_for_h1_PS
	total_wins_for_h1_PS+= 1

def get_Win_For_H1():
	global total_wins_for_h1_PS
	return total_wins_for_h1_PS

def increment_Win_For_H2():
	global total_wins_for_h2_PS
	total_wins_for_h2_PS+= 1

def get_Win_For_H2():
	global total_wins_for_h2_PS
	return total_wins_for_h2_PS

def set_Turn_Start_Time():
	global turn_start_time
	turn_start_time = time.time()

def get_turn_start_time():
	global turn_start_time
	turn_start_time
	return turn_start_time

def set_player_time_limit(limit):
	global player_time_limit
	player_time_limit = limit

def get_player_time_limit():
	global player_time_limit
	return player_time_limit


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
	BLOCK = 'B'
	
	def __init__(self, board_size=3, number_of_blocks=2, block_coordinates = [], 
				lineup_size=3, d1=3, d2=3, time_threshold=5, a=True, p1=AI, p2=AI, h1=True, h2=True, recommend=True):
		'''
		Constructor of game object takes the board parameters and ensures that they are within value requirements and creates the game object

		board_size (int): represents the NxN board size min 3 and max 10
		number_of_blocks (int): number of blocks that will be placed on the board
		block_coordinates (list): 2d coordinates of block placement, if empty, blocks are randomly assigned
		lineup_size (int): The number of the same consecutive X's or O's needed to win the game
		d1, d2 (int): The depth of the tree traversarl for each player
		time_threshold (int): The amount of time in seconds that the algorithm has to come up with a resonable decision for a node
		p1, p2 (int): The numbers associated with choosing an AI or HUMAN as player 1 or 2
		H1, H2 (bool): Setting it to True will use heuristic 1, heuristic 2 otherwise for both players, respectively
		recommend (bool): Setting this to true will have the AI display the best tile to place a piece X or O, nothing otherwise 
		'''
		temp_string = 'gameTrace-'+str(board_size)+str(number_of_blocks)+str(lineup_size)+str(time_threshold)+'.txt'
		print(temp_string)
		gameTraceFile = open(temp_string, "w")
		self.gameTraceFile = gameTraceFile
		gameTraceFile.write('n='+str(board_size)+' b='+str(number_of_blocks)+' s='+str(lineup_size)+' t='+str(time_threshold)+'\n')
		gameTraceFile.write('blocs=('+str(block_coordinates)+')\n\n')
		if h1:
			gameTraceFile.write('Player 1: '+ str(p1) +' d='+str(d1)+' a='+str(h1)+' e1 (Consecutivity)\n')
		else:
			gameTraceFile.write('Player 1: '+ str(p1) +' d='+str(d1)+' a='+str(h1)+' e2 (Closest Winning Condition)\n')
		if h2:
			gameTraceFile.write('Player 2: '+ str(p2) +' d='+str(d2)+' a='+str(h2)+' e1 (Consecutivity)\n')
		else:
			gameTraceFile.write('Player 2: '+ str(p2) +' d='+str(d2)+' a='+str(h2)+' e2 (Closest Winning Condition)\n')
		gameTraceFile.write('\n')

		self.evaluations_by_depth = {}
		self.turncount = 0
		self.board_size = board_size
		self.number_of_blocks = number_of_blocks
		self.block_coordinates = block_coordinates
		self.lineup_size = lineup_size
		self.d1 = d1
		self.d2 = d2
		self.time_threshold = time_threshold
		self.recommend = recommend
		self.a = a
		self.p1 = p1
		self.p2 = p2
		self.h1 = h1
		self.h2 = h2
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
		'''
			Initializes the game board with or without Blocks B.
		'''
		self.current_state = [['.' for i in range(self.board_size)] for j in range(self.board_size)]
		if (self.block_coordinates == []):
			for i in range(self.number_of_blocks):
				self.current_state[random.randint(0,self.board_size-1)][random.randint(0,self.board_size-1)] = self.BLOCK
		else:
			for i in range(self.number_of_blocks):
				for coord in self.block_coordinates:
					self.current_state[coord[0]][coord[1]] = self.BLOCK
		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		'''
			Draws the nxn board with the current contents 
		'''
		print()
		self.gameTraceFile.write('\n')
		for i in range(self.board_size):
			self.gameTraceFile.write('   '+str(i))
		if self.turncount > 0:
			self.gameTraceFile.write('\t(MOVE #'+str(self.turncount)+')')
		self.turncount +=1
		self.gameTraceFile.write('\n  +')
		for i in range(self.board_size):
			self.gameTraceFile.write('----')
		self.gameTraceFile.write('\n')
		for y in range(0, self.board_size):
			self.gameTraceFile.write(str(y)+'|')
			for x in range(0, self.board_size):
				print(F'{self.current_state[x][y]}', end="")
				self.gameTraceFile.write('  '+str(self.current_state[x][y]))
			print()
			self.gameTraceFile.write('\n')
		print()
		self.gameTraceFile.write('\n')
		
	def is_valid(self, px, py):
		'''
		Checks if player move is inside game bounds or on an empty slot

		px (int): The integer value for the x coordinate
		py (int): The integer value for the y coordinate

		Returns true/false if the coordinates inputted are correct or not
		'''
		if px < 0 or px > self.board_size-1 or py < 0 or py > self.board_size-1:
			return False
		elif self.current_state[px][py] != '.' and self.current_state[px][py] != self.BLOCK:
			return False
		else:
			return True

	def is_end(self):
		'''
		Verifies if win condition vertical/horizontal/diagonal lineup_size is met

		returns a winner, if there is one or a tie, if that is the case. None if the game is still going
		'''
		# Vertical win
		pivot_v = '.'
		#print("Vertical check:")
		for j in range(0, self.board_size): #iterate through columns first
			for i in range(0, self.board_size-self.lineup_size+1): #iterate through rows after (the arrays themselves)
				pivot_v = self.current_state[i][j]
				#print("[", i, "][", j,"] = ", pivot_v)
				hasFailed = False
				if (pivot_v != '.' and pivot_v != self.BLOCK):
					for k in range(1, self.lineup_size): #iterate through winning lineup size
						#print("k:", k)
						#print("[", i, "][", (j+k),"]")
						if (pivot_v != self.current_state[i+k][j]):
							hasFailed = True
							break
					if not hasFailed:return pivot_v #if the third loop iterates entirely, it means a lineup was found. Return the pivot
		# Horizontal win
		#Create what the winning line ups will look like horizontally in the form of a string
		#review: think it's supposed to be line_up size? not board size?
		#print("Horizontal check:")
		horizontal_winX = 'X' * self.lineup_size
		horizontal_winO = 'O' * self.lineup_size
		for i in range(0, self.board_size):
			current_row = ''.join(self.current_state[i]) # turn array into string: for example, ['X', 'O', 'X'] -> 'XOX'
			# print(self.current_state[i])
			# print(current_row)
			if (horizontal_winX in current_row):return 'X'
			elif (horizontal_winO in current_row):return 'O'

		# Main diagonal win. Ie diagonals that start from top left and work their way to bottom right, including main diagonal
		#print("Main diag check:")
		pivot_d1 = '.'
		#iterate through rows first
		for i in range(0, self.board_size-self.lineup_size+1): # must consider a limit for the diagonal size
			for j in range(0, self.board_size-self.lineup_size+1):
				# print("i:", i, ",j:", j)
				# print("value:",self.current_state[i][j])
				pivot_d1 = self.current_state[i][j]
				hasFailed = False
				if (pivot_d1 != '.' and pivot_d1 != self.BLOCK):
					for k in range(1, self.lineup_size):
						# print(k)
						# print("[",i+k,"],[",j+k,"]")
						if (pivot_d1 != self.current_state[i+k][j+k]): #iterate diagonally
							hasFailed = True
							break
					if not hasFailed:return pivot_d1

		# Second diagonal win
		pivot_d2 = '.'
		for i in range(0, self.board_size-self.lineup_size):
			for j in range(self.board_size-1, self.lineup_size-2, -1):
				pivot_d2 = self.current_state[i][j]
				hasFailed = False
				if (pivot_d2 != '.' and pivot_d2 != self.BLOCK):
					for k in range(1, self.lineup_size+1):
						if (pivot_d2 != self.current_state[i+k][j-k]):
							hasFailed = True
							break
					if not hasFailed:return pivot_d2

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
		'''
			An extension to the method above. This prints out the information of the winner of a match or stalemate. As well as metrics.

			self: game object with all attributes

			returns the result
		'''
		global evaluation_time
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
				if(self.h1==True):
					increment_Win_For_H1()
				else:
					increment_Win_For_H2()
			elif self.result == 'O':
				print('The winner is O!')
				if(self.h2==True):
					increment_Win_For_H1()
				else:
					increment_Win_For_H2()
			elif self.result == '.':
				print("It's a tie!")

			#6b
			print('\n6(b)i\t Average Evaluation Time: '+str(round(sum(evaluation_time)/len(evaluation_time), 2))+'s\n')
			self.gameTraceFile.write('6(b)i\t Average Evaluation Time: '+str(round(sum(evaluation_time)/len(evaluation_time), 2))+'s\n')
			print('6(b)ii\t Total heuristic evaluations: '+ str(get_Game_Eval_Counter()) +'\n')
			self.gameTraceFile.write('6(b)ii\t Total heuristic evaluations: '+ str(get_Game_Eval_Counter()) +'\n')
			print('6(b)iii\t Evaluations by depth: '+str(self.evaluations_by_depth)+'\n')
			self.gameTraceFile.write('6(b)iii\t Evaluations by depth: '+str(self.evaluations_by_depth)+'\n')
			temp_list = [key * val for key, val in self.evaluations_by_depth.items()]
			temp_list = (sum(temp_list)/(sum(self.evaluations_by_depth.values())))
			print('6(b)iv\t Average Evaluation depth: '+str(round(temp_list, 2))+'\n')
			self.gameTraceFile.write('6(b)iv\t Average Evaluation depth: '+'\n')
			print('6(b)v\t Average recursion depth: '+'\n')
			self.gameTraceFile.write('6(b)v\t Average recursion depth: '+'\n')
			print('6(b)vi\t Total moves: '+str(self.turncount-1)+'\n')
			self.gameTraceFile.write('6(b)vi\t Total moves: '+str(self.turncount-1)+'\n')
			increment_Moves_PS(self.turncount - 1)
			self.turncount = 0
			increment_Total_Eval_Counter_PS(get_Game_Eval_Counter())
			reset_Game_Eval_Counter()
			self.initialize_game()
		return self.result

	def input_move(self):
		'''
			Receives player/AI input

			self: game object with all attributes
		'''
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		'''
			Switches player turns
		'''
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def heuristic_one(self, max= False):
		'''
		Calculates consecutivity
		|i	|i+1	|h(n)
		---------------------
		|X	|X		|+2
			|.		|+1
			|B		|+0
			|O		|-1
		self: game object with all attributes
		Max = False, means X is playing
		Max = True, means O is playing

		returns a heuristic value evaluated at *this* node
		'''
		increment_Evaluation_Counter()
		maximize_for = ''
		minimize_for = ''
		#sets the player X or O we want to maximize for
		if max:
			maximize_for = 'X'
			minimize_for = 'O'
		else:
			maximize_for = 'O'
			minimize_for = 'X'
		temp_heuristic_value = 0
		total_heuristic_value = 0

		#Row
		row_is_still_playable = False
		for i in range (0, self.board_size):
			temp_heuristic_value = 0
			row_is_still_playable = False
			for j in range(0, self.board_size):
				# Makes sure there is still an empty spot to play in the row
				if self.current_state[i][j] == '.':
					row_is_still_playable = True
				if self.current_state[i][j] == maximize_for:
					temp_heuristic_value += 1
				# Skips the last index, because it has no neighbour (prevents index out of bounds)
				if j != self.board_size-1:
					if self.current_state[i][j] == maximize_for and self.current_state[i][j+1] == maximize_for:
						temp_heuristic_value += 2
					elif self.current_state[i][j] == maximize_for and self.current_state[i][j+1] == '.':
						temp_heuristic_value += 1
					elif self.current_state[i][j] == maximize_for and self.current_state[i][j+1] == 'B':
						temp_heuristic_value += 0
					elif self.current_state[i][j] == maximize_for and self.current_state[i][j+1] == minimize_for:
						temp_heuristic_value -= 1
			if row_is_still_playable == True:
				total_heuristic_value += temp_heuristic_value

		#Column
		for i in range (0, self.board_size):
			temp_heuristic_value = 0
			col_is_still_playable = False
			for j in range(0, self.board_size):
				# Makes sure there is still an empty spot to play in the row
				if self.current_state[i][j] == '.':
					col_is_still_playable = True
				if self.current_state[i][j] == maximize_for:
					temp_heuristic_value += 1
				# Skips the last index, because it has no neighbour (prevents index out of bounds)
				if i != self.board_size-1:
					if self.current_state[i][j] == maximize_for and self.current_state[i+1][j] == maximize_for:
						temp_heuristic_value += 2
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j] == '.':
						temp_heuristic_value += 1
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j] == 'B':
						temp_heuristic_value += 0
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j] == minimize_for:
						temp_heuristic_value -= 1
			if col_is_still_playable == True:
				total_heuristic_value += temp_heuristic_value

		#Left to right Diagonal --->
		for i in range (0, self.board_size):
			temp_heuristic_value = 0
			col_is_still_playable = False
			for j in range(0, self.board_size):
				# Makes sure there is still an empty spot to play in the row
				if self.current_state[i][j] == '.':
					col_is_still_playable = True
				if self.current_state[i][j] == maximize_for:
					temp_heuristic_value += 1
				# Skips diagonals that are too small to win with (i.e a diagonal of size 2, in a game where you need 3 in a row to win)
				if j <= self.board_size - self.lineup_size and i <= self.board_size - self.lineup_size:
					if self.current_state[i][j] == maximize_for and self.current_state[i+1][j+1] == maximize_for:
						temp_heuristic_value += 2
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j+1] == '.':
						temp_heuristic_value += 1
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j+1] == 'B':
						temp_heuristic_value += 0
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j+1] == minimize_for:
						temp_heuristic_value -= 1
			if col_is_still_playable == True:
				total_heuristic_value += temp_heuristic_value

		#Right to left Diagonal --->
		for i in range (0, self.board_size):
			temp_heuristic_value = 0
			col_is_still_playable = False
			for j in range((self.board_size - 1), -1, -1):
				# Makes sure there is still an empty spot to play in the row
				if self.current_state[i][j] == '.':
					col_is_still_playable = True
				if self.current_state[i][j] == maximize_for:
					temp_heuristic_value += 1
				# Skips diagonals that are too small to win with (i.e a diagonal of size 2, in a game where you need 3 in a row to win)
				if i < (self.lineup_size -1) and j >= self.lineup_size-1:
					if self.current_state[i][j] == maximize_for and self.current_state[i+1][j-1] == maximize_for:
						temp_heuristic_value += 2
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j-1] == '.':
						temp_heuristic_value += 1
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j-1] == 'B':
						temp_heuristic_value += 0
					elif self.current_state[i][j] == maximize_for and self.current_state[i+1][j-1] == minimize_for:
						temp_heuristic_value -= 1
				else:
					break
			if col_is_still_playable == True:
				total_heuristic_value += temp_heuristic_value

		if maximize_for == 'X':
			total_heuristic_value= (-1 * total_heuristic_value)
		return total_heuristic_value
				
	def heuristic_two(self, max=False):
		'''
		self: game object with all attributes
		Calculates the amount of blocks left to complete the closest winning condition
		Max (bool): The boolean value needed to determine if max is seeking to maximize his heuristic. Min otherwise 

		returns a heuristic value evaluated at *this* node
		'''
		increment_Evaluation_Counter()
		maximize_for = ''
		#sets the player X or O we want to maximize for
		if max:
			maximize_for = 'X'
			minimize_for = 'O'
		else:
			maximize_for = 'O'
			minimize_for = 'X'

		heuristic_value = 0
	
		# Vertical
		vertical_lineup_streak_number = 0
		for j in range(0, self.board_size):
			for i in range(0, self.board_size-self.lineup_size+1):
				pivot_v = self.current_state[i][j]
				temp_streak = 0
				if (pivot_v != self.BLOCK):
					for k in range(0, self.lineup_size):
						if (self.current_state[i+k][j] == self.BLOCK or self.current_state[i+k][j] == minimize_for):
							break
						elif (self.current_state[i+k][j] == maximize_for):
							temp_streak += 1
				if not max:
					temp_streak *= -1
				if (abs(temp_streak) > abs(vertical_lineup_streak_number)):
					vertical_lineup_streak_number = temp_streak

		heuristic_value = vertical_lineup_streak_number

		#Horizontal
		horizontal_lineup_streak_number = 0
		for i in range(0, self.board_size):
			for j in range(0, self.board_size-self.lineup_size+1):
				pivot_h = self.current_state[i][j]
				temp_streak = 0
				if (pivot_h != self.BLOCK):
					for k in range(0, self.lineup_size):
						if (self.current_state[i][j+k] == self.BLOCK or self.current_state[i][j+k] == minimize_for):
							break
						elif (self.current_state[i][j+k] == maximize_for):
							temp_streak += 1
				if not max:
					temp_streak *= -1
				if (abs(temp_streak) > abs(horizontal_lineup_streak_number)):
					horizontal_lineup_streak_number = temp_streak

		# check so far which of the two line-up types is closer to complete
		if (abs(horizontal_lineup_streak_number) > abs(vertical_lineup_streak_number)):
			heuristic_value = horizontal_lineup_streak_number

		# Top Left -> Bottom Right Diagonals
		main_diagonals_lineup_streak_number = 0
		for i in range(0, self.board_size-self.lineup_size+1):
			for j in range(0, self.board_size-self.lineup_size+1):
				pivot_d1 = self.current_state[i][j]
				temp_streak = 0
				if (pivot_d1 != self.BLOCK):
					for k in range(0, self.lineup_size):
						if (self.current_state[i+k][j+k] == self.BLOCK or self.current_state[i+k][j+k] == minimize_for):
							break
						elif (self.current_state[i+k][j+k] == maximize_for):
							temp_streak += 1
				if not max:
					temp_streak *= -1
				if (abs(temp_streak) > abs(main_diagonals_lineup_streak_number)):
					main_diagonals_lineup_streak_number = temp_streak
			
		if (abs(main_diagonals_lineup_streak_number) > abs(heuristic_value)):
				heuristic_value = main_diagonals_lineup_streak_number

		# Top Right -> Bottom Left Diagonals
		second_diagonals_lineup_streak_number = 0
		for i in range(0, self.board_size-self.lineup_size):
			for j in range(self.board_size-1, self.lineup_size-2, -1):
				pivot_d2 = self.current_state[i][j]
				temp_streak = 0
				if (pivot_d2 != self.BLOCK):
					for k in range (0, self.lineup_size):
						if (self.current_state[i+k][j-k] == self.BLOCK or self.current_state[i+k][j-k] == minimize_for):
							break
						elif (self.current_state[i+k][j-k] == maximize_for):
							temp_streak += 1
				if not max:
					temp_streak *= -1
				if (abs(temp_streak) > abs(second_diagonals_lineup_streak_number)):
					second_diagonals_lineup_streak_number = temp_streak
			
		if (abs(second_diagonals_lineup_streak_number) > abs(heuristic_value)):
			heuristic_value = second_diagonals_lineup_streak_number
		return heuristic_value

	def minimax(self, max, depth, h1):
		'''
		Minimax algorithm implementation

		self: game object with all attributes
		max (bool): Chosing which player to minimize/maximize for
		h1 (bool): True is heuristic one, False is Heuristic 2

		returns heuristic value acquired, and the x & y coordinate of it
		'''
		global global_flag
		value = 1000
		if max:
			value = -1000
		x = None
		y = None
		if round(time.time() - get_turn_start_time(), 7) > get_player_time_limit()-0.01:
			if h1:
				return (self.heuristic_one(max), x, y)
			else:
				return (self.heuristic_two(max), x, y)
		if (depth <= 0):
			if h1:
				return (self.heuristic_one(max), x, y)
			else:
				return (self.heuristic_two(max), x, y)

		hasCombinations = False
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if self.current_state[i][j] == '.':
					hasCombinations = True
					if depth in self.evaluations_by_depth:
						self.evaluations_by_depth[depth] += get_Evaluation_Counter()
					else:
						self.evaluations_by_depth[depth] = get_Evaluation_Counter()
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False, depth=depth-1, h1=h1)
						if v >= value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True, depth=depth-1, h1=h1)
						if v <= value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		if (hasCombinations == False):
			if h1:
				return (self.heuristic_one(max), x, y)
			else:
				return (self.heuristic_two(max), x, y)
		return(value, x, y)

	def alphabeta(self, alpha=-100, beta=100, max=False, depth=3, h1=True):
		'''
		Alphabeta algorithm implementation

		self: game object with all attributes
		alpha (float): Float used for comparison
		beta (float): Float used for comparison
		max (bool): Chosing which player to minimize/maximize for
		depth (int): Traversal depth
		h1 (bool): True is heuristic one, False is Heuristic 2

		returns heuristic value acquired, and the x & y coordinate of it
		'''
		# We're initially setting it to 1000 or -1000 as worse than the worst case:
		if round(time.time() - get_turn_start_time(), 7) > get_player_time_limit():
			print('Time Limit Reached!')
			if max:
				print('O LOSES')
				quit()
			else:
				print('X LOSES')
				quit()
		value = 1000
		if max:
			value = -1000
		x = None
		y = None
		
		if (depth <= 0):
			if h1:
				return (self.heuristic_one(max), x, y)
			else:
				return (self.heuristic_two(max), x, y)
		
		hasCombinations = False
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if self.current_state[i][j] == '.':
					hasCombinations = True
					if depth in self.evaluations_by_depth:
						self.evaluations_by_depth[depth] += get_Evaluation_Counter()
					else:
						self.evaluations_by_depth[depth] = get_Evaluation_Counter()
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False, depth=depth-1, h1=h1)
						if v >= value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True, depth=depth-1, h1=h1)
						if v <= value:
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

		if (hasCombinations == False):
			if h1:
				return (self.heuristic_one(max), x, y)
			else:
				return (self.heuristic_two(max), x, y)
				
		return (value, x, y)

	def play(self, algo=None, player_x=None, player_o=None, d1=5, d2=5, h1=True, h2=True):
		'''
		Plays the game!

		self: game object with all attributes
		algo: Game.MINIMAX for minmax or Game.ALPHABETA
		player_x: Game.AI for AI or Game.HUMAN
		player_y: Game.AI for AI or Game.HUMAN
		player_x_heuristic: True uses H1, False uses H2
		player_o_heuristic: True uses H1, False uses H2
		depth: the depth that minmax or alphabeta will traverse
		'''
		global evaluation_time
		global heuristic_evaluation
		global global_flag
		global total_evaluations_by_depth
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			print()
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			set_Turn_Start_Time()
			#X is ◦ the white/hollow circle
			global_flag = False
			evaluations_by_depth =0
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False, depth=d1, h1=h1)
				else:
					(_, x, y) = self.minimax(max=True, depth=d2, h1=h2)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False, depth=d1, h1=h1)
				else:
					(m, x, y) = self.alphabeta(max=True, depth=d2, h1=h2)
			end = time.time()
			if self.player_turn != self.BLOCK and ((self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN)):
					if self.recommend:
						self.gameTraceFile.write('\n')
						self.gameTraceFile.write('Player '+str(self.player_turn)+' under Human Control plays: x='+str(x)+', y='+str(y)+'\n')
						print(F'Player {self.player_turn} under Human Control plays: x = {x}, y = {y}')
						self.gameTraceFile.write('\n')
						#print(F'i\tEvaluation time: {round(end - start, 7)}s')
						#evaluation_time.append(round(end - start, 7))
						#print('ii\tHeuristic Evaluations:', get_Evaluation_Counter())
						#heuristic_evaluation.append(m)
						#self.gameTraceFile.write('ii\tHeuristic evaluations: '+str(get_Evaluation_Counter())+'\n')
						#print(F'iii\tEvaluations by depth: ') #NOT FINISHED
						#print(F'iv\tAverage evalution depth ' + str(global_counter)) #Not FINISHED
						#print(F'iv\tAverage Recursion depth ') #NOT FINISHED
						#print(F'Recommended move: x = {x}, y = {y}')

					(x,y) = self.input_move()
			if self.player_turn != self.BLOCK and ((self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI)):
						self.gameTraceFile.write('\n')
						self.gameTraceFile.write('Player '+str(self.player_turn)+' under AI Control plays: x='+str(x)+', y='+str(y)+'\n')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
						self.gameTraceFile.write('\n')

			#TURN OUTPUT RESULTS ARE HERE
			print(F'i\tEvaluation time: {round(end - start, 7)}s')
			self.gameTraceFile.write('i\tEvaluation time: '+str(round(end - start, 7))+'\n')
			evaluation_time.append(round(end - start, 7))

			print(F'ii\tHeuristic Evaluations: {get_Evaluation_Counter()}')
			self.gameTraceFile.write('ii\tHeuristic evaluations: '+str(get_Evaluation_Counter())+'\n')

			print(F'iii\tEvaluations by depth: '+ str(self.evaluations_by_depth)) #NOT FINISHED
			total_evaluations_by_depth.update(self.evaluations_by_depth)

			temp_list = [key * val for key, val in self.evaluations_by_depth.items()]
			temp_list = (sum(temp_list)/(sum(self.evaluations_by_depth.values())))
			print(F'iv\tAverage evaluation depth '+str(round(temp_list, 2))) #Not FINISHED
			print(F'iv\tAverage Recursion depth ') #NOT FINISHED
			print(F'Recommended move: x = {x}, y = {y}')

			self.current_state[x][y] = self.player_turn
			increment_Game_Eval_Counter(get_Evaluation_Counter())
			reset_Evaluation_Counter()
			self.switch_player()

def main():
	inputs = menu()
	g = Game(recommend=True)
	if (inputs != []):
		loop_code = int(input('How many times would you like to run the game?\n'))
		g = Game(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7], inputs[8], inputs[9], inputs[10], inputs[11], recommend=True)
		set_player_time_limit(inputs[6])
		for i in range(loop_code):
			g.play(algo=g.a, player_x=g.p1, player_o=g.p2, d1=g.d1, d2=g.d2, h1=g.h1, h2=g.h2)

		#SCOREBOARD FILE WRITING HAPPENS HERE!!!!
		scoreboardFile = open("Scoreboard.txt", "w")
		scoreboardFile.write('n='+ str(3) +' b='+str(2)+' s='+str(3)+' t='+str(5)+'\n\n')
		scoreboardFile.write('Player 1: d='+str(3)+' a='+str(True)+'\n')
		scoreboardFile.write('Player 2: d='+str(3)+' a='+str(True)+'\n\n')
		scoreboardFile.write(str(loop_code)+' games'+'\n\n')
		scoreboardFile.write('Total wins for heuristic e1: '+ str(get_Win_For_H1()) +' ('+str(round(100 * (get_Win_For_H1() / loop_code), 2)) +'%) (Consecutivity)\n')
		scoreboardFile.write('Total wins for heuristic e2: '+ str(get_Win_For_H2()) +' ('+str(round(100 * (get_Win_For_H2() / loop_code), 2)) +'%) (Closest Winning Condition)\n\n')
		scoreboardFile.write('i\tAverage evaluation time: '+ str(round(sum(evaluation_time)/len(evaluation_time), 2)) +'s\n')
		scoreboardFile.write('ii\tTotal heuristic evaluations: '+ str(get_Total_Eval_Counter_PS()) +'\n')
		scoreboardFile.write('iii\tEvaluations by depth: '+ str(total_evaluations_by_depth) +'\n')
		temp_list = [key * val for key, val in total_evaluations_by_depth.items()]
		temp_list = (sum(temp_list)/(sum(total_evaluations_by_depth.values())))
		scoreboardFile.write('iv\tAverage evaluation depth: '+ str(round(temp_list, 2)) +'\n')
		scoreboardFile.write('v\tAverage recursion depth: '+ 'x' +'\n')
		scoreboardFile.write('vi\tAverage moves per game: '+ str(round(get_Total_Moves_PS() / loop_code, 2)) +'\n')
		reset_Total_Eval_Counter_PS()
		reset_Moves_PS()

	else:
		loop_code = int(input('How many times would you like to run the game?\n'))
		for i in range(loop_code):
			g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI)
		#SCOREBOARD FILE WRITING HAPPENS HERE!!!!
		scoreboardFile = open("Scoreboard.txt", "w")
		scoreboardFile.write('n='+ str(3) +' b='+str(2)+' s='+str(3)+' t='+str(5)+'\n\n')
		scoreboardFile.write('Player 1: d='+str(3)+' a='+str(True)+'\n')
		scoreboardFile.write('Player 2: d='+str(3)+' a='+str(True)+'\n\n')
		scoreboardFile.write(str(loop_code)+' games'+'\n\n')
		scoreboardFile.write('Total wins for heuristic e1: '+ str(get_Win_For_H1()) +' ('+str(round(100 * (get_Win_For_H1() / loop_code), 2)) +'%) (Consecutivity)\n')
		scoreboardFile.write('Total wins for heuristic e2: '+ str(get_Win_For_H2()) +' ('+str(round(100 * (get_Win_For_H2() / loop_code), 2)) +'%) (Closest Winning Condition)\n\n')
		scoreboardFile.write('i\tAverage evaluation time: '+ str(round(sum(evaluation_time)/len(evaluation_time), 2)) +'s\n')
		scoreboardFile.write('ii\tTotal heuristic evaluations: '+ str(get_Total_Eval_Counter_PS()) +'\n')
		scoreboardFile.write('iii\tEvaluations by depth: '+ str(total_evaluations_by_depth) +'\n')
		temp_list = [key * val for key, val in total_evaluations_by_depth.items()]
		temp_list = (sum(temp_list)/(sum(total_evaluations_by_depth.values())))
		scoreboardFile.write('iv\tAverage evaluation depth: '+ str(round(temp_list, 2)) +'\n')
		scoreboardFile.write('v\tAverage recursion depth: '+ 'x' +'\n')
		scoreboardFile.write('vi\tAverage moves per game: '+ str(round(get_Total_Moves_PS() / loop_code, 2)) +'\n')
		reset_Total_Eval_Counter_PS()
		reset_Moves_PS()

def menu():
	'''
		UI for user

		returns inputs in array format
	'''
	print('\n---------- Welcome to Team Oranges Mini-Assignment 2 for COMP 472 ----------\n')

	print('Would you like to use default values?')
	print('Defaults: AI vs Human, 3x3 grid, Traversal Depth = 3, Traversal Algorith = ALPHABETA, time threshold - 5s')
	defaults = str(input('\nPlease select one of the following options: (y/n)'))
	if (defaults == 'y'):
		print('Defaults chosen. Program proceeding...\n')
		return []
	elif (defaults == 'n'):
		print('User will enter custom parameters. Program proceeding...\n')

	grid_size = int(input('\nEnter grid size (NxN), between 3 and 10: '))

	choice = str(input('\nRandomized blocks or enter them manually? (y/n)'))
	if (choice == 'y'):
		print('Randomized blocks selected\n')
	elif (choice == 'n'):
		print('Manually entering blocks\n')

	number_of_blocks = int(input('\nEnter number of blocks, between 0 and 2n: '))
	
	block_coordinates = [None] * number_of_blocks
	if (choice == 'n'):
		for i in range(0, number_of_blocks):
			x_cord = int(input('\nEnter X coordinate of block ' + str(i+1) + ' (Must be valid): '))
			y_cord = int(input('\nEnter Y coordinate of block ' + str(i+1) + ' (Must be valid): '))
			block_coordinates[i] = (x_cord, y_cord)
	else:
		block_coordinates = []

	lineup_size = int(input('\nEnter the line-up size, between 3 and n: '))

	d1 = int(input('\nEnter adversarial search depth d1: '))
	d2 = int(input('\nEnter adversarial search depth d2: '))
	t = float(input('\nEnter maximum allowed time (in seconds) for AI to return a move (must be above 0): '))

	minimax = True
	choice = str(input('\nMINIMAX or ALPHABETA P1? (m/a)'))
	if (choice == 'm'):
		print('MINIMAX selected\n')
		a = Game.MINIMAX
	elif (choice == 'a'):
		print('ALPHABETA selected\n')
		a = Game.ALPHABETA

	choice = str(input('\nMINIMAX or ALPHABETA P2? (m/a)'))
	if (choice == 'm'):
		print('MINIMAX selected\n')
		a = Game.MINIMAX
	elif (choice == 'a'):
		print('ALPHABETA selected\n')
		a = Game.ALPHABETA

	choice = str(input('\nIs p1 AI or HUMAN? (a/h):'))
	player1 = Game.AI
	if (choice == 'a'):
		print('P1 is AI\n')
		player1 = Game.AI
	elif (choice == 'h'):
		print('P1 is human\n')
		player1 = Game.HUMAN
	
	choice = str(input('\nIs p2 AI or HUMAN? (a/h):'))
	player2 = Game.AI
	if (choice == 'a'):
		print('P2 is AI\n')
		player2 = Game.AI
	elif (choice == 'h'):
		print('P2 is human\n')
		player2 = Game.HUMAN

	choice = str(input('\nPlayer 1 will use Heuristic 1 or Heuristic 2? (1/2):'))
	h1 = True
	if (choice == '1'):
		print('H1 chosen\n')
		h1 = True
	elif (choice == '2'):
		print('H2 chosen\n')
		h1 = False

	choice = str(input('\nPlayer 2 will use Heuristic 1 or Heuristic 2? (1/2):'))
	h2 = True
	if (choice == '1'):
		print('H1 chosen\n')
		h2 = True
	elif (choice == '2'):
		print('H2 chosen\n')
		h2 = False

	return (grid_size, number_of_blocks, block_coordinates, lineup_size, d1, d2, t, a, player1, player2, h1, h2)

if __name__ == "__main__":
	main()