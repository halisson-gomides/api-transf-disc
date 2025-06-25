from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedProjetoBasicoMetasModuloEmpresasResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

projeto_basico_metas_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@projeto_basico_metas_modulo_empresas_router.get(
    "/projeto-basico-metas-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Metas do Projeto Básico.",
    response_description="Lista Paginada de Metas do Projeto Básico",
    response_model=PaginatedProjetoBasicoMetasModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_projeto_basico_metas_modulo_empresas(
    id_meta_projeto_basico: Optional[int] = Query(None, description='Identificador único da meta - accfo', ge=1),
    id_qci_acffo: Optional[int] = Query(None, description='Identificador único do qci - accfo', ge=1),
    numero_meta_projeto_basico: Optional[int] = Query(None, description='Número da Meta', ge=1),
    descricao_meta_projeto_basico: Optional[str] = Query(None, description='Descrição da Meta'),
    nome_item_investimento_meta: Optional[str] = Query(None, description='Nome do Item de Investimento'),
    descricao_subitem_investimento_meta: Optional[str] = Query(None, description='Descrição do Subitem de Investimento'),
    quantidade_itens_meta_projeto_basico: Optional[float] = Query(None, description='Quantidade de itens da Meta'),
    unidade_item_investimento_meta: Optional[str] = Query(None, description='Código da unidade de fornecimento'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.ProjetoBasicoMetasModuloEmpresas).where(
            and_(
                models.ProjetoBasicoMetasModuloEmpresas.id_meta_projeto_basico == id_meta_projeto_basico if id_meta_projeto_basico is not None else True,
                models.ProjetoBasicoMetasModuloEmpresas.id_qci_acffo == id_qci_acffo if id_qci_acffo is not None else True,
                models.ProjetoBasicoMetasModuloEmpresas.numero_meta_projeto_basico == numero_meta_projeto_basico if numero_meta_projeto_basico is not None else True,
                models.ProjetoBasicoMetasModuloEmpresas.descricao_meta_projeto_basico.ilike(f"%{descricao_meta_projeto_basico}%") if descricao_meta_projeto_basico is not None else True,
                models.ProjetoBasicoMetasModuloEmpresas.nome_item_investimento_meta.ilike(f"%{nome_item_investimento_meta}%") if nome_item_investimento_meta is not None else True,
                models.ProjetoBasicoMetasModuloEmpresas.descricao_subitem_investimento_meta.ilike(f"%{descricao_subitem_investimento_meta}%") if descricao_subitem_investimento_meta is not None else True,
                models.ProjetoBasicoMetasModuloEmpresas.quantidade_itens_meta_projeto_basico == quantidade_itens_meta_projeto_basico if quantidade_itens_meta_projeto_basico is not None else True,
                models.ProjetoBasicoMetasModuloEmpresas.unidade_item_investimento_meta.ilike(f"%{unidade_item_investimento_meta}%") if unidade_item_investimento_meta is not None else True,
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
