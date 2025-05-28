def isDeterministe(automate):
    if len(automate.listInitiaux) != 1:
        return False

    transitions_dict = {}
    for transition in automate.listTransition:
        source_id = transition.etatSource.idEtat
        symbol = list(transition.alphabet.valAlphabet)[0]
        key = (source_id, symbol)
        if key in transitions_dict:
            return False
        transitions_dict[key] = transition.etatDestination.idEtat

    return True