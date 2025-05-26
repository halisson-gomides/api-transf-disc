from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedCronogramaDesembolsoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

crono_router = APIRouter(tags=["Desembolso"])
config = Settings()


@crono_router.get("/cronograma_desembolso",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Cronograma de Desembolso.",
                response_description="Lista Paginada de Cronograma de Desembolso",
                response_model=PaginatedCronogramaDesembolsoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_cronograma_desembolso(
    id_proposta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Proposta', gt=0),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    nr_parcela_crono_desembolso: Optional[int] = Query(None, description='Número da Parcela do Desembolso', gt=0),
    mes_crono_desembolso: Optional[int] = Query(None, description='Mês do Desembolso', ge=1, le=12),
    ano_crono_desembolso: Optional[int] = Query(None, description='Ano do Desembolso', gt=0),
    tipo_resp_crono_desembolso: Optional[Literal['Concedente', 'Convenente', 'Rendimento de Aplicação']] = Query(None, description='Tipo do Responsável definido no Cronograma de Desembolsos.'),
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
        query = select(models.CronogramaDesembolso).where(
            and_(
                models.CronogramaDesembolso.id_proposta == id_proposta if id_proposta is not None else True,
                models.CronogramaDesembolso.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.CronogramaDesembolso.nr_parcela_crono_desembolso == nr_parcela_crono_desembolso if nr_parcela_crono_desembolso is not None else True,
                models.CronogramaDesembolso.mes_crono_desembolso == mes_crono_desembolso if mes_crono_desembolso is not None else True,
                models.CronogramaDesembolso.ano_crono_desembolso == ano_crono_desembolso if ano_crono_desembolso is not None else True,
                models.CronogramaDesembolso.tipo_resp_crono_desembolso.ilike(f"%{tipo_resp_crono_desembolso}%") if tipo_resp_crono_desembolso is not None else True,
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