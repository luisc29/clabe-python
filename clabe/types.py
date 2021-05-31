from decimal import Decimal
from enum import Enum
from typing import ClassVar

from .errors import BankCodeValidationError, ClabeControlDigitValidationError
from .validations import BANK_NAMES, BANKS, compute_control_digit


def validate_digits(v: str) -> str:
    if not v.isdigit():
        raise TypeError('No digit')
    return v


class Clabe(str):
    """
    Based on: https://es.wikipedia.org/wiki/CLABE
    """

    strip_whitespace: ClassVar[bool] = True
    min_length: ClassVar[int] = 18
    max_length: ClassVar[int] = 18

    def __init__(self, clabe: str):
        self.bank_code_abm = clabe[:3]
        self.bank_code_banxico = BANKS[clabe[:3]]
        self.bank_name = BANK_NAMES[self.bank_code_banxico]

    @classmethod
    def __get_validators__(cls):
        yield cls.str_validator
        yield cls.constr_strip_whitespace
        yield cls.constr_length_validator
        yield cls.validate_digits
        yield cls.validate_bank_code_abm
        yield cls.validate_control_digit
        yield cls

    @classmethod
    def validate_bank_code_abm(cls, clabe: str) -> str:
        if clabe[:3] not in BANKS.keys():
            raise BankCodeValidationError
        return clabe

    @classmethod
    def validate_control_digit(cls, clabe: str) -> str:
        if clabe[-1] != compute_control_digit(clabe):
            raise ClabeControlDigitValidationError
        return clabe

    @property
    def bank_code(self):
        return self.bank_code_banxico

    @classmethod
    def validate_digits(cls, clabe: str) -> str:
        if not clabe.isdigit():
            raise TypeError('No digit')
        return clabe

    @classmethod
    def constr_length_validator(cls, clabe: str) -> str:
        clabe_len = len(clabe)

        if clabe_len > cls.max_length:
            raise AttributeError('Max length exceeded')

        if clabe_len < cls.min_length:
            raise AttributeError('Min length exceeded')

        return clabe

    @classmethod
    def str_validator(cls, clabe: str) -> str:
        if isinstance(clabe, str):
            if isinstance(clabe, Enum):
                return clabe.value
            else:
                return clabe
        elif isinstance(clabe, (float, int, Decimal)):
            # is there anything else we want to add here? If you think so, create an issue.
            return str(clabe)
        elif isinstance(clabe, (bytes, bytearray)):
            return clabe.decode()
        else:
            raise TypeError('Not a string')

    @classmethod
    def constr_strip_whitespace(cls, clabe: str) -> str:
        return clabe.strip()
