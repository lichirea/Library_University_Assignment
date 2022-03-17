import pickle


class Files:

    def readpickle(self, file):
        f = open(file, "rb")
        return pickle.load(f)

    def writepickle(self, file, result):
        f = open(file, "wb")
        pickle.dump(result, f)

    def readtext(self, file):
        f = open(file, "r")
        return f.readlines()

    def writetext(self, file, result):
        f = open(file, "w")
        f.write(result)