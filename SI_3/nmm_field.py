from nmm_pawn_types import NMM_Pawn


class NMM_Field:
    def __init__(self, coordinates: str, value=None):
        self.coordinates = coordinates
        self.value = value
        self.adjacent_fields = []

    def add_adjacent_fields(self, *fields):
        for field in fields:
            self.adjacent_fields.append(field)

    def get_empty_adjacent_fields(self):
        return [field for field in self.adjacent_fields if field.value is None]

    def __repr__(self):
        return f'{self.coordinates}'
