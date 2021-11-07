class MemoryLogger(object):
    # __instance = MemoryLogger()
    def __init__(self):
        self.__maxMemory = 0
    @staticmethod
    def getInstance(self):
        return self
    def getMaxMemory(self):
        return self.__maxMemory

    def reset(self):
        self.__maxMemory = 0

    def checkMemory(self):
        currentMemory = (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / 1024 / 1024
        if currentMemory > self.__maxMemory:
            self.__maxMemory = currentMemory