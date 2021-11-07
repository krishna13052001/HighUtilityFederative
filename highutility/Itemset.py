class Itemset(object):
    def _initialize_instance_fields(self):
        self.itemset = []
        self.utility = 0
    def getItems(self):
        return self.itemset
    def __init__(self):
        self._initialize_instance_fields()

        self.itemset = []
    def __init__(self, item):
        self._initialize_instance_fields()

        self.itemset = [item]
    def __init__(self, items):
        self._initialize_instance_fields()

        self.itemset = items
    def __init__(self, itemset, utility):
        self._initialize_instance_fields()

        self.itemset = [0 for _ in range(len(itemset))]
        i = 0
        for item in itemset:
            self.itemset[i] = int(item)
            i += 1
        self.utility = utility
    def __init__(self, itemset, utility):
        self._initialize_instance_fields()

        self.itemset = itemset
        self.utility = utility
    def getUtility(self):
        return self.utility
    def size(self):
        return len(self.itemset)
    def get(self, position):
        return self.itemset[position]
    def setUtility(self, utility):
        self.utility = utility
    def cloneItemSetMinusOneItem(self, itemToRemove):
        newItemset = [0 for _ in range(len(self.itemset) -1)]
        i =0
        j = 0
        while j < len(self.itemset):
            if self.itemset[j] != itemToRemove:
                newItemset[i] = self.itemset[j]
                i += 1
            j += 1
        return Itemset(newItemset)
    def toString(self):
        r = StringBuffer()
        i = 0
        while i< self.size():
            r.append(self.get(i))
            r.append(' ')
            i += 1
        return str(r)
