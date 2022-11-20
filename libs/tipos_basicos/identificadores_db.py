from typing import Union
from uuid import UUID, uuid4


class Id(UUID):
    """
    Representa um `Id` de objeto para persistência
    """

    def __init__(self, *args):

        if args:
            uuid_ou_string: bool = isinstance(args[0], Union[UUID, str])
            eh_uma_subclasse: bool = issubclass(self.__class__, Id)

            if not uuid_ou_string:
                raise ValueError(
                    f"Para instanciar um `Id` passe um uuid4() ou um uuid4() como string"
                )

            if uuid_ou_string and eh_uma_subclasse:
                novo_id = str(args[0])
        else:
            novo_id = str(uuid4())

        super().__init__(novo_id)

    @staticmethod
    def is_valid(uuid: Union[UUID, str]):

        if isinstance(uuid, UUID):
            return True

        try:
            uuid_gerado = UUID(uuid, version=4)
        except:
            return False

        return str(uuid_gerado) == uuid


class IdUsuario(Id):
    pass


class IdGlicemia(Id):
    pass
