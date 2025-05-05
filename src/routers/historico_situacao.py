from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedHistoricoSituacaoResponse
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

historico_situacao_router = APIRouter(tags=["Instrumento"])
config = Settings()


@historico_situacao_router.get("/historico_situacao",
                             status_code=status.HTTP_200_OK,
                             description="Retorna uma Lista Paginada do Histórico de Situações das Propostas/Convênios.",
                             response_description="Lista Paginada do Histórico de Situações",
                             response_model=PaginatedHistoricoSituacaoResponse
                             )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_historico_situacao(
    id_proposta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Proposta', gt=0),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    dia_historico_sit: Optional[str] = Query(None, description='Data de entrada da situação no sistema (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    historico_sit: Optional[str] = Query(None, description='Situação histórica da Proposta/Convênio'),
    dias_historico_sit: Optional[int] = Query(None, description='Dias em que a Proposta/Convênio permaneceu na situação', gt=0),
    cod_historico_sit: Optional[int] = Query(None, description='Código da situação histórica da Proposta/Convênio'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]  # Exclude pagination and dbsession

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.HistoricoSituacao).where(
            and_(
                models.HistoricoSituacao.id_proposta == id_proposta if id_proposta is not None else True,
                models.HistoricoSituacao.nr_convenio == nr_convenio if nr_convenio is not None else True,
                cast(models.HistoricoSituacao.dia_historico_sit, Date) == date.fromisoformat(dia_historico_sit) if dia_historico_sit is not None else True,
                models.HistoricoSituacao.historico_sit.ilike(f"%{historico_sit}%") if historico_sit is not None else True,
                models.HistoricoSituacao.dias_historico_sit == dias_historico_sit if dias_historico_sit is not None else True,
                models.HistoricoSituacao.cod_historico_sit == cod_historico_sit if cod_historico_sit is not None else True,
            )
        ).order_by(models.HistoricoSituacao.dia_historico_sit)
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedHistoricoSituacaoResponse,
                                          current_page=pagina,
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)