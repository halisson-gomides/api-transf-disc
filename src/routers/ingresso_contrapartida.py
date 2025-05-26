from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedIngressoContrapartidaResponse
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

ingresso_contrapartida_router = APIRouter(tags=["Desembolso"])
config = Settings()


@ingresso_contrapartida_router.get("/ingresso-contrapartida",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Ingressos de Contrapartida.",
                response_description="Lista Paginada de Ingressos de Contrapartida",
                response_model=PaginatedIngressoContrapartidaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_ingresso_contrapartida(
    nr_convenio: Optional[int] = Query(None, description='Número do Convênio'),
    dt_ingresso_contrapartida: Optional[date] = Query(None, description='Data da disponibilização do recurso por parte do Convenente'),
    vl_ingresso_contrapartida: Optional[float] = Query(None, description='Valor disponibilizado pelo Convenente para a conta do instrumento'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]    
    
    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)
    
    try:
        query = select(models.IngressoContrapartida).where(
            and_(
                models.IngressoContrapartida.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.IngressoContrapartida.dt_ingresso_contrapartida == dt_ingresso_contrapartida if dt_ingresso_contrapartida is not None else True,
                models.IngressoContrapartida.vl_ingresso_contrapartida == vl_ingresso_contrapartida if vl_ingresso_contrapartida is not None else True,
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)