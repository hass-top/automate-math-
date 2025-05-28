class Alphabet: 
    def __init__(self, idAlphabet, valAlphabet):
        self.idAlphabet = idAlphabet
        self.valAlphabet = {valAlphabet} if isinstance(valAlphabet, str) else set(valAlphabet)

    def __repr__(self):
        return f"Alphabet({self.valAlphabet})"
    def getStr(self):
        for alpha in self.valAlphabet:
            return alpha