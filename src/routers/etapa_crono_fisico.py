from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedEtapaCronoFisicoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

etapa_crono_fisico_router = APIRouter(tags=["Plano de Trabalho"])
config = Settings()


@etapa_crono_fisico_router.get("/etapa_crono_fisico",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Cronograma Físico de Etapas.",
                response_description="Lista Paginada de Etapas do Cronograma Físico",
                response_model=PaginatedEtapaCronoFisicoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_etapa_crono_fisico(
    id_etapa: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Etapa', gt=0),
    id_meta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Meta', gt=0),
    nr_etapa: Optional[int] = Query(None, description='Número da Etapa gerada pelo Sistema', gt=0),
    desc_etapa: Optional[str] = Query(None, description='Especificação da etapa vinculada a meta do cronograma físico'),
    data_inicio_etapa: Optional[str] = Query(None, description='Data de início prevista para execução da etapa', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_fim_etapa: Optional[str] = Query(None, description='Data fim prevista para execução da etapa', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    uf_etapa: Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'] = Query(None, description='UF cadastrada para a Etapa'),
    municipio_etapa: Optional[str] = Query(None, description='Município cadastrado para a Etapa'),
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
        query = select(models.EtapaCronoFisico).where(
            and_(
                models.EtapaCronoFisico.id_etapa == id_etapa if id_etapa is not None else True,
                models.EtapaCronoFisico.id_meta == id_meta if id_meta is not None else True,
                models.EtapaCronoFisico.nr_etapa == nr_etapa if nr_etapa is not None else True,
                models.EtapaCronoFisico.desc_etapa.ilike(f"%{desc_etapa}%") if desc_etapa is not None else True,
                cast(models.EtapaCronoFisico.data_inicio_etapa, Date) == date.fromisoformat(data_inicio_etapa) if data_inicio_etapa is not None else True,
                cast(models.EtapaCronoFisico.data_fim_etapa, Date) == date.fromisoformat(data_fim_etapa) if data_fim_etapa is not None else True,
                models.EtapaCronoFisico.uf_etapa.ilike(f"%{uf_etapa}%") if uf_etapa is not None else True,
                models.EtapaCronoFisico.municipio_etapa.ilike(f"%{municipio_etapa}%") if municipio_etapa is not None else True,
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