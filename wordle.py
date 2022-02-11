#!/usr/bin/env python

import string


def parseValidWords(filepath):
    with open(filepath, 'r') as file: line = file.readline()
    words = line.replace("\"", '').split(',')
    return [word.upper() for word in words]


def countAllLetterOccurrences(words):
    letters = list(string.ascii_uppercase) 
    counts = {letter:0 for letter in letters}
    for letter in letters:
        for word in words:
            if letter in word:
                counts[letter] += 1
    return counts


def removeRepeatLetters(word):
    return str("".join(set(word)))


def evaluateWord(counts, word):
    letters = removeRepeatLetters(word)
    score = 0
    for letter in letters:
        if letter not in counts.keys(): 
            continue
        score += counts[letter]
    return score


def computeBestGuess(counts, words):
    topWord, topScore = None, 0
    for word in words:
        score = evaluateWord(counts, word)
        if score > topScore:
            topWord, topScore = word, score
    return topWord


def printGuess(word):
    print("-"*28)
    print("\t|", end="")
    for letter in word:
        print("{}|".format(letter), end="")
    print("\n"+"-"*28)

def getGuessResults(word):
    print()
    none, present, correct = [], [], []
    for i, letter  in enumerate(word):
        color = input("    |{}|\t".format(letter))
        if color.upper() == "GREY":
            none.append(letter)
        elif color.upper() == "YELLOW":
            present.append((i, letter))
        elif color.upper() == "GREEN":
            correct.append((i, letter))
        else: 
            print("Enter a wordle color you fuck")

    return none, present, correct


def removeWordsWithGreyLetters(none, words):
    updatedWords = set() 
    for word in words:
        wordIsGood = True
        for letter in none:
            if letter in word:
                wordIsGood = False
                break

        if wordIsGood:
            updatedWords.add(word)
    return list(updatedWords)


def removeWordsWithoutYellowLetters(present, words):
    updatedWords = set()
    for word in words:
        wordIsGood = True
        for location, letter in present:

            letterInWrongLocation = word[location] == letter
            letterNotInWord = letter not in word

            if letterInWrongLocation or letterNotInWord:
                wordIsGood = False
                break

        if wordIsGood:
            updatedWords.add(word)

    return list(updatedWords)


def removeWordsWithoutGreenLetters(correct, words):
    updatedWords = set()
    for word in words:
        wordIsGood = True

        for location, letter in correct:
            if word[location] != letter:
                wordIsGood = False
                break

        if wordIsGood:
            updatedWords.add(word)

    return list(updatedWords)



def distillWords(none, present, correct, words):

    updatedWords1 = removeWordsWithGreyLetters(none, words)
    updatedWords2 = removeWordsWithoutYellowLetters(present, updatedWords1)
    updatedWords3 = removeWordsWithoutGreenLetters(correct, updatedWords2)
    return updatedWords3


def main():
    words = parseValidWords("words.txt")
    counts = countAllLetterOccurrences(words)
    startWord = computeBestGuess(counts, words)
    sortedCounts = {let : count for let, count in sorted(counts.items(), key=lambda item: item[1])}
    currentGuess = startWord

    while True:
        printGuess(currentGuess) 
        none, present, correct = getGuessResults(currentGuess)
        words = distillWords(none, present, correct, words)
        print("\nPossible words remaining: {}\n\n{}\n".format(len(words), words))
        if currentGuess in words: words.remove(currentGuess)
        currentGuess = computeBestGuess(counts, words)
    
    print("\n")

if __name__ == "__main__":
    main()



