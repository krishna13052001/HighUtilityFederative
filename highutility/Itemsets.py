from . import Itemset
class Itemsets(object):
    def __init__(self, name):
        #instance fields found by Java to Python Converter:
        self.__levels = []
        self.__itemsetsCount = 0
        name = None

        self.__name = name
        self.__levels.append([])
    def printItemsets(self):
        print(" ------- " + self.__name + " -------")
        patternCount = 0
        levelCount = 0
        for level in self.__levels:
            print("  L" + levelCount + " ")
            for itemset in level:
                itemset.getItems().sort()
                print("  pattern " + patternCount + ":  " +str(itemset), end = '')
                print("Utility :  " + itemset.getUtility(), end = '')
                patternCount += 1
                print(" ")
            levelCount += 1
        print(" --------------------------------")
    def addItemset(self, itemset, k):
        while len(self.__levels) <= k:
            self.__levels.append([])
        self.__levels[k].append(itemset)
        self.__itemsetsCount += 1
    def getLevels(self):
        return self.__levels
    def getItemsetsCount(self):
        return self.__itemsetsCount
    def setName(self, newName):
        self.__name = newName
    def decreaseItemsetCount(self):
        self.__itemsetsCount -= 1
