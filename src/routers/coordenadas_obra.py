from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedCoordenadasObraResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

coordenadas_obra_router = APIRouter(tags=["Outros"])
config = Settings()

@coordenadas_obra_router.get(
    "/coordenadas-obra",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Coordenadas das Obras.",
    response_description="Lista Paginada de Coordenadas das Obras",
    response_model=PaginatedCoordenadasObraResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_coordenadas_obra(
    id_proposta: Optional[int] = Query(None, description='Código do Sistema para uma Proposta', ge=1),
    nome_projeto_cadastro_obra: Optional[str] = Query(None, description='Nome do projeto cadastrado'),
    latitude_cadastro_obra: Optional[float] = Query(None, description='Latitude do local da obra'),
    longitude_cadastro_obra: Optional[float] = Query(None, description='Longitude do local da obra'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.CoordenadasObra).where(
            and_(
                models.CoordenadasObra.id_proposta == id_proposta if id_proposta is not None else True,
                models.CoordenadasObra.nome_projeto_cadastro_obra.ilike(f"%{nome_projeto_cadastro_obra}%") if nome_projeto_cadastro_obra is not None else True,
                models.CoordenadasObra.latitude_cadastro_obra == latitude_cadastro_obra if latitude_cadastro_obra is not None else True,
                models.CoordenadasObra.longitude_cadastro_obra == longitude_cadastro_obra if longitude_cadastro_obra is not None else True,
            )
        )
        result = await get_paginated_data(
            query=query,
            dbsession=dbsession,
            response_schema=PaginatedResponseTemplate,
            current_page=pagina,
            records_per_page=tamanho_da_pagina
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=config.ERROR_MESSAGE_INTERNAL)