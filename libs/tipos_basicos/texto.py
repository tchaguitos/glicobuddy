from re import compile


class EmailInvalido(Exception):
    pass


class SenhaInvalida(Exception):
    pass


class NomeInvalido(Exception):
    pass


class Email(str):
    """"""

    def __new__(cls, email: str):

        if not isinstance(email, str):
            raise EmailInvalido("Você deve fornecer um e-mail válido")

        if len(email) <= 8:
            raise EmailInvalido("O e-mail fornecido não possui caracteres suficientes")

        padrao_de_email = compile(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")
        email_eh_valido = padrao_de_email.match(email)

        if not email_eh_valido:
            raise EmailInvalido("Você deve fornecer um e-mail válido")

        return super().__new__(cls, email)


class Senha(str):
    """"""

    def __new__(cls, senha: str):
        if len(senha) < 6:
            raise SenhaInvalida("A senha não possui caracteres suficientes")

        return super().__new__(cls, senha)


class Nome(str):
    """"""

    def __new__(cls, nome: str):
        if len(nome) <= 7:
            raise NomeInvalido("O nome não possui caracteres suficientes")

        return super().__new__(cls, nome)
