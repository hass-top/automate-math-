class Etat:
    def __init__(self, idEtat, labelEtat, typeEtat):
        self.idEtat = idEtat
        self.labelEtat = labelEtat
        self.typeEtat = typeEtat

    def __repr__(self):
        return f"Etat({self.idEtat}, label={self.labelEtat}, type={self.typeEtat})"

    def to_dict(self):
        return {
            'id': self.idEtat,
            'label': self.labelEtat,
            'type': self.typeEtat
        }

    @staticmethod
    def from_dict(data):
        return Etat(data['id'], data['label'], data['type'])