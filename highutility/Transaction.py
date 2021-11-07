class Transaction(object):

    def _initialize_instance_fields(self):
        self.offset = 0
        self.items = []
        self.utilities = []
        self.transactionUtility = 0
        self.prefixUtility = 0

    tempItems = [0 for _ in range(2000)]
    tempUtilities = [0 for _ in range(2000)]
    def __init__(self, items, utilities, transactionUtility):
        self._initialize_instance_fields()

        self.items = items
        self.utilities = utilities
        self.transactionUtility = transactionUtility
        self.offset = 0
        self.prefixUtility = 0
    def __init__(self, transaction, offsetE):
        self._initialize_instance_fields()

        self.items = transaction.getItems()
        self.utilities = transaction.getUtilities()
        utilityE = self.utilities[offsetE]
        self.prefixUtility = transaction.prefixUtility + utilityE
        self.transactionUtility = transaction.transactionUtility - utilityE
        i = transaction.offset
        while i < offsetE:
            self.transactionUtility -= transaction.utilities[i]
            i += 1
        self.offset = offsetE+1
    def toString(self):
        buffer = StringBuilder()
        i = offset
        while i < len(self.items):
            buffer.append(self.items[i])
            buffer.append("[")
            buffer.append(self.utilities[i])
            buffer.append("] ")
            i += 1
        buffer.append(" Remaining Utility:" +self.transactionUtility)
        buffer.append(" Prefix Utility:" + self.prefixUtility)
        return str(buffer)
    def getItems(self):
        return self.items
    def getUtilities(self):
        return self.utilities
    def getLastPosition(self):
        return len(self.items) -1
    def removeUnpromisingItems(self, oldNamesToNewNames):
        i = 0
        j = 0
        while j< len(self.items):
            item = self.items[j]
            newName = oldNamesToNewNames[item]
            if newName != 0:
                tempItems[i] = newName
                tempUtilities[i] = self.utilities[j]
                i += 1
            else:
                self.transactionUtility -= self.utilities[j]
            j += 1
        self.items = [0 for _ in range(i)]
        System.arraycopy(tempItems, 0, self.items, 0, i)
        self.utilities = [0 for _ in range(i)]
        System.arraycopy(tempUtilities, 0, self.utilities, 0, i)
        insertionSort(self.items, self.utilities)
    @staticmethod
    def insertionSort(items, utitilies):
        j = 1
        while j< len(items):
            itemJ = items[j]
            utilityJ = utitilies[j]
            i = j - 1
            while i>=0 and (items[i] > itemJ):
                items[i+1] = items[i]
                utitilies[i+1] = utitilies[i]
                i -= 1
            items[i+1] = itemJ
            utitilies[i+1] = utilityJ
            j += 1
