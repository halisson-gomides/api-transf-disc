from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedProrrogaOficioResponse, PaginatedResponseTemplate
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

prorroga_oficio_router = APIRouter(tags=["Instrumento"])
config = Settings()


@prorroga_oficio_router.get("/prorroga_oficio",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada dos dados de Prorroga de Ofício.",
    response_description="Lista Paginada de Prorrogações de Ofício",
    response_model=PaginatedProrrogaOficioResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_prorroga_oficio(
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    nr_prorroga: Optional[str] = Query(None, description='Número do Prorroga de Ofício'),
    dt_inicio_prorroga: Optional[str] = Query(None, description='Data Início de Vigência do Prorroga de Ofício (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_fim_prorroga: Optional[str] = Query(None, description='Data Fim de Vigência do Prorroga de Ofício (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dias_prorroga: Optional[int] = Query(None, description='Dias de prorrogação', gt=0),
    dt_assinatura_prorroga: Optional[str] = Query(None, description='Data de assinatura do Prorroga de Ofício (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    sit_prorroga: Optional[Literal['DISPONIBILIZADA', 'PUBLICADA']] = Query(None, description='Situação atual do Prorroga de Ofício'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    # Exclude pagination params and dbsession from the check
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.ProrrogaOficio).where(
            and_(
                models.ProrrogaOficio.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.ProrrogaOficio.nr_prorroga.ilike(f"%{nr_prorroga}%") if nr_prorroga is not None else True,
                cast(models.ProrrogaOficio.dt_inicio_prorroga, Date) == date.fromisoformat(dt_inicio_prorroga) if dt_inicio_prorroga is not None else True,
                cast(models.ProrrogaOficio.dt_fim_prorroga, Date) == date.fromisoformat(dt_fim_prorroga) if dt_fim_prorroga is not None else True,
                models.ProrrogaOficio.dias_prorroga == dias_prorroga if dias_prorroga is not None else True,
                cast(models.ProrrogaOficio.dt_assinatura_prorroga, Date) == date.fromisoformat(dt_assinatura_prorroga) if dt_assinatura_prorroga is not None else True,
                models.ProrrogaOficio.sit_prorroga == sit_prorroga if sit_prorroga is not None else True,
            )
        )

        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate,
                                          current_page=pagina,
                                          records_per_page=tamanho_da_pagina)
        # result.data = [models.ProrrogaOficio.model_validate(item) for item in result.data]
        return result

    # except ValueError as ve: # Catch potential date parsing errors
    #      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"Formato de data inválido: {ve}. Utilize o formato AAAA-MM-DD.")
    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)