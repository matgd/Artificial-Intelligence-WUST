class FutoshikiField:
    def __init__(self, value=0, domain=None):
        """
        Constructor.
        :param max_value: N, max value in domain
        :param value: Value of field, if empty then 0
        """
        self.value = value

        self.top_constraint = None
        self.bottom_constraint = None
        self.right_constraint = None
        self.left_constraint = None

    def assign_constraint(self, direction: str, type: str, field: 'FutoshikiField'):
        """
        Assign constraint to field.
        :param direction: 'TOP'/'BOTTOM'/'LEFT'/'RIGHT'
        :param type: 'GT'/'LT' - greater than / lesser than
        :param field: Another field
        :return: None
        """
        assert type == 'GT' or type == 'LT'

        if direction.upper() == 'TOP':
            self.top_constraint = (type, field)
        elif direction.upper() == 'BOTTOM':
            self.bottom_constraint = (type, field)
        elif direction.upper() == 'LEFT':
            self.left_constraint = (type, field)
        elif direction.upper() == 'RIGHT':
            self.right_constraint = (type, field)

    def has_constraints(self) -> bool:
        constraints = [self.top_constraint, self.bottom_constraint,
                       self.right_constraint, self.left_constraint]

        return not all(constraint is None for constraint in constraints)

    def __str__(self) -> str:
        return str(self.value)
