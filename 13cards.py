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

possible_cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
say_answer = {True:'Correct', None:'Kinda', False:'Damn wrong'}

class Player:
	def __init__(self, name=None):
		self.cards = []
		self.guess_made = []
		if name:
			self.name = name
		else:
			self.name = random_name()

	def __str__(self):
		return self.name + ": " + str(self.cards)

	def get_card(self, card):
		self.cards.append(card)	

	def make_guess(self, revealed):
		cards_left = [c for c in possible_cards if c not in self.cards + revealed]
		random.shuffle(cards_left)
		guess = cards_left[0:3]
		# guess = random.choice([p for p in itertools.permutations(cards_left) if p not in self.guess_made])
		self.guess_made.append(guess)
		return guess

	def answer(self, guess):
		if set(guess) == set(self.cards):
			return True
		elif bool(set(guess) & set(self.cards)):
			return None
		else:
			return False

class Deck:
	def __init__(self):
		random.shuffle(possible_cards)	
		self.hidden = list(possible_cards)
		self.revealed = []

	def __str__(self):
		s = 'Hidden: ' + str(self.hidden) + '\n'
		s += 'Revealed: ' + str(self.revealed) + '\n'
		return s

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

class Game:
	def __init__(self, players):
		self.deck = Deck()
		self.players = players
		
	def __str__(self):
		return (
			'===========================================\n'
			'                Game Status                \n'
			'===========================================\n'
			+ str(self.deck)
			+ '\n'.join("%s" %str(p) for p in self.players) + '\n'
		)

	def new_player(self, player, name=None):
		self.append(Player(name=name))

	def initial_cards(self):
		for i in range(3):
			for p in self.players:
				p.get_card(self.deck.pop())

	def start(self):
		print "Game starts!!"
		print "Distributing cards ..."
		self.initial_cards()
		attacker, defender = self.players
		while True:
			print self
			# attacker makes guess
			guess = attacker.make_guess(self.deck.revealed)
			print attacker.name + ': ' + '"%s"'%', '.join(c for c in guess)

			# defender answers
			answer = defender.answer(guess)
			print defender.name + ': ' + '"%s"'%say_answer[answer]
			if answer:
				break

			# attacker updates

			# defender updates

			# reveal one card
			self.deck.reveal()

			# swap turn
			attacker, defender = defender, attacker

players = [Player(), Player()]		
game = Game(players)
game.start()