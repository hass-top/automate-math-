import Alphabet 
class Transition:
    def __init__(self, idTransition, etatSource, etatDestination, alphabet):
        self.idTransition = idTransition
        self.etatSource = etatSource
        self.etatDestination = etatDestination
        self.alphabet = alphabet

    def __repr__(self):
        return f"Transition({self.etatSource.idEtat}, {self.alphabet.valAlphabet}, {self.etatDestination.idEtat})"

    def to_dict(self):
        return {
            'id': self.idTransition,
            'src': self.etatSource.idEtat,
            'symb': list(self.alphabet.valAlphabet)[0],
            'dst': self.etatDestination.idEtat
        }
    def next(self,lettre : str):
        assert len(lettre) == 1, "impossible de tester deux lettre à la fois"
        if lettre in self.alphabet.valAlphabet:
            return self.etatDestination
        else:
            return False
    def sameAs(self,another):
        return self.etatSource.labelEtat == another.etatSource.labelEtat and self.alphabet.valAlphabet == another.alphabet.valAlphabet and self.etatDestination.labelEtat == another.etatDestination.labelEtat