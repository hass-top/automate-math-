from deterministe import isDeterministe
from completeAutomate import completeAutomate
from Etat import Etat
from Transition import Transition
from Alphabet import Alphabet
from AAutomate import Automate

def minimiseAutomate(automate):
    if not isDeterministe(automate):
        return None
    automate = completeAutomate(automate)

    F = set(automate.listFinaux)
    Q = set(automate.listEtat)
    P = [F, Q - F]
    W = [F]

    while W:
        A = W.pop()
        for a in automate.alphabet:  # Use alphabet (set of symbols)
            X = set()
            for t in automate.listTransition:
                if next(iter(t.alphabet.valAlphabet)) == a and t.etatDestination in A:
                    X.add(t.etatSource)
            new_P = []
            for Y in P:
                inter = Y & X
                diff = Y - X
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

    classes = P
    etat_mapping = {}
    nouveaux_etats = []
    nouveaux_initiaux = []
    nouveaux_finaux = []
    nouveaux_transitions = []

    for i, classe in enumerate(classes):
        noms = sorted(e.idEtat for e in classe)
        id_ = "_".join(noms)
        e_type = "normal"
        if any(e in automate.listFinaux for e in classe):
            e_type = "final"
        if any(e in automate.listInitiaux for e in classe):
            e_type = "initial" if e_type == "normal" else "initial_final"
        e = Etat(id_, id_, e_type)
        nouveaux_etats.append(e)
        for et in classe:
            etat_mapping[et.idEtat] = e
        if "initial" in e_type:
            nouveaux_initiaux.append(e)
        if "final" in e_type:
            nouveaux_finaux.append(e)

    for c in classes:
        rep = list(c)[0]
        for a in automate.alphabet:
            for t in automate.listTransition:
                if t.etatSource.idEtat == rep.idEtat and next(iter(t.alphabet.valAlphabet)) == a:
                    src = etat_mapping[t.etatSource.idEtat]
                    dst = etat_mapping[t.etatDestination.idEtat]
                    id_tr = f"{src.idEtat}_{a}_{dst.idEtat}"
                    transition = Transition(id_tr, src, dst, Alphabet(f"A_{a}", a))
                    if transition not in nouveaux_transitions:
                        nouveaux_transitions.append(transition)
                    break

    return Automate(
        alphabets=[Alphabet(f"A_{s}", s) for s in automate.alphabet],
        etats=nouveaux_etats,
        initiaux=nouveaux_initiaux,
        finaux=nouveaux_finaux,
        transitions=nouveaux_transitions
    )