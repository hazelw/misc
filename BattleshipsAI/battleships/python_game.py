from random import randint, choice

__author__ = 'Hazel'
battleshipLengthsAvailable = [6,5,5,4]

class GameBoard:
    '''
    Class that holds information about the game board (such as full and masked states, how many ships have been hit)
    '''

    def __init__(self):
        '''
        :return: nil

        Generates an empty game board.
        '''

        self.gameBoard = []
        self.maskedBoard = []
        self.hitShips = 0

        # generates an empty board
        for i in range(10):
            # todo: find a better way of doing this - list comprehensions?
            currentList = []
            maskedList = []
            for j in range(10):
                currentList.append('#')
                maskedList.append('~')
            self.gameBoard.append(currentList)
            self.maskedBoard.append(maskedList)


    def printBoard(self):
        '''
        :return: nil

        Prints an uncensored version of the game board
        '''
        for x in range(10):
            for y in range(10):
                print(self.gameBoard[x][y], end='')
            print('')

    def printMaskedBoard(self):
        '''
        :return: nil

        Prints a censored version of the game board
        '''
        for x in range(10):
            for y in range(10):
                print(self.maskedBoard[x][y], end='')
            print('')

    def addBattleship(self, x, y, length, direction):
        '''
        adds the battleship if it does not intercept any other battleship - returns false otherwise
        :param x: x-coordinate of new battleship
        :param y: y-coordinate of new battleship
        :param length: size of new battleship
        :param direction: direction of new battleship - V/H for vertical/horizontal
        :return: true if adding the battleship was successful, false otherwise
        '''

        if direction == 'V':
            currentLoc = 0
            while currentLoc < length:
                if(self.gameBoard[y+currentLoc][x] == 'o'):
                    print('New battleship overlays current battleship')
                    return False
                else:
                    currentLoc += 1;
        elif direction == 'H':
            currentLoc = 0
            while currentLoc < length:
                if(self.gameBoard[y][x+currentLoc] == 'o'):
                    print('New battleship overlays current battleship')
                    return False
                else:
                    currentLoc += 1;
        else:
            return False

        # the new battleship does not intersect an old battleship - actually add the battleship
        if direction == 'V':
            currentLoc = 0
            while currentLoc < length:
                self.gameBoard[y+currentLoc][x] = 'o'
                currentLoc += 1
        elif direction == 'H':
            currentLoc = 0
            while currentLoc < length:
                self.gameBoard[y][x+currentLoc] = 'o'
                currentLoc += 1

        return True

    def makeGuess(self, x, y):
        '''
        :param x: x-coordinate of the player's/AI's guess
        :param y: y-coordinate of the player's/AI's guess
        :return: nil

        Checks if the location has already been selected, returns an error message if so. If not, copies across the
        value of the square to the censored game board and increments the number of hit ships on the board
        '''

        if(self.maskedBoard[y][x] == '~'):
            self.maskedBoard[y][x] = self.gameBoard[y][x]
            if(self.gameBoard[y][x] == 'o'):
                print("Battleship hit!")
                self.hitShips += 1
                return True
        else:
            print('Oops! That square had already been selected')

        return False


