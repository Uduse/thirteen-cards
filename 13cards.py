import itertools
import random

names =	[ 
	"April",
	"Ben",
	"Caro",
	"Douglas",
	"Eva",
	"Firen",
	"George",
	"Henry",
	"Ian",
	"Jen",
	"Kate",
	"Lori",
	"Moss",
	"Nancy",
	"Opera",
	"Peggy",
	"Quasar",
	"Roy",
	"Sam",
	"Tonny",
	"Uduse",
	"Victor",
	"Wane",
	"Xvier",
	"Yvone",
	"Zack"
]

def random_name():
	random.shuffle(names)
	return names.pop() 

all_cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
say_answer = {True:'Correct', None:'Kinda', False:'Damn wrong'}

class Player(object):
	def __init__(self, name=None):
		self.hand =	set() 
		if name:
			self.name = name
		else:
			self.name = random_name()

	def __str__(self):
		return self.name + ": " + str(list(self.hand))

	def get_card(self, card):
		self.hand.add(card)	

	def make_guess(self, revealed):
		pass

	def answer_guess(self, guess):
		if guess == self.hand:
			return True
		elif bool(guess & self.hand):
			return None
		else:
			return False

	def got_guess(self, guess):
		pass

	def got_answer(self, guess, answer):
		pass

class StupidPlayer(Player):
	def __init__(self, name=None):
		super(StupidPlayer, self).__init__(name)
		self.guess_made = set() 
		self.neutral = [] 
		self.positive = []
		self.negative = []

	def make_guess(self, revealed):
		cards_left = [c for c in all_cards if c not in 
			list(self.hand) + revealed + self.negative]
		random.shuffle(cards_left)
		guess = frozenset(cards_left[0:3])
		self.guess_made.add(guess)
		return guess

	def got_guess(self, guess):
		self.negative.extend(guess)		

	def got_answer(self, guess, answer):
		if answer:
			return
		elif answer == False:
			self.negative.extend(guess)
		else:
			pass

class InteractivePlayer(Player):
	def __init__(self, name=None):
		super(InteractivePlayer, self).__init__(name)
		self.guess_made = set()

	def make_guess(self, revealed):
		print 'Your hand: ' + str(list(self.hand))
		guess = set()
		while len(guess) < 3:
			s = raw_input('Please enter your guess:')
			l = [c for c in s if c in all_cards or c == '1']
			if "1" in l:
				l[l.index('1')] = '10'
			guess = set(l[0:3])
		print
		return guess

class Deck:
	def __init__(self):
		random.shuffle(all_cards)	
		self.hidden = list(all_cards)
		self.revealed = []

	def __str__(self):
		return 'Revealed: ' + str(self.revealed)

	def pop(self):
		card = random.choice(self.hidden)
		self.hidden.remove(card)
		return card

	def reveal(self):
		card = random.choice(self.hidden)
		self.hidden.remove(card)
		self.revealed.append(card)

	def empty(self):
		return len(self.hidden) == 0

	def cards_left(self):
		return len(self.hidden)

class Game:
	def __init__(self):
		self.deck = Deck()
		self.players = []
		self.mode = None
		self.winner = None
		self.round = 0

	def __str__(self):
		return (
			'===========================================\n'
			'                Game Status                \n'
			'===========================================\n'
			+ str(self.deck)
			+ '\n'.join("%s" %str(p) for p in self.players) + '\n'
		)

	def new_player(self, player):
		self.players.append(player)

	def initial_cards(self):
		for i in range(3):
			for p in self.players:
				p.get_card(self.deck.pop())

	def welcome_dialog(self):
		print "Welcome!"
		while True:
			mode = raw_input(
				'Please enter game mode:\n'
				'1. Single Player\n'
				'2. Two Players\n'
				'3. Watch Sample Battle\n'
			)
			if mode == '1':
				name = raw_input('Your name is:').strip()
				self.new_player(InteractivePlayer(name))
				self.new_player(StupidPlayer())
				break
			elif mode == '2':
				self.new_player(InteractivePlayer())
				self.new_player(InteractivePlayer())
				break
			elif mode == '3':
				self.new_player(StupidPlayer())
				self.new_player(StupidPlayer())
				break
			else:
				print 'Please enter a valid mode'

		print "Game starts!!"
		print "Distributing cards ..."
		print

	def start(self):
		self.welcome_dialog()
		self.initial_cards()
		self.attacker, self.defender = self.players
		while not self.deck.empty():
			print 'Round ' + str(self.round) + '...\n'
			self.round += 1

			# Player 1 first attacks
			self.play(self.attacker, self.defender)
			
			# Stop if player 1 got it right
			if self.check_winner():
				break

			# swap turn
			self.attacker, self.defender = self.defender, self.attacker

			# Player 2 first attacks
			self.play(self.attacker, self.defender)
			
			# Stop if player 2 got it right
			if self.check_winner():
				break
		
			# reveal one card
			self.deck.reveal()
			print self.deck
			print

			# swap turn
			self.attacker, self.defender = self.defender, self.attacker

	def attacker_message(self, guess):
		print self.attacker.name + ': ' + '"%s"'%', '.join(c for c in guess)

	def defender_message(self, answer):
		print self.defender.name + ': ' + '"%s"'%say_answer[answer]

	def play(self, attacker, defender):
		# attacker makes guess
		guess = attacker.make_guess(self.deck.revealed)
		self.defender.got_guess(guess)

		self.attacker_message(guess)

		# defender answers
		answer = self.defender.answer_guess(guess)
		self.attacker.got_answer(guess, answer)

		self.defender_message(answer)

		# end game if someone wins		
		if answer:
			self.winner = self.attacker
		print

	def check_winner(self):
		if self.winner:
			return True
		else:
			return False

game = Game()
game.start()