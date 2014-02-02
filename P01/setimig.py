
from random import randint

class Game():
    def __init__(self):
        self.playerOption = None
        self.initializeDeck()
        self.playerDeck = []
        self.adaDeck = []
    def initializeDeck(self):
        """
        Utility method to initialize the game's deck
        """
        self.deck = range(1, 11)
    def run(self):
        """
        Core method of the game
        """
        print "Set i Mig"
        print ""
        print "  1. Agafar una altra carta"
        print "  2. Plantar-se"
        print ""
        self.getPlayerOption()
        while self.playerOption != 2 and len(self.deck) > 0:
            c = self.getCard()
            self.playerDeck.append(c)
            print "[%d], %s, Punts: %f" % ( c, self.getStringDeck(self.playerDeck), self.getDeckScore(self.playerDeck) )
            print ""
            self.getPlayerOption()
        print ""
        print "Torn d'ADA..."
        print ""
        self.initializeDeck()
        self.playAdaTurn()
        playerScore = self.getDeckScore(self.playerDeck)
        adaScore = self.getDeckScore(self.adaDeck)
        playerDistance = self.getDistance(self.playerDeck)
        adaDistance = self.getDistance(self.adaDeck)
        print ' TU:', self.getStringDeck(self.playerDeck), playerScore, playerDistance
        print 'ADA:', self.getStringDeck(self.adaDeck), adaScore, adaDistance
        print ""
        if playerScore == 0:
            print "PER PLANTAR-TE NO PENSIS QUE POTS GUANYAR A ADA..."
        else:
            if playerDistance > 0:
                if adaDistance >= 0:
                    print "TOTS DOS HEU PERDUT!"
                else:
                    print "HAS PERDUT!"
            else:
                if adaDistance > 0:
                    print "HAS GUANYAT!"
                else:
                    if abs(playerDistance) > abs(adaDistance):
                        print "HAS PERDUT!"
                    elif abs(playerDistance) < abs(adaDistance):
                        print "HAS GUANYAT!"
                    else:
                        print "HEU EMPATAT!"
    def playAdaTurn(self):
        """
        ADA turn simulation. Pretty eager the girl...
        """
        while self.getDeckScore(self.adaDeck) < 7.5 and len(self.deck) > 0:
            # Always eagerly fetch a card
            self.adaDeck.append(self.getCard())
            # Verify how many points is ADA from getting 7.5
            distance = self.getDistance(self.adaDeck)
            if distance > 0:
                # ADA knows that she has lost :(
                break
            else:
                # ADA tries to find if there's a card in the deck
                # that would satisfy the 7.5
                distance = abs(distance)
                if distance > 0.5:
                    # In case the distance to 7.5 is greater than 0.5,
                    # ADA tries to find if there's a card suitable to
                    # her needs
                    try:
                        self.deck.index(int(distance))
                    except ValueError:
                        # If ADA does not find any card in the deck,
                        # simply end the game.
                        break
                else:
                    # Otherwise, we try to find if we have any card
                    # greater than 7.
                    cards = filter(lambda n: n > 7, self.deck)
                    if len(cards) == 0:
                        # If there's no card with value greater than 7,
                        # end the game.
                        break
    def getDistance(self, deck):
        """
        Returns the difference of a deck's score with 7.5
        """
        return self.getDeckScore(deck) - 7.5
    def getCard(self):
        """
        Get a random card of the deck, and remove the card from it.
        """
        i = randint(0, len(self.deck) - 1)
        return self.deck.pop(i)
    def getDeckScore(self, deck):
        """
        Returns the score of the deck.
        """
        s = 0
        for card in deck:
            if card > 7:
                s += 0.5
            else:
                s += card
        return s
    def getStringDeck(self, deck):
        """
        Returns a string representation of a deck.
        """
        if len(deck) == 0:
            return '()'
        s = '('
        for card in deck:
            if card <= 7: s += '[%d], ' % card
            elif card == 8: s += '[S], '
            elif card == 9: s += '[C], '
            elif card == 10: s += '[R], '
        return s[:-2] + ')'
    def getPlayerOption(self):
        """
        Asks the player which option to choose.
        """
        self.playerOption = input("Selecciona: ")

if __name__ == '__main__':
    Game().run()
