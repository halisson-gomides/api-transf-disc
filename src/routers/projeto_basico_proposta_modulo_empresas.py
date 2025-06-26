from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedProjetoBasicoPropostaModuloEmpresasResponse, PaginatedResponseTemplate
from typing import Optional
from appconfig import Settings
from src.cache import cache

projeto_basico_proposta_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@projeto_basico_proposta_modulo_empresas_router.get(
    "/projeto-basico-proposta-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Propostas do Projeto Básico.",
    response_description="Lista Paginada de Propostas do Projeto Básico",
    response_model=PaginatedProjetoBasicoPropostaModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_projeto_basico_proposta_modulo_empresas(
    id_proposta_acffo: Optional[int] = Query(None, description='Identificador único do acffo da proposta', ge=1),
    id_proposta: Optional[int] = Query(None, description='Identificador único da proposta', ge=1),
    valor_global_proposta_projeto_basico: Optional[float] = Query(None, description='Valor Global da Proposta do Projeto Básico'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.ProjetoBasicoPropostaModuloEmpresas).where(
            and_(
                models.ProjetoBasicoPropostaModuloEmpresas.id_proposta_acffo == id_proposta_acffo if id_proposta_acffo is not None else True,
                models.ProjetoBasicoPropostaModuloEmpresas.id_proposta == id_proposta if id_proposta is not None else True,
                models.ProjetoBasicoPropostaModuloEmpresas.valor_global_proposta_projeto_basico == valor_global_proposta_projeto_basico if valor_global_proposta_projeto_basico is not None else True,
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

