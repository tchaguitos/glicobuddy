from jose import JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from libs.unidade_de_trabalho import SqlAlchemyUnitOfWork
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.usuarios.adaptadores.jwt import GeradorDeToken
from contextos.usuarios.servicos.visualizadores import consultar_usuario_por_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/usuarios/login")


def retornar_usuario_logado(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar suas credenciais. Faça login novamente",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = GeradorDeToken.verificar_token(token=token)
        usuario_id: str = payload.get("id")

        if usuario_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    usuario_logado = consultar_usuario_por_id(
        usuario_id=IdUsuario(usuario_id),
        uow=SqlAlchemyUnitOfWork(),
    )

    if usuario_logado is None:
        raise credentials_exception

    return usuario_logado
