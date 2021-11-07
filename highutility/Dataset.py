class Dataset(object):
    def __init__(self, datasetPath, maximumTransactionCount):
        self.transactions = None
        self.__maxItem = 0

        self.transactions = []
        br = BufferedReader(FileReader(datasetPath))
        line = None
        i =0
        while (line = br.readLine()) is not None:
            if not line == True or line[0] == '#' or line[0] == '%' or line[0] == '@':
                continue
            i += 1
            self.transactions.append(createTransaction(line))
            if i==maximumTransactionCount:
                break
        print("Transaction count :" + len(self.transactions))
        br.close()
    
    def __createTransaction(self, line):
        split = line.split(":")
        transactionUtility = int(split[1])
        itemsString = split[0].split(" ")
        itemsUtilitiesString = split[2].split(" ")
        items = [0 for _ in range(len(itemsString))]
        utilities = [0 for _ in range(len(itemsString))]
        i = 0
        while i < len(items):
            items[i] = int(itemsString[i])
            utilities[i] = int(itemsUtilitiesString[i])
            if items[i] > maxItem:
                maxItem = items[i]
            i += 1
        return Transaction(items, utilities, transactionUtility)

    def getTransactions(self):
        return transactions

    def getMaxItem(self):
        return maxItem
    def toString(self):
        datasetContent = StringBuilder()
        for transaction in transactions:
            datasetContent.append(str(transaction))
            datasetContent.append("\n")
        return str(datasetContent)

