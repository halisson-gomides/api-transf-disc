from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedHistoricoProjetoBasicoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

historico_projeto_basico_router = APIRouter(tags=["Outros"])
config = Settings()


@historico_projeto_basico_router.get("/historico-projeto-basico",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Histórico de Projeto Básico.",
                response_description="Lista Paginada de Histórico de Projeto Básico",
                response_model=PaginatedHistoricoProjetoBasicoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_historico_projeto_basico(
    id_proposta: Optional[int] = Query(None, description='Código da Proposta'),
    data_hist_pb_tr: Optional[str] = Query(None, description='Data de registro (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    situacao_hist_pb_tr: Optional[Literal['Aceito / Fase de Análise', 'Complementação Solicitada', 'Em Análise', 'Em Elaboracao', 'Em Complementacao', 'Enviada para Análise', 'Homologada', 'Rejeitada']] = Query(None, description='Situação do acompanhamento'),
    evento_hist_pb_tr: Optional[str] = Query(None, description='Indicador do Evento'),
    versao_doc_pb_tr: Optional[int] = Query(None, description='Número da Versão usada no sistema de versionamento', ge=0),
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
        query = select(models.HistoricoProjetoBasico).where(
            and_(
                models.HistoricoProjetoBasico.id_proposta == id_proposta if id_proposta is not None else True,
                cast(models.HistoricoProjetoBasico.data_hist_pb_tr, Date) == date.fromisoformat(data_hist_pb_tr) if data_hist_pb_tr is not None else True,
                models.HistoricoProjetoBasico.situacao_hist_pb_tr == situacao_hist_pb_tr if situacao_hist_pb_tr is not None else True,
                models.HistoricoProjetoBasico.evento_hist_pb_tr.ilike(f"%{evento_hist_pb_tr}%") if evento_hist_pb_tr is not None else True,
                models.HistoricoProjetoBasico.versao_doc_pb_tr == versao_doc_pb_tr if versao_doc_pb_tr is not None else True,
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