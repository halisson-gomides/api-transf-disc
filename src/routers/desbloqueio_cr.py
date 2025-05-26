from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedDesbloqueioCrResponse
from datetime import date, datetime
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

desbloqueio_cr_router = APIRouter(tags=["Desembolso"])
config = Settings()


@desbloqueio_cr_router.get("/desbloqueio-cr",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Desbloqueio de Contrato de Repasse.",
                response_description="Lista Paginada de Desbloqueios de CR",
                response_model=PaginatedDesbloqueioCrResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_desbloqueio_cr(
    nr_convenio: Optional[int] = Query(None, description='Número do Convênio'),
    nr_ob: Optional[str] = Query(None, description='Número da OB'),
    data_cadastro: Optional[str] = Query(None, description='Data de Cadastro', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_envio: Optional[str] = Query(None, description='Data de envio da solicitação de desbloqueio do recurso', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    tipo_recurso_desbloqueio: Optional[Literal["OB", "INGRESSO CONTRAPARTIDA", "RENDIMENTO APLICAÇÃO"]] = Query(None, description='Tipo do Recurso'),
    vl_total_desbloqueio: Optional[float] = Query(None, description='Valor total de desbloqueio para o Contrato de Repasse'),
    vl_desbloqueado: Optional[float] = Query(None, description='Valor desbloqueado para o Contrato de Repasse'),
    vl_bloqueado: Optional[float] = Query(None, description='Valor bloqueado para o Contrato de Repasse'),
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
        query = select(models.DesbloqueioCr).where(
            and_(
                models.DesbloqueioCr.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.DesbloqueioCr.nr_ob == nr_ob if nr_ob is not None else True,
                cast(models.DesbloqueioCr.data_cadastro, Date) == date.fromisoformat(data_cadastro) if data_cadastro is not None else True,
                cast(models.DesbloqueioCr.data_envio, Date) == date.fromisoformat(data_envio) if data_envio is not None else True,
                models.DesbloqueioCr.tipo_recurso_desbloqueio == tipo_recurso_desbloqueio if tipo_recurso_desbloqueio is not None else True,
                models.DesbloqueioCr.vl_total_desbloqueio == vl_total_desbloqueio if vl_total_desbloqueio is not None else True,
                models.DesbloqueioCr.vl_desbloqueado == vl_desbloqueado if vl_desbloqueado is not None else True,
                models.DesbloqueioCr.vl_bloqueado == vl_bloqueado if vl_bloqueado is not None else True,
            )
        ).order_by(models.DesbloqueioCr.data_cadastro)
        
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)