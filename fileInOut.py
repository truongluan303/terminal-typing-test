from sentence import Sentence

class FileInOut():
    def __init__(self) -> None:
        self.sentenceList = []
    
    def readFile(self, fileName):
        f = open(fileName)
        line = f.readline
        line = str(line)
        while line:
            newSentence = Sentence(line)
            self.sentenceList.append(newSentence)
            line = f.readline()

    def getSentences(self):
        return self.sentenceList
