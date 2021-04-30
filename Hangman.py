'''
Description:
        You must create a Hangman game that allows the user to play and guess a secret word.  
        See the assignment description for details.
    
@author: Karen Wang    kw336
'''


import random

def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''
    
    print('How many misses do you want? Hard has 8 and Easy has 12.')
    mode = input('(h)ard or (e)asy> ')
    if mode == 'h':
        print('You have 8 misses to guess word')
        return 8
    elif mode == 'e':
        print('You have 12 misses to guess word')
        return 12




def getWord(words, length):
    '''
    Selects the secret word that the user must guess. 
    This is done by randomly selecting a word from words that is of length length.
    '''

    sameLengths = [x for x in words if len(x) == length]
    secretWord = random.choice(sameLengths)
    return secretWord




def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    sortedList = sorted(lettersGuessed)
    sortedString = ' '.join(sortedList)
    hangmanString = ' '.join(hangmanWord)
    return "letters you've guessed: " + sortedString + "\n" + "misses " \
                                                              "remaining = " \
           + str(missesLeft) + "\n" + hangmanString





def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    
    print(displayString)
    guessed = '&'
    while guessed == '&':
        guess = str(input('letter> '))
        if guess not in lettersGuessed:
            guessed = guess
        else:
            print('you already guessed that')
    return guess




def updateHangmanWord(guessedLetter, secretWord, hangmanWord):
    '''
    Updates hangmanWord according to whether guessedLetter is in secretWord and where in secretWord guessedLetter is in.
    '''
    
    if guessedLetter in secretWord:
        for i in range(len(secretWord)):
            if secretWord[i] == guessedLetter:
                hangmanWord[i] = guessedLetter
    return hangmanWord




def processUserGuess(guessedLetter, secretWord, hangmanWord, missesLeft):
    '''
    Uses the information in the parameters to update the user's progress in the hangman game.
    '''

    if guessedLetter not in secretWord:
        missesLeft -= 1
        return [hangmanWord, missesLeft, False]
    else:
        hangmanWord = updateHangmanWord(guessedLetter, secretWord, hangmanWord)
        return [hangmanWord, missesLeft, True]




def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''
    
    f = open(filename)
    words = []
    for line in f:
        line = line.strip()
        words.append(line)
    f.close()
    length = random.randint(5, 10)

    missesLeft = handleUserInputDifficulty()
    secretWord = getWord(words, length)

    hangmanWord = ['_' for ch in secretWord]
    lettersGuessed = []

    while missesLeft > 0 and ''.join(hangmanWord) != secretWord:
        displayString = createDisplayString(lettersGuessed, missesLeft, hangmanWord)
        guessedLetter = handleUserInputLetterGuess(lettersGuessed, displayString)
        lettersGuessed.append(guessedLetter)
        result = processUserGuess(guessedLetter, secretWord, hangmanWord,
                              missesLeft)
        if result[2] == False:
            missesLeft -= 1
        if guessedLetter not in secretWord:
            print('you missed: ' + guessedLetter + ' not in word')

    if missesLeft <= 0:
        print("you're hung!" + '\n' + 'word is ' + secretWord)
        return False
    if '_' not in hangmanWord:
        print('you guessed the word ' + secretWord)
        return True


if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    result = runGame('lowerwords.txt')
    wins = 0
    losses = 0
    if result == True:
        wins += 1
    elif result == False:
        losses += 1
    again = input('Do you want to play again? y or n>')
    while again == 'y':
        result = runGame('lowerwords.txt')
        if result == True:
            wins += 1
        elif result == False:
            losses += 1
        again = input('Do you want to play again? y or n>')
    print('You won ' + str(wins) + ' game(s) and lost ' + str(losses))