from collections import deque
from Etat import Etat
from Transition import Transition
from AAutomate import Automate
from Alphabet import Alphabet
from minimiseAutomate import minimiseAutomate
def afn_afd(afn):
    def etats_to_str(etats):
        return "_".join(sorted([str(e.idEtat) for e in etats]))

    etat_mapping = {}
    #afn = Automate()
   
    new_alphabets = afn.alphabet.copy()
    
    new_alphabets = [
        a if isinstance(a, Alphabet) else Alphabet(f"alpha_{a}", a)
        for a in new_alphabets
    ]

    etats = []
    initiaux = []
    finaux = []
    transitions = []

    file = deque()
    vus = set()

    initiaux_set = set(afn.initiaux)
    nom_init = etats_to_str(initiaux_set)
    etat_init = Etat(nom_init, nom_init, "initial")
    etat_mapping[nom_init] = etat_init
    etats.append(etat_init)
    initiaux.append(etat_init)
    file.append(initiaux_set)
    vus.add(nom_init)

    while file:
        etats_courants = file.popleft()
        nom_etat_courant = etats_to_str(etats_courants)
        etat_source = etat_mapping[nom_etat_courant]

        for alpha in new_alphabets:
            prochains_etats = set()

            alpha_symbol = next(iter(alpha.valAlphabet)) if isinstance(alpha, Alphabet) else alpha

            for etat in etats_courants:
                for t in afn.transitions:
                    # Handle t.alphabet as Alphabet object or string
                    t_symbol = (
                        next(iter(t.alphabet.valAlphabet))
                        if isinstance(t.alphabet, Alphabet)
                        else t.alphabet
                    )
                    if t.etatSource.idEtat == etat.idEtat and t_symbol == alpha_symbol:
                        prochains_etats.add(t.etatDestination)

            if not prochains_etats:
                continue

            nom_prochain = etats_to_str(prochains_etats)

            if nom_prochain not in vus:
                type_etat = "normal"
                if any(e in afn.finaux for e in prochains_etats):
                    type_etat = "final"

                nouvel_etat = Etat(nom_prochain, nom_prochain, type_etat)
                etat_mapping[nom_prochain] = nouvel_etat
                etats.append(nouvel_etat)
                if type_etat == "final":
                    finaux.append(nouvel_etat)
                file.append(prochains_etats)
                vus.add(nom_prochain)

            t = Transition(
                idTransition=f"{etat_source.labelEtat}_{alpha_symbol}_{nom_prochain}",
                etatSource=etat_source,
                etatDestination=etat_mapping[nom_prochain],
                alphabet=alpha
            )
            transitions.append(t)

    afd = Automate(
        alphabets=new_alphabets,
        etats=etats,
        initiaux=initiaux,
        finaux=finaux,
        transitions=transitions
    )

    return minimiseAutomate(afd)