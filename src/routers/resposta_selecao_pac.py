from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedRespostaSelecaoPacResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

ressp_router = APIRouter(tags=["PAC"])
config = Settings()


@ressp_router.get("/resposta_selecao_pac",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Respostas Selecionadas do PAC.",
                response_description="Lista Paginada de Respostas Selecionadas do PAC",
                response_model=PaginatedRespostaSelecaoPacResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_resposta_selecao_pac(
    id_pergunta_selecao_pac: Optional[int] = Query(None, description='Identificador único da pergunta do programa Novo PAC'),
    id_proposta_selecao_pac: Optional[int] = Query(None, description='Identificador único da Proposta do Novo PAC'),
    resposta_selecao_pac: Optional[str] = Query(None, description='Resposta da pergunta da Proposta do Novo PAC'),
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
        query = select(models.RespostaSelecaoPac).where(
            and_(
                models.RespostaSelecaoPac.id_pergunta_selecao_pac == id_pergunta_selecao_pac if id_pergunta_selecao_pac is not None else True,
                models.RespostaSelecaoPac.id_proposta_selecao_pac == id_proposta_selecao_pac if id_proposta_selecao_pac is not None else True,
                models.RespostaSelecaoPac.resposta_selecao_pac.ilike(f"%{resposta_selecao_pac}%") if resposta_selecao_pac is not None else True,
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