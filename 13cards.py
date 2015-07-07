# TODO: Select difficulty
# TODO: Repetitive games
# TODO: OkayPlayer
# TODO: Save/Load game
# TODO: Guess size must be three
import itertools
import random

names = [
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
    "Tony",
    "Uduse",
    "Victor",
    "Wane",
    "Xavier",
    "Yvonne",
    "Zack"
]


def random_name():
    random.shuffle(names)
    return names.pop()


def sort_card(card):
    if card == 'A':
        return 1
    elif card == 'J':
        return 11
    elif card == 'Q':
        return 12
    elif card == 'K':
        return 13
    else:
        return int(card)


def sorted_cards(cards):
    return sorted(list(cards), key=sort_card)


all_cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
say_answer = {True: 'Correct', None: 'Kinda', False: 'Damn wrong'}


class Player(object):
    def __init__(self, name=None):
        self.hand = set()
        self.last_guess = None
        if name:
            self.name = name
        else:
            self.name = random_name()

    def __str__(self):
        return self.name + ": " + str(sorted_cards(self.hand))

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

    def got_answer(self, answer):
        pass


class StupidPlayer(Player):
    def __init__(self, name=None):
        super(StupidPlayer, self).__init__(name)
        self.guess_made = set()
        self.negative = []

    def make_guess(self, revealed):
        cards_left = [c for c in all_cards if c not in
                      list(self.hand) + revealed + self.negative]
        random.shuffle(cards_left)
        guess = frozenset(cards_left[0:3])
        self.guess_made.add(guess)
        self.last_guess = guess
        return guess

    def got_guess(self, guess):
        self.negative.extend(guess)

    def got_answer(self, answer):
        if answer:
            return
        elif answer == False:
            self.negative.extend(self.last_guess)
        else:
            pass


class OkayPlayer(Player):
    def __init__(self, name=None):
        super(OkayPlayer, self).__init__(name=name)
        self.guess_made = set()
        self.guess_got = set()
        self.cards_info = dict((c, None) for c in all_cards)
        self.positive_pairs = list()
        self.positive_triads = list()
        self.last_guess_mode = None
        self.last_one = None
        self.last_pair = None
        self.last_triad = None

    def get_card(self, card):
        super(OkayPlayer, self).get_card(card)
        self.cards_info[card] = False

    def snipe_one(self):
        self.last_guess_mode = 1
        negative = [c for c in self.cards_info if self.cards_info[c] == False]
        not_sure = random.choice([c for c in self.cards_info if self.cards_info[c] is None])
        random.shuffle(negative)
        negative_pair = negative[0:2]
        guess = negative_pair + [not_sure]
        self.last_guess = guess
        self.last_one = not_sure
        return guess

    def snipe_two(self):
        self.last_guess_mode = 2
        not_sure = [c for c in self.cards_info if self.cards_info[c] is None]
        negative = random.choice([c for c in self.cards_info if self.cards_info[c] == False])
        paired_cards = [c for p in self.positive_pairs for c in p]
        candidates = list(set(not_sure) - set(paired_cards))
        if len(candidates) < 2:
            return
        self.last_pair = candidates[0:2]
        guess = set(self.last_pair + [negative])
        return guess

    def snipe_three(self):
        self.last_guess_mode = 3
        info = sorted(list(self.cards_info.items()), key=lambda x: sort_card(x[0]))
        print info
        # print '\n'.join()
        l = [c for c in self.cards_info if self.cards_info[c] is None]
        random.shuffle(l)
        guess = set(l[0:3])
        self.last_triad = guess
        return guess

    def snipe(self):
        guess = self.snipe_two()
        if guess:
            self.last_guess = guess
            return guess
        else:
            guess = self.snipe_one()
            self.last_guess = guess
            return guess


    def update(self, revealed):
        for c in revealed:
            self.cards_info[c] = False
        for p in self.positive_pairs:
            if self.cards_info[p[0]] == False:
                self.cards_info[p[1]] = True
                # self.positive_pairs.remove(p)
            if self.cards_info[p[1]] == False:
                self.cards_info[p[0]] = True
                # self.positive_pairs.remove(p)
        for t in self.positive_triads:
            if sum(1 for c in t if self.cards_info[c] == False) == 2:
                for c in t:
                    if c != False:
                        self.cards_info[c] = True
                # self.positive_triads.remove(t)

    def make_guess(self, revealed):
        self.update(revealed)
        positive = self.cards_info.values().count(True)
        not_sure = self.cards_info.values().count(None)
        if positive + not_sure == 3:
            return set(
                key for key, val in self.cards_info.items()
                if val == True or val is None
            )
        else:
            return self.snipe()
        # elif positive > 2:
        #     self.last_guess = self.snipe_one()
        #     return self.last_guess
        # else:
        #     self.last_guess = self.snipe_two()
        #     return self.last_guess
        # elif positive == 0:
        # 	return self.snipe_three()

    def got_guess(self, guess):
        self.guess_got.add(guess)

    def got_answer(self, answer):
        if answer == False:
            for c in self.last_guess:
                self.cards_info[c] = False
        elif answer == None:
            if self.last_guess_mode == 3:
                self.positive_triads.append(list(self.last_triad))
            elif self.last_guess_mode == 2:
                self.positive_pairs.append(list(self.last_pair))
            else:
                # Snipe One
                self.cards_info[self.last_one] = True

