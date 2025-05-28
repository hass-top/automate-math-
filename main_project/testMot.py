from AAutomate import Automate
from isComplet import isComplet
from deterministe import isDeterministe
from PyQt5.QtWidgets import QTextEdit
from Alphabet import Alphabet
from completeAutomate import completeAutomate
def testMot_automate(automate:Automate,mot:str, result_text:QTextEdit,alphabets:Alphabet):
    cursors = list()
    alphabets = [
        a if isinstance(a, Alphabet) else Alphabet(f"alpha_{a}", a)
        for a in alphabets
    ]
    auto = automate
    for cursor in auto.listInitiaux:
        cursors.append(cursor)
    associations = dict()
    for etat in auto.listEtat:
        for trans in auto.transitions:
            if trans.etatSource == etat:
                if etat in associations.keys():
                    associations[etat].append(trans)
                else:
                    associations[etat] = [trans]

    if not isComplet(auto):
        result_text.append("l'automate fourni est non complet !")
        return
    if not isDeterministe(auto):
        result_text.append("Attention: l'automate fourni n'est pas détérministe, le résultat peut être non cohérent")
    
    for lett in mot:
        for alph in alphabets:
            if (lett in alph.valAlphabet):
                break
        else:
            result_text.append("Erreur: une des lettres données n'existe pas dans l'alphabet")
            return
        
                    
        for i in range(len(cursors)):
            if cursors[i] == None:
                continue
            for trans in associations[cursors[i]]:
                d = trans.next(lett)
                if d:
                    cursors[i] = d
                    break
            else:
                cursors[i] = None
    for curs in cursors:
        if curs in auto.listFinaux:
            result_text.append(f"le mot '{mot}' est accépté par l'automate")
            return
    result_text.append(f"le mot '{mot}' est rejeté")