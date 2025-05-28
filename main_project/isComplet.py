import Transition
import AAutomate
def isComplet(automate : AAutomate.Automate):
    """
    etats_ids = [etat.idEtat for etat in automate.listEtat]
    alphabets = [a.valAlphabet for a in automate.listAlphabets]
    transitions = {}
    for t in automate.listTransition:
        key = (t.etatSource.idEtat, t.alphabet.valAlphabet)
        transitions[key] = t.etatDestination.idEtat
    for e in etats_ids:
        for s in alphabets:
            if (e, s) not in transitions:
                return False
    """
    etas = automate.listEtat.copy()
    trans = automate.listTransition.copy()

    for et in etas:
        for lett in automate.alphabet:
            for tran in trans:
                if lett in tran.alphabet.valAlphabet and tran.etatSource == et:
                    break
            else:
                return False
    return True