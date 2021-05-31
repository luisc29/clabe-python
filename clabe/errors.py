class BankCodeValidationError(ValueError):
    code = 'clabe.bank_code'
    msg_template = 'código de banco no es válido'


class ClabeControlDigitValidationError(ValueError):
    code = 'clabe.control_digit'
    msg_template = 'clabe dígito de control no es válido'
