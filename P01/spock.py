
from random import randint

class Result():
    """
    A class emulating an enumeration of possible results of the game.
    """
    WIN = 0
    LOSE = 1
    DRAW = 2

class Weapon():
    """
    Base class of RPSSL component. It does have the logic to play against other weapons.
    """
    def __init__(self):
        self.strongAgainst = {}
    def strong(self, weaponClass, verb):
        """
        Defines that the weapon class passed by is weaker than self, and verbs it. Err I mean
        it indicate what self does to the weapon class passed by.
        """
        self.strongAgainst[weaponClass] = verb
    def battle(self, weapon):
        """
        Simulate a battle between a weapon and self. It returns a tuple of:
         - Result Static value
         - Action of the battle
        """
        if self.__class__ == weapon.__class__:
            return ( Result.DRAW, None )
        if weapon.__class__ in self.strongAgainst:
            action = '%s %s %s' % ( self.__class__.__name__, self.strongAgainst[weapon.__class__], weapon.__class__.__name__ )
            return ( Result.WIN, action )
        action = '%s %s %s' % ( weapon.__class__.__name__, weapon.strongAgainst[self.__class__], self.__class__.__name__ )
        return ( Result.LOSE, action )
    def __str__(self):
        """
        Returns the string representation of self.
        """
        return self.__class__.__name__

class Rock(Weapon):
    """
    The Rock. Strong against the Scissors and the Lizzard.
    """
    def __init__(self):
        Weapon.__init__(self)
        self.strong(Scissors, 'crushes')
        self.strong(Lizzard, 'crushes')

class Paper(Weapon):
    """
    Paper. You use it on any thesis, and can disprove Spock. Also kills Rock, WITHOUT FIRE!!
    """
    def __init__(self):
        Weapon.__init__(self)
        self.strong(Rock, 'covers')
        self.strong(Spock, 'disprove')

class Scissors(Weapon):
    """
    The sharp Scissors can cut through Paper and Lizzards.
    """
    def __init__(self):
        Weapon.__init__(self)
        self.strong(Paper, 'cuts')
        self.strong(Lizzard, 'decapitates')

class Spock(Weapon):
    """
    Live long and prosper. Smashes and Vaporizes. 'nuf said.
    """
    def __init__(self):
        Weapon.__init__(self)
        self.strong(Scissors, 'smashes')
        self.strong(Rock, 'vaporizes')

class Lizzard(Weapon):
    """
    Weeeeeeeeee. It poisons Spock, and eats Paper for breakfast.
    """
    def __init__(self):
        Weapon.__init__(self)
        self.strong(Spock, 'poisons')
        self.strong(Paper, 'eats')

class Game():
    """
    The game main logic class.
    """
    def __init__(self):
        self.weapons = [Rock(), Paper(), Scissors(), Spock(), Lizzard()]
        self.playerOption = None
        self.playerScore = 0
        self.adaOption = None
        self.adaScore = 0
    def showPresentation(self):
        """
        Utility method to state business and options.
        """
        print "Rock, Paper, Scissors, Spock, Lizzard"
        print ""
        print "  1. Rock"
        print "  2. Paper"
        print "  3. Scissors"
        print "  4. Spock"
        print "  5. Lizzard"
        print "  6. END THE GAME (AND YOU JUST LOST)"
        print ""
    def showScore(self):
        """
        It shows how severely pwned you've been.
        """
        print ""
        print "  Player  |    Ada"
        print " -------------------"
        print "   %3d    |   %3d" % ( self.playerScore, self.adaScore )
        print ""
    def getPlayerOption(self):
        """
        Sets the player's option after being inputted at the standard input.
        """
        try:
            self.playerOption = input("Choose: ")
        except SyntaxError:
            self.playerOption = None
    def getAdaOption(self):
        """
        Sets the AI option.
        """
        self.adaOption = randint(0, 4)
    def run(self):
        """
        Game core method. 
        """
        self.showPresentation()
        
        self.getPlayerOption()
        while self.playerOption != 6:
            if self.playerOption >= 0 and self.playerOption <= 6:
                self.getAdaOption()
                print "YOU:", self.weapons[self.playerOption - 1]
                print "ADA:", self.weapons[self.adaOption]
                result, action = self.weapons[self.playerOption - 1].battle(self.weapons[self.adaOption])
                if result == Result.DRAW:
                    print "DRAW!"
                else:
                    if result == Result.WIN:
                        self.playerScore += 1
                        print "%s, YOU WIN!" % action
                    else:
                        self.adaScore += 1
                        print "%s, YOU LOSE" % action
            self.getPlayerOption()
        
        self.showScore()
        print "What about a nice game of chess?"

if __name__ == '__main__':
    Game().run()
