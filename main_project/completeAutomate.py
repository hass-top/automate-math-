from isComplet import isComplet
from Etat import Etat
from Transition import Transition
from Alphabet import Alphabet
from AAutomate import Automate

def completeAutomate(automate):
    if isComplet(automate):
        # Return a copy of the original if complete
        return Automate(
            alphabets=[Alphabet(f"A_{s}", s) for s in automate.alphabet],
            etats=automate.listEtat.copy(),
            initiaux=automate.listInitiaux.copy(),
            finaux=automate.listFinaux.copy(),
            transitions=automate.listTransition.copy()
        )

    # Create a new automaton copy
    new_automate = Automate(
        alphabets=[Alphabet(f"A_{s}", s) for s in automate.alphabet],
        etats=automate.listEtat.copy(),
        initiaux=automate.listInitiaux.copy(),
        finaux=automate.listFinaux.copy(),
        transitions=automate.listTransition.copy()
    )

    id_puits = "Puits"
    etat_puits = Etat(id_puits, id_puits, "normal")
    new_automate.ajouter_etat(etat_puits)

    existing_transitions = {(t.etatSource.idEtat, next(iter(t.alphabet.valAlphabet))) for t in new_automate.listTransition}

    for etat in new_automate.listEtat:
        for symb in new_automate.alphabet:
            a = Alphabet(f"A_{symb}", symb)
            key = (etat.idEtat, symb)
            if key not in existing_transitions:
                t = Transition(
                    idTransition=f"{etat.idEtat}_{symb}_Puits",
                    etatSource=etat,
                    etatDestination=etat_puits,
                    alphabet=a
                )
                new_automate.ajouter_transition(t)

    for symb in new_automate.alphabet:
        a = Alphabet(f"A_{symb}", symb)
        t = Transition(
            idTransition=f"Puits_{symb}_Puits",
            etatSource=etat_puits,
            etatDestination=etat_puits,
            alphabet=a
        )
        new_automate.ajouter_transition(t)

    return new_automate