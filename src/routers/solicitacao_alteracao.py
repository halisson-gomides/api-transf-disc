from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedSolicitacaoAlteracaoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

solicitacao_alteracao_router = APIRouter(tags=["Outros"])
config = Settings()

@solicitacao_alteracao_router.get(
    "/solicitacao-alteracao",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Solicitações de Alteração.",
    response_description="Lista Paginada de Solicitações de Alteração",
    response_model=PaginatedSolicitacaoAlteracaoResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_solicitacao_alteracao(
    id_solicitacao: Optional[int] = Query(None, description='Identificador único da tabela solicitacao_alteracao', ge=1),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Faixa reservada: 700000 a 999999', ge=1),
    nr_solicitacao: Optional[str] = Query(None, description='Número sequencial/ano da solicitação de alteração do Convenente para o Concedente, via termo aditivo'),
    situacao_solicitacao: Optional[Literal['Aceita', 'Cadastrada', 'Em Análise', 'Recusada']] = Query(None, description='Situação da solicitação de alteração'),
    objeto_solicitacao: Optional[str] = Query(None, description='Objeto de alteração da solicitação de alteração do Convenente para o Concedente, via termo aditivo'),
    data_solicitacao: Optional[str] = Query(None, description='Data da solicitação de alteração (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.SolicitacaoAlteracao).where(
            and_(
                models.SolicitacaoAlteracao.id_solicitacao == id_solicitacao if id_solicitacao is not None else True,
                models.SolicitacaoAlteracao.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.SolicitacaoAlteracao.nr_solicitacao == nr_solicitacao if nr_solicitacao is not None else True,
                models.SolicitacaoAlteracao.situacao_solicitacao == situacao_solicitacao if situacao_solicitacao is not None else True,
                models.SolicitacaoAlteracao.objeto_solicitacao.ilike(f"%{objeto_solicitacao}%") if objeto_solicitacao is not None else True,
                cast(models.SolicitacaoAlteracao.data_solicitacao, Date) == date.fromisoformat(data_solicitacao) if data_solicitacao is not None else True,
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