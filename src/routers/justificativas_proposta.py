from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedJustificativasPropostaResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

jus_prop_router = APIRouter(tags=["Proposta"])
config = Settings()


@jus_prop_router.get("/justificativas_proposta",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Justificativas das Propostas.",
                response_description="Lista Paginada de Justificativas das Propostas",
                response_model=PaginatedJustificativasPropostaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_justificativas_proposta(
    id_proposta: Optional[int] = Query(None, description='Identificador único da Proposta'),
    caracterizacao_interesses_reci: Optional[str] = Query(None, description='CCaracterização dos interesses recíprocos da proposta'),
    publico_alvo: Optional[str] = Query(None, description='Público alvo da proposta'),
    problema_a_ser_resolvido: Optional[str] = Query(None, description='Problema a ser resolvido pela proposta'),
    resultados_esperados: Optional[str] = Query(None, description='Resultados esperados pela proposta'),
    relacao_proposta_objetivos_pro: Optional[str] = Query(None, description='Relação entre a proposta e os objetivos e diretrizes do programa'),
    capacidade_tecnica: Optional[str] = Query(None, description='Capacidade Técnica e Gerencial da proposta'),
    justificativa: Optional[str] = Query(None, description='Justificativa da solicitação da proposta'),
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
        query = select(models.JustificativasProposta).where(
            and_(
                models.JustificativasProposta.id_proposta == id_proposta if id_proposta is not None else True,
                models.JustificativasProposta.caracterizacao_interesses_reci.ilike(f"%{caracterizacao_interesses_reci}%") if caracterizacao_interesses_reci is not None else True,
                models.JustificativasProposta.publico_alvo.ilike(f"%{publico_alvo}%") if publico_alvo is not None else True,
                models.JustificativasProposta.problema_a_ser_resolvido.ilike(f"%{problema_a_ser_resolvido}%") if problema_a_ser_resolvido is not None else True,
                models.JustificativasProposta.resultados_esperados.ilike(f"%{resultados_esperados}%") if resultados_esperados is not None else True,
                models.JustificativasProposta.relacao_proposta_objetivos_pro.ilike(f"%{relacao_proposta_objetivos_pro}%") if relacao_proposta_objetivos_pro is not None else True,
                models.JustificativasProposta.capacidade_tecnica.ilike(f"%{capacidade_tecnica}%") if capacidade_tecnica is not None else True,
                models.JustificativasProposta.justificativa.ilike(f"%{justificativa}%") if justificativa is not None else True,
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
