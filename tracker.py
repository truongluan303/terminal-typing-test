from sentence import Sentence
from fileInOut import FileInOut
import time, random

class Tracker:
    def __init__(self) -> None:
        # variables
        self.totalWords = 0
        self.totalChar = 0
        self.tic = 0
        self.toc = 0
        self.timeInSec = 0
        self.errors = 0
        self.totalErrors = 0
        self.wordsInLine = []
        self.sentences = self.__getSentences()

    
    def startTiming(self):
        self.tic = time.perf_counter()


    def doneTiming(self):
        self.toc = time.perf_counter()
        self.timeInSec = self.toc - self.tic 


    # look for errors that the typer made
    def checkError(self, userLine: str):
        i = 0
        errorsFound = 0
        errorsAt = []
        # loop through each word in both strings and check if there's a difference
        for standardWord, userWord in zip(self.wordsInLine, userLine.split()):
            if standardWord != userWord:
                errorsFound += 1
                errorsAt.append(userWord)
        self.errors = errorsFound
        return errorsAt     # return the strings that were typed wrong
    

    def getFinalResult(self):
        # for the last sentence, getNewSentence was not called, so we have to update the
        # typos error here for the very last sentence
        self.totalErrors += self.errors
        # create a result string for output
        result = str(self.totalWords) + " words / " + str(self.totalChar) + " characters " 
        result += "in " + str(round(self.timeInSec)) + " seconds\n"
        result += str(self.totalErrors) + " typo errors / "
        result += "Accuracy: " + str(self.__getAccuracy()) + " %\n"
        result += "WPM = " + str(self.__getWPM())
        return result


    def getNewSentence(self):
        # update the errors from the last sentence before moving to the new one
        self.totalErrors += self.errors
        # randomly pick a new sentence
        rand = random.randint(1, len(self.sentences) - 1)
        newSentence: Sentence = self.sentences.pop(rand)
        # get the string from the new sentence object
        line: str = newSentence.getString()
        self.wordsInLine.clear()
        for word in line.split():
            self.wordsInLine.append(word)
        # get the number of words and characters from the new sentence object
        self.totalWords += newSentence.getWordsCount()
        self.totalChar += newSentence.getCharCount()
        return newSentence


    def __getWPM(self):
        wpm = round(self.__getAccuracy() * (self.totalWords / (self.timeInSec / 60)) / 100)
        return wpm

    def __getAccuracy(self):
        return (100 - round((self.totalErrors / self.totalWords) * 100))

    # get all the sentences read from the input text file
    def __getSentences(self):
        fileIO = FileInOut()
        fileIO.readFile("input.txt")
        return fileIO.getSentences()
        
    