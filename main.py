import re

class Row:
    def __init__(self, phase, forceX, forceY, forceZ):
        self.phase = phase
        self.forceX = forceX
        self.forceY = forceY
        self.forceZ = forceZ


class Table:
    def __init__(self, name):
        self.name = name
        self._rows = []

    def addRow(self, row):
        self._rows.append(row)
    

class Results:
    def __init__(self, fileName):
        self.fileName = fileName
        self.tables = []

class Chunker:
    def __init__(self, startRegexExp, terminateRegexExp, fileName):
        self.startRegexExp = startRegexExp
        self.terminateRegexExp = terminateRegexExp
        self.fileName = fileName
        self.chunks = []

    def processFile(self):
        babyChunk = ""
        chunkin = False

        with open(self.fileName) as file:
            for line in file:
                if(chunkin):
                    if(self.finish(line)):
                        completeBabychunk = babyChunk
                        self.chunks.append(completeBabychunk)
                        babyChunk = ""
                    else:
                        babyChunk += line
                else:
                    chunkin = self.start(line)

    def finish(self, line):
        return re.search(self.terminateRegexExp, line)

    def start(self, line):
        return re.search(self.startRegexExp, line) 

    def getChunks(self):
        return self.chunks

#"SEASTATE NO    [0-9]"
#Test code:
row = Row(1,2,3,4)
table = Table("TestTable")
table.addRow(row)