class Game:
    def __init__(self):
        '''
        initialises the game
        :return: nil
        '''

        gameBoard = GameBoard()
        gameBoard.printBoard()
        self.setupplayer()
        self.playGame()

    def setupplayer(self):
        '''
        :return: nil

        Captures all player information (eg. name, battleship locations)
        '''

        for battleshipLength in battleshipLengthsAvailable:
            while True:
                try:
                    locationResponse = input('Please select a location for your %s block battleship (format x,y)' %(str(battleshipLength)))
                    x = int(locationResponse.split(',')[0])
                    y = int(locationResponse.split(',')[1])

                    while(True):
                        direction = input('Please enter a direction for your battleship (H/V)')

                        if(direction == 'H'):
                            if(x + battleshipLength > 10):
                                raise BattleshipOutOfBoundsException
                                pass
                            else:
                                break
                        elif (direction == 'V'):
                            if(y + battleshipLength > 10):
                                raise BattleshipOutOfBoundsException
                                pass
                            else:
                                break
                        else:
                            print('Direction invalid')

                    if (player.gameBoard.addBattleship(x,y,battleshipLength,direction) == True):
                        player.gameBoard.printBoard()
                        break
                except BattleshipOutOfBoundsException:
                    print('Battleship out of bounds')

    def playGame(self):
        '''
        :return: nil

        Kicks off the game, requests guesses from the player.
        '''
        winner = None

        while(winner == None):
            guess = input('Your turn, select coordinates (of form x,y): ')
            player.makeGuess(guess)

            if(ai.makeGuess() == True):
                print('AI hit!')
            else:
                print('AI missed')

            winner = self.checkWinCondition()

            if(winner != None):
                print("And the winner is... " + winner.name)


    def checkWinCondition(self):
        '''
        :return: winner of the game, else None

        Checks if the game has been won - if so, returns the winner of the game (either the Player object or the AI
        object)
        '''

        if(player.gameBoard.hitShips == 20):
            return ai
        elif(ai.gameBoard.hitShips == 20):
            return player
        else:
            return None


class Player:
    '''
    Represents the human player.
    '''
    name = ''
    gameBoard = GameBoard()

    def __init__(self, name):
        '''
        :param name:
        :return: nil

        Initialises the player, gives them a name (aww)
        '''
        self.name = name

    def makeGuess(self, guess):
        '''
        :param guess: x,y coordinates of the player's guess
        :return: nil

        Makes the guess input by the player.
        '''
        guess = guess.split(',')
        x_guess = int(guess[0])
        y_guess = int(guess[1])

        AI.gameBoard.makeGuess(x_guess, y_guess)
        print("Your view:")
        AI.gameBoard.printMaskedBoard()


class AI(Player):
    '''
    Represents the AI player.
    '''
    gameBoard = GameBoard()

    def __init__(self):
        '''
        :return nil

        initialises the AI, creates a bunch of battleships for it
        '''
        self.name = 'AI'
        self.generateBattleships()

    def generateBattleships(self):
        '''
        :return: nil

        Generates battleships for the AI.
        '''
        temp = 0
        for battleshipLengthAvailable in battleshipLengthsAvailable:
            direction = choice(['V','H'])
            while(True):
                temp += 1
                if(direction == 'V'):
                    x = randint(0,9)
                    y = randint(0,9-battleshipLengthAvailable)
                elif(direction == 'H'):
                    x = randint(0,9-battleshipLengthAvailable)
                    y = randint(0,9)

                if(self.gameBoard.addBattleship(x,y,battleshipLengthAvailable,direction) == True):
                    break


    def makeGuess(self):
        '''
        :return: nil

        makes a random move if either no battleships hit/all battleships it can see are surrounded by water
        makes a move up/down/left/right if battleship looks like it continues
        '''

        print("AI's view: ")
        print(player.gameBoard.printMaskedBoard())

        for i in range(10):
            for j in range(10):
                if player.gameBoard.maskedBoard[i][j] == 'o':
                    if(i-1 >= 0 and player.gameBoard.maskedBoard[i-1][j] == '~'):
                        return player.gameBoard.makeGuess(j,i-1)
                    elif(i+1 < 10 and player.gameBoard.maskedBoard[i+1][j] == '~'):
                        return player.gameBoard.makeGuess(j,i+1)
                    elif(j-1 >= 0 and player.gameBoard.maskedBoard[i][j-1] == '~'):
                        return player.gameBoard.makeGuess(j-1,i)
                    elif(j+1 < 10 and player.gameBoard.maskedBoard[i][j+1] == '~'):
                        return player.gameBoard.makeGuess(j+1,i)

        maskedChoice = '~'
        choice_x = None
        choice_y = None
        while (maskedChoice == '~'):
            choice_x = randint(0,9)
            choice_y = randint(0,9)

            maskedChoice = player.gameBoard.makeGuess(choice_x,choice_y)

        return maskedChoice


class BattleshipOutOfBoundsException(Exception):
    '''
    Exception thrown when someone attempts to add a battleship outside of the grid.
    '''
    pass


name = input("What is your name?")
player = Player(name)
ai = AI()
Game()