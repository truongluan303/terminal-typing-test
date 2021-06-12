import re

class Sentence(object):
    def __init__(self, string) -> None:
        self.string = string
        self.wordsCount = self.__countWords()
        self.charCount = self.__countChar()

    def getString(self):
        return self.string

    def getWordsCount(self):
        return self.wordsCount

    def getCharCount(self):
        return self.charCount

    def setString(self, newString):
        self.string = newString
        self.wordsCount = self.__countWords()
        self.charCount = self.__countChar()
        
    def __countWords(self):
        return len(re.findall(r'\w+', self.string))

    def __countChar(self):
        # total number of characters in the string
        total = len(self.string)   
        # total number of spaces
        spaceCount = sum(map(lambda x : 1 if ' ' in x else 0, self.string))
        return (total - spaceCount)