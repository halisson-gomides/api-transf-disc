from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedPerguntaSelecaoPacResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

persp_router = APIRouter(tags=["PAC"])
config = Settings()


@persp_router.get("/pergunta_selecao_pac",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Perguntas Selecionadas do PAC.",
                response_description="Lista Paginada de Perguntas Selecionadas do PAC",
                response_model=PaginatedPerguntaSelecaoPacResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_pergunta_selecao_pac(
    id_pergunta_selecao_pac: Optional[int] = Query(None, description='Identificador único da pergunta do programa Novo PAC', gt=0),
    id_programa: Optional[int] = Query(None, description='Código Sequencial do Sistema para um Programa', gt=0),
    pergunta_selecao_pac: Optional[str] = Query(None, description='Campo para definição da pergunta do programa Novo PAC'),
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
        query = select(models.PerguntaSelecaoPac).where(
            and_(
                models.PerguntaSelecaoPac.id_pergunta_selecao_pac == id_pergunta_selecao_pac if id_pergunta_selecao_pac is not None else True,
                models.PerguntaSelecaoPac.id_programa == id_programa if id_programa is not None else True,
                models.PerguntaSelecaoPac.pergunta_selecao_pac.ilike(f"%{pergunta_selecao_pac}%") if pergunta_selecao_pac is not None else True,
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
