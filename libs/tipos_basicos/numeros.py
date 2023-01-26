class ValorDeGlicemiaInvalido(Exception):
    pass


class ValorDeGlicemia(int):
    """"""

    def __new__(cls, valor: int):
        if not isinstance(valor, int):
            raise ValorDeGlicemiaInvalido(
                "Você deve fornecer um valor de glicemia válido"
            )

        if not valor > 20:
            raise ValorDeGlicemiaInvalido(
                "O valor da glicemia deve ser superior a 20mg/dl"
            )

        return super().__new__(cls, valor)
