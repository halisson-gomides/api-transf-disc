from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedSolicitacaoAjustePtResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

solicitacao_ajuste_pt_router = APIRouter(tags=["Outros"])
config = Settings()


@solicitacao_ajuste_pt_router.get("/solicitacao-ajuste-pt",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Solicitações de Ajuste do Plano de Trabalho.",
                response_description="Lista Paginada de Solicitações de Ajuste do Plano de Trabalho",
                response_model=PaginatedSolicitacaoAjustePtResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_solicitacao_ajuste_pt(
    id_ajuste_pt: Optional[int] = Query(None, description='Identificador único do ajuste do plano de trabalho', ge=1),
    id_proposta: Optional[int] = Query(None, description='Identificador da proposta associada ao ajuste', ge=1),
    nr_ajuste_pt: Optional[str] = Query(None, description='Número do ajuste do plano de trabalho no formato sequencial/ano'),
    data_solicitacao_ajuste_pt: Optional[str] = Query(None, description='Data da solicitação do ajuste do plano de trabalho (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    situacao_solicitacao_ajuste_pt: Optional[Literal['Ajustado (aguardando aprovação)','Ajustado e Aprovado', 'Autorizado (aguardando execução do ajuste)', 'Cadastrado', 'Em Análise (aguardando parecer)', 'Não Autorizado', 'Parecer Emitido']] = Query(None, description='Situação atual da solicitação de ajuste'),
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
        query = select(models.SolicitacaoAjustePt).where(
            and_(
                models.SolicitacaoAjustePt.id_ajuste_pt == id_ajuste_pt if id_ajuste_pt is not None else True,
                models.SolicitacaoAjustePt.id_proposta == id_proposta if id_proposta is not None else True,
                models.SolicitacaoAjustePt.nr_ajuste_pt == nr_ajuste_pt if nr_ajuste_pt is not None else True,
                cast(models.SolicitacaoAjustePt.data_solicitacao_ajuste_pt, Date) == date.fromisoformat(data_solicitacao_ajuste_pt) if data_solicitacao_ajuste_pt is not None else True,
                models.SolicitacaoAjustePt.situacao_solicitacao_ajuste_pt == situacao_solicitacao_ajuste_pt if situacao_solicitacao_ajuste_pt is not None else True,
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