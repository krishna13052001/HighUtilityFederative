from memoryLogger import MemoryLogger
class AlgoEFIM(object):
    def __init__(self):
        self.__highUtilityItemsets = None
        self.writer = None
        self.__patternCount = 0
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.minUtil = 0
        self.DEBUG = False
        self.__utilityBinArraySU = []
        self.__utilityBinArrayLU = []
        self.__temp = [0 for _ in range(500)]
        self.timeIntersections = 0
        self.timeDatabaseReduction = 0
        self.timeIdentifyPromisingItems = 0
        self.timeSort = 0
        self.timeBinarySearch = 0
        self.oldNameToNewNames = []
        self.newNamesToOldNames = []
        self.newItemCount = 0
        self.activateTransactionMerging = False
        self.MAXIMUM_SIZE_MERGING = 1000
        self.transactionReadingCount = 0
        self.mergeCount = 0
        self.__candidateCount = 0
        self.__activateSubtreeUtilityPruning = False

    def runAlgorithm(self, minUtil, inputPath, outputPath, activateTransactionMerging, maximumTransactionCount, activateSubtreeUtilityPruning):
        self.mergeCount=0
        self.transactionReadingCount=0
        self.timeIntersections = 0
        self.timeDatabaseReduction = 0
        self.activateTransactionMerging = activateTransactionMerging
        self.__activateSubtreeUtilityPruning = activateSubtreeUtilityPruning
        self.startTimestamp = System.currentTimeMillis()
        dataset = Dataset(inputPath, maximumTransactionCount)
        self.minUtil = minUtil
        if outputPath is not None:
            self.writer = BufferedWriter(FileWriter(outputPath))
        else:
            self.writer = None
            self.__highUtilityItemsets = Itemsets("Itemsets")
        self.__patternCount = 0
        MemoryLogger.getInstance().reset()
        if self.DEBUG:
            print("===== Initial database === ")
            print(str(dataset))
        useUtilityBinArrayToCalculateLocalUtilityFirstTime(dataset)
        if self.DEBUG:
            print("===== TWU OF SINGLE ITEMS === ")
            i = 1
            while i < len(self.__utilityBinArrayLU):
                print("item : " + i + " twu: " + self.__utilityBinArrayLU[i])
                i += 1
            print()
        itemsToKeep = []
        j = 1
        while j< len(self.__utilityBinArrayLU):
            if self.__utilityBinArrayLU[j] >= minUtil:
                itemsToKeep.append(j)
            j += 1
        insertionSort(itemsToKeep, self.__utilityBinArrayLU)
        self.oldNameToNewNames = [0 for _ in range(dataset.getMaxItem() + 1)]
        self.newNamesToOldNames = [0 for _ in range(dataset.getMaxItem() + 1)]
        currentName = 1
        j = 0
        while j< len(itemsToKeep):
            item = itemsToKeep[j]
            self.oldNameToNewNames[item] = currentName
            self.newNamesToOldNames[currentName] = item
            itemsToKeep[j] = currentName
            currentName += 1
            j += 1
        self.newItemCount = len(itemsToKeep)
        self.__utilityBinArraySU = [0 for _ in range(self.newItemCount + 1)]
        if self.DEBUG:
            print(itemsToKeep)
            print(java.util.Arrays.toString(self.oldNameToNewNames))
            print(java.util.Arrays.toString(self.newNamesToOldNames))
        i = 0
        while i< dataset.getTransactions().size():
            transaction = dataset.getTransactions().get(i)
            transaction.removeUnpromisingItems(self.oldNameToNewNames)
            i += 1
        timeStartSorting = System.currentTimeMillis()
        if activateTransactionMerging:
            Collections.sort(dataset.getTransactions(), ComparatorAnonymousInnerClass(self))
            emptyTransactionCount = 0
            i = 0
            while i< dataset.getTransactions().size():
                transaction = dataset.getTransactions().get(i)
                if transaction.items.length == 0:
                    emptyTransactionCount += 1
                i += 1
            dataset.transactions = dataset.transactions.subList(emptyTransactionCount, dataset.transactions.size())
        timeSort = System.currentTimeMillis() - timeStartSorting
        if DEBUG:
            print("===== Database without unpromising items and sorted by TWU increasing order === ")
            print(str(dataset))
        useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(dataset)
        itemsToExplore = []
        if activateSubtreeUtilityPruning:
            for item in itemsToKeep:
                if utilityBinArraySU[item] >= minUtil:
                    itemsToExplore.append(item)
        if DEBUG:
            print("===== List of promising items [utility value > minutility value] === ")
            print(itemsToKeep)
        if activateSubtreeUtilityPruning:
            backtrackingEFIM(dataset.getTransactions(), itemsToKeep, itemsToExplore, 0)
        else:
            backtrackingEFIM(dataset.getTransactions(), itemsToKeep, itemsToKeep, 0)
        endTimestamp = System.currentTimeMillis()
        if writer is not None:
            writer.close()
        MemoryLogger.getInstance().checkMemory()
        return highUtilityItemsets

    # class ComparatorAnonymousInnerClass(Comparator):
    class ComparatorAnonymousInnerClass():
        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance
        def compare(self, t1, t2):
            pos1 = t1.items.length - 1
            pos2 = t2.items.length - 1
            if t1.items.length < t2.items.length:
                while pos1 >=0:
                    subtraction = t2.items[pos2] - t1.items[pos1]
                    if subtraction !=0:
                        return subtraction
                    pos1 -= 1
                    pos2 -= 1
                return -1
            elif t1.items.length > t2.items.length:
                while pos2 >=0:
                    subtraction = t2.items[pos2] - t1.items[pos1]
                    if subtraction !=0:
                        return subtraction
                    pos1 -= 1
                    pos2 -= 1
                return 1
            else:
                while pos2 >=0:
                    subtraction = t2.items[pos2] - t1.items[pos1]
                    if subtraction !=0:
                        return subtraction
                    pos1 -= 1
                    pos2 -= 1
                return 0
    @staticmethod
    def insertionSort(items, utilityBinArrayTWU):
        j = 1
        while j< len(items):
            itemJ = items[j]
            i = j - 1
            itemI = items[i]
            comparison = utilityBinArrayTWU[itemI] - utilityBinArrayTWU[itemJ]
            if comparison == 0:
                comparison = itemI - itemJ
            while comparison > 0:
                items[i+1] = itemI
                i -= 1
                if i<0:
                    break
                itemI = items[i]
                comparison = utilityBinArrayTWU[itemI] - utilityBinArrayTWU[itemJ]
                if comparison == 0:
                    comparison = itemI - itemJ
            items[i+1] = itemJ
            j += 1
    def __backtrackingEFIM(self, transactionsOfP, itemsToKeep, itemsToExplore, prefixLength):
        candidateCount += len(itemsToExplore)
        j = 0
        while j < len(itemsToExplore):
            e = itemsToExplore[j]
            transactionsPe = []
            utilityPe = 0
            consecutiveMergeCount = 0
            previousTransaction = None
            timeFirstIntersection = System.currentTimeMillis()
            for transaction in transactionsOfP:
                transactionReadingCount += 1
                timeBinaryLocal = System.currentTimeMillis()
                positionE = -1
                low = transaction.offset
                high = transaction.items.length - 1
                while high >= low:
                    middle = (low + high) >> 1
                    if transaction.items[middle] < e:
                        low = middle + 1
                    elif transaction.items[middle] == e:
                        positionE = middle
                        break
                    else:
                        high = middle - 1
                timeBinarySearch += System.currentTimeMillis() - timeBinaryLocal
                if positionE > -1:
                    if transaction.getLastPosition() == positionE:
                        utilityPe += transaction.utilities[positionE] + transaction.prefixUtility
                    else:
                        if activateTransactionMerging and MAXIMUM_SIZE_MERGING >= (transaction.items.length - positionE):
                            projectedTransaction = Transaction(transaction, positionE)
                            utilityPe += projectedTransaction.prefixUtility
                            if previousTransaction is None:
                                previousTransaction = projectedTransaction
                            elif isEqualTo(projectedTransaction, previousTransaction):
                                mergeCount += 1
                                if consecutiveMergeCount == 0:
                                    itemsCount = previousTransaction.items.length - previousTransaction.offset
                                    items = [0 for _ in range(itemsCount)]
                                    System.arraycopy(previousTransaction.items, previousTransaction.offset, items, 0,itemsCount)
                                    utilities = [0 for _ in range(itemsCount)]
                                    System.arraycopy(previousTransaction.utilities, previousTransaction.offset,utilities, 0, itemsCount)
                                    positionPrevious = 0
                                    positionProjection = projectedTransaction.offset
                                    while positionPrevious < itemsCount:
                                        utilities[positionPrevious] += projectedTransaction.utilities[positionProjection]
                                        positionPrevious += 1
                                        positionProjection += 1
                                    previousTransaction.prefixUtility += projectedTransaction.prefixUtility
                                    sumUtilities = previousTransaction.prefixUtility
                                    previousTransaction = Transaction(items, utilities,previousTransaction.transactionUtility+ projectedTransaction.transactionUtility)
                                    previousTransaction.prefixUtility = sumUtilities
                                else:
                                    positionPrevious = 0
                                    positionProjected = projectedTransaction.offset
                                    itemsCount = previousTransaction.items.length
                                    while positionPrevious < itemsCount:
                                        previousTransaction.utilities[positionPrevious] += projectedTransaction.utilities[positionProjected]
                                        positionPrevious += 1
                                        positionProjected += 1
                                    previousTransaction.transactionUtility += projectedTransaction.transactionUtility
                                    previousTransaction.prefixUtility += projectedTransaction.prefixUtility
                                consecutiveMergeCount += 1
                            else:
                                transactionsPe.append(previousTransaction)
                                previousTransaction = projectedTransaction
                                consecutiveMergeCount = 0
                        else:
                            projectedTransaction = Transaction(transaction, positionE)
                            utilityPe += projectedTransaction.prefixUtility
                            transactionsPe.append(projectedTransaction)
                    transaction.offset = positionE
                else:
                    transaction.offset = low
            timeIntersections += (System.currentTimeMillis() - timeFirstIntersection)
            if previousTransaction is not None:
                transactionsPe.append(previousTransaction)
            temp[prefixLength] = newNamesToOldNames[e]
            if utilityPe >= minUtil:
                output(prefixLength, utilityPe)
            useUtilityBinArraysToCalculateUpperBounds(transactionsPe, j, itemsToKeep)
            initialTime = System.currentTimeMillis()
            newItemsToKeep = []
            newItemsToExplore = []
            k = j + 1
            while k < len(itemsToKeep):
                itemk = itemsToKeep[k]
                if utilityBinArraySU[itemk] >= minUtil:
                    if activateSubtreeUtilityPruning:
                        newItemsToExplore.append(itemk)
                    newItemsToKeep.append(itemk)
                elif utilityBinArrayLU[itemk] >= minUtil:
                    newItemsToKeep.append(itemk)
                k += 1
            timeIdentifyPromisingItems += (System.currentTimeMillis() - initialTime)
            if activateSubtreeUtilityPruning:
                self.__backtrackingEFIM(transactionsPe, newItemsToKeep, newItemsToExplore, prefixLength + 1)
            else:
                self.__backtrackingEFIM(transactionsPe, newItemsToKeep, newItemsToKeep, prefixLength + 1)
            j += 1
        MemoryLogger.getInstance().checkMemory()

    def __isEqualTo(self, t1, t2):
        length1 = t1.items.length - t1.offset
        length2 = t2.items.length - t2.offset
        if length1 != length2:
            return False
        position1 = t1.offset
        position2 = t2.offset
        while position1 < t1.items.length:
            if t1.items[position1] != t2.items[position2]:
                return False
            position1 += 1
            position2 += 1
        return True
    def useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset):
        utilityBinArrayLU = [0 for _ in range(dataset.getMaxItem() + 1)]
        for transaction in dataset.getTransactions():
            for item in transaction.getItems():
                utilityBinArrayLU[item] += transaction.transactionUtility

    def useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self, dataset):
        sumSU = None
        for transaction in dataset.getTransactions():
            sumSU = 0
            for i in range(transaction.getItems().length - 1, -1, -1):
                item = transaction.getItems()[i]
                sumSU += transaction.getUtilities()[i]
                utilityBinArraySU[item] += sumSU

    def __useUtilityBinArraysToCalculateUpperBounds(self, transactionsPe, j, itemsToKeep):
        initialTime = System.currentTimeMillis()
        i = j + 1
        while i < len(itemsToKeep):
            item = itemsToKeep[i]
            utilityBinArraySU[item] = 0
            utilityBinArrayLU[item] = 0
            i += 1
        sumRemainingUtility = None
        for transaction in transactionsPe:
            transactionReadingCount += 1
            sumRemainingUtility = 0
            high = len(itemsToKeep) - 1
            i = transaction.getItems().length - 1
            while i >= transaction.offset:
                item = transaction.getItems()[i]
                contains = False
                low = 0
                while high >= low:
                    middle = (low + high) >> 1 
                    itemMiddle = itemsToKeep[middle]
                    if itemMiddle == item:
                        contains = True
                        break
                    elif itemMiddle < item:
                        low = middle + 1
                    else:
                        high = middle - 1
                if contains:
                    sumRemainingUtility += transaction.getUtilities()[i]
                    utilityBinArraySU[item] += sumRemainingUtility + transaction.prefixUtility
                    utilityBinArrayLU[item] += transaction.transactionUtility + transaction.prefixUtility
                i -= 1
        timeDatabaseReduction += (System.currentTimeMillis() - initialTime)
    
    def __output(self, tempPosition, utility):
        patternCount += 1
        if writer is None:
            copy = [0 for _ in range(tempPosition + 1)]
            System.arraycopy(temp, 0, copy, 0, tempPosition + 1)
            highUtilityItemsets.addItemset(Itemset(copy, utility), len(copy))
        else:
            buffer = StringBuffer()
            i = 0
            while i <= tempPosition:
                buffer.append(temp[i])
                if i != tempPosition:
                    buffer.append(' ')
                i += 1
            buffer.append(" #UTIL: ")
            buffer.append(utility)
            writer.write(str(buffer))
            writer.newLine()
    def printStats(self):
        print("========== EFIM v97 - STATS ============")
        print(" minUtil = " + minUtil)
        print(" High utility itemsets count: " + patternCount)
        print(" Total time ~: " + (endTimestamp - startTimestamp) + " ms")
        if DEBUG:
            print(" Transaction merge count ~: " + mergeCount)
            print(" Transaction read count ~: " + transactionReadingCount)

            print(" Time intersections ~: " + timeIntersections + " ms")
            print(" Time database reduction ~: " + timeDatabaseReduction + " ms")
            print(" Time promising items ~: " + timeIdentifyPromisingItems + " ms")
            print(" Time binary search ~: " + timeBinarySearch + " ms")
            print(" Time sort ~: " + timeSort + " ms")
        print(" Max memory:" + MemoryLogger.getInstance().getMaxMemory())
        print(" Candidate count : " + candidateCount)
        print("=====================================")