class InteractivePlayer(Player):
    def __init__(self, name=None):
        super(InteractivePlayer, self).__init__(name)
        self.guess_made = set()

    def display_hand(self):
        print 'Your hand: ' + str(sorted_cards(self.hand))

    def make_guess(self, revealed):
        self.display_hand()
        guess = set()
        while len(guess) < 3:
            s = raw_input('Please enter your guess:')
            l = [c for c in s if c in all_cards or c == '1']
            if "1" in l:
                l[l.index('1')] = '10'
            guess = set(l[0:3])
        print
        self.last_guess = guess
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
            + '\n'.join("%s" % str(p) for p in self.players) + '\n'
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
                self.new_player(OkayPlayer())
                break
            elif mode == '2':
                self.new_player(InteractivePlayer())
                self.new_player(InteractivePlayer())
                break
            elif mode == '3':
                self.new_player(OkayPlayer())
                self.new_player(OkayPlayer())
                # self.new_player(StupidPlayer())
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
            self.play()

            # Stop if player 1 got it right
            if self.check_winner():
                break

            # swap turn
            self.attacker, self.defender = self.defender, self.attacker

            # Player 2 first attacks
            self.play()

            # Stop if player 2 got it right
            if self.check_winner():
                break

            # reveal one card
            if self.round >= 2:
                self.deck.reveal()
                print self.deck
                print

            # swap turn
            self.attacker, self.defender = self.defender, self.attacker

        if self.deck.empty():
            self.winner = self.attacker
        self.game_over()

    def game_over(self):
        print 'Game Over!'
        print self.winner.name + ' Won!'

    def attacker_message(self, guess):
        print (
            self.attacker.name + ': '
            + '"%s"' % (', '.join(c for c in sorted_cards(guess)))
        )

    def defender_message(self, answer):
        print self.defender.name + ': ' + '"%s"' % say_answer[answer]

    def play(self):
        # attacker makes guess
        guess = self.get_guess()
        self.attacker_message(guess)
        self.defender.got_guess(guess)

        # defender answers
        answer = self.defender.answer_guess(guess)
        self.defender_message(answer)
        self.attacker.got_answer(answer)

        # end game if someone wins
        if answer:
            self.winner = self.attacker
        print

    def get_guess(self):
        guess = frozenset(self.attacker.make_guess(self.deck.revealed))
        if len(guess) != 3:
            raise ValueError("Invalid guess!")
        return guess

    def check_winner(self):
        if self.winner:
            return True
        else:
            return False

game = Game()
game.start()
