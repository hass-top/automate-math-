from deterministe import isDeterministe
from isComplet import isComplet

def isMinimal(automate):
    if not isDeterministe(automate) or not isComplet(automate):
        return False

    P = [set(automate.listFinaux), set([e for e in automate.listEtat if e not in automate.listFinaux])]
    W = [set(automate.listFinaux)]

    while W:
        A = W.pop()
        for a in automate.alphabet:  # Use alphabet (set of symbols)
            X = set()
            for t in automate.listTransition:
                if next(iter(t.alphabet.valAlphabet)) == a and t.etatDestination in A:
                    X.add(t.etatSource)
            new_P = []
            for Y in P:
                inter = Y.intersection(X)
                diff = Y.difference(X)
                if inter and diff:
                    new_P.append(inter)
                    new_P.append(diff)
                    if Y in W:
                        W.remove(Y)
                        W.append(inter)
                        W.append(diff)
                    else:
                        if len(inter) <= len(diff):
                            W.append(inter)
                        else:
                            W.append(diff)
                else:
                    new_P.append(Y)
            P = new_P

    nb_classes = len(P)
    nb_etats = len(automate.listEtat)
    return nb_classes == nb_etats