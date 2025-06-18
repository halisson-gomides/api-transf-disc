from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedResumoFisicoFinanceiroResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

resumo_fisico_financeiro_router = APIRouter(tags=["Outros"])
config = Settings()


@resumo_fisico_financeiro_router.get("/resumo-fisico-financeiro",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Resumo Físico e Financeiro.",
                response_description="Lista Paginada de Resumo Físico e Financeiro",
                response_model=PaginatedResumoFisicoFinanceiroResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_resumo_fisico_financeiro(
    id_proposta: Optional[int] = Query(None, description='Código da Proposta'),
    valor_total_resumo_fisico_financeiro: Optional[float] = Query(None, description='Valor Total do Resumo Físico e Financeiro', ge=0),
    valor_realizado_resumo_fisico_financeiro: Optional[float] = Query(None, description='Valor Realizado do Resumo Físico e Financeiro', ge=0),
    percentual_execucao_resumo_fisico_financeiro: Optional[float] = Query(None, description='Percentual de Execução do Resumo Físico e Financeiro', ge=0, le=100),
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
        query = select(models.ResumoFisicoFinanceiro).where(
            and_(
                models.ResumoFisicoFinanceiro.id_proposta == id_proposta if id_proposta is not None else True,
                models.ResumoFisicoFinanceiro.valor_total_resumo_fisico_financeiro == valor_total_resumo_fisico_financeiro if valor_total_resumo_fisico_financeiro is not None else True,
                models.ResumoFisicoFinanceiro.valor_realizado_resumo_fisico_financeiro == valor_realizado_resumo_fisico_financeiro if valor_realizado_resumo_fisico_financeiro is not None else True,
                models.ResumoFisicoFinanceiro.percentual_execucao_resumo_fisico_financeiro == percentual_execucao_resumo_fisico_financeiro if percentual_execucao_resumo_fisico_financeiro is not None else True,
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
