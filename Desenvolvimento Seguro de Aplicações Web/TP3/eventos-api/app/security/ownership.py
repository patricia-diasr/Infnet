from typing import Callable, Optional, TypeVar
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.database.session import get_session
from app.models.usuario import Usuario
from app.security.auth import get_current_user


T = TypeVar("T")


def requer_dono(
    buscar_por_id: Callable[[Session, int], Optional[T]],
    campo_dono: str,
    descricao: str = "deste recurso",
    nome_recurso: str = "recurso",
):
    def dependencia(
        id: int,
        current_user: Usuario = Depends(get_current_user),
        session: Session = Depends(get_session),
    ) -> T:
        recurso = buscar_por_id(session, id)

        if recurso is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Recurso não encontrado: {nome_recurso}")

        if getattr(recurso, campo_dono) != current_user.username:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Você não é o dono {descricao}")

        return recurso

    return dependencia
