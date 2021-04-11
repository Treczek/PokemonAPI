"""
Namespace for all custom exceptions
"""


class NonExistingPokemon(LookupError):
    pass


class InvalidPayload(AttributeError):
    pass
