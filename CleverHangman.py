'''
Description:
        You must create a Hangman game that allows the user to play and guess a secret word.
        See the assignment description for details.

@author: Karen Wang    kw336
'''


import random


def handleUserInputDebugMode():
    '''
    This function will prompt the user if they wish to play in debug mode. True is returned
     if the user enters the letter “d”, indicating debug mode was chosen; False is returned otherwise.
    '''

    mode = input('Which mode do you want: (d)ebug or (p)lay')
    if mode == 'd':
        return True
    elif mode == 'p':
        return False



def handleUserInputWordLength():
    '''
    This function returns an integer value specified by the user that determines how long secretWord should be.
    '''
    length = input('How many letters in the word you will guess?')
    return int(length)



def handleUserInputDifficulty(): #keep as is
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



def createTemplate(currTemplate, letterGuess, word):
    '''
    Creates a new template for the secret word that user will see, returning it as a string.
    '''
    template = []
    for ch in currTemplate:
        template.append(ch)
    for i in range(len(word)):
        if word[i] == letterGuess:
            template[i] = letterGuess
    return ''.join(template)



def getNewWordList(currTemplate, letterGuess, wordList, debug):
    '''
    Constructs a dictionary of strings as the keys and lists as the values. Returns the (key, value) pair with
    longest list. Ties are broken by the most number of underscores.
    '''

    dict = {}
    for word in wordList:
        key = createTemplate(currTemplate, letterGuess, word)
        if key not in dict:
            dict[key] = [word]
        else:
            dict[key].append(word)

    tuples = sorted(dict.items(), key=lambda x: x[0].count('_'), reverse=True)
    tuples = sorted(tuples, key=lambda x: len(x[1]), reverse=True)
    if debug:
        for x in sorted(dict.items()):
            print(x[0], ':', len(x[1]))
        print('# keys =', len(dict.items()))
    return tuples[0]



def createDisplayString(lettersGuessed, missesLeft, hangmanWord): #modified
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(len(alphabet)):
        if alphabet[i] in lettersGuessed:
            alphabet[i] = ' '
    hangmanString = ' '.join(hangmanWord)
    return "letters not yet guessed: " + ''.join(alphabet) + "\n" + "misses " \
                                                              "remaining = " \
           + str(missesLeft) + "\n" + hangmanString





def handleUserInputLetterGuess(lettersGuessed, displayString): #keep as is
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



def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    '''
    Takes the user's guess, the user's current progress on the word, and the number of misses left;
    updates the number of misses left and indicates whether the user missed.
    '''

    if guessedLetter not in hangmanWord:
        missesLeft -= 1
        bool = False
    else:
        bool = True
    return [missesLeft, bool]


def runGame(filename): #modify
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''
    debug = handleUserInputDebugMode()

    f = open(filename)
    words = []
    for line in f:
        line = line.strip()
        words.append(line)
    f.close()

    length = handleUserInputWordLength()
    wordList = [x for x in words if len(x) == length]
    word = random.choice(wordList)

    missesLeft = handleUserInputDifficulty()

    hangmanWord = ['_' for ch in word]
    currTemplate = ''.join(hangmanWord)
    lettersGuessed = []

    while missesLeft > 0 and ''.join(hangmanWord) != word:
        displayString = createDisplayString(lettersGuessed, missesLeft, hangmanWord)
        letterGuess = handleUserInputLetterGuess(lettersGuessed, displayString)
        lettersGuessed.append(letterGuess)

        if debug == True:
            print('(word is ' + word + ')')
            print('# possible words: ', len(wordList))

        possible = getNewWordList(currTemplate, letterGuess, wordList, debug)
        hangmanWord = [ch for ch in possible[0]]
        wordList = possible[1]
        word = random.choice(possible[1])
        currTemplate = possible[0]
        result = processUserGuessClever(letterGuess, hangmanWord,
                              missesLeft)
        missesLeft = result[0]
        if letterGuess not in word:
            print('you missed: ' + letterGuess + ' not in word')


    if missesLeft <= 0:
        print("you're hung!" + '\n' + 'word is ' + word)
        return False
    if '_' not in hangmanWord:
        print('you guessed the word ' + word)
        return True


if __name__ == "__main__":
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
