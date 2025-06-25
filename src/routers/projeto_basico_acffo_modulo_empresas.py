from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedProjetoBasicoAcffoModuloEmpresasResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

projeto_basico_acffo_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@projeto_basico_acffo_modulo_empresas_router.get(
    "/projeto-basico-acffo-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada dos Projetos Básicos ACFFO.",
    response_description="Lista Paginada de Projetos Básicos ACFFO",
    response_model=PaginatedProjetoBasicoAcffoModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_projeto_basico_acffo_modulo_empresas(
    id_acffo: Optional[int] = Query(None, description='Identificador único do acffo', ge=1),
    id_proposta: Optional[int] = Query(None, description='Identificador único da proposta', ge=1),
    ultima_versao_projeto_basico: Optional[int] = Query(None, description='Número da versão atual do Projeto Básico', ge=0),
    apelido_empreendimento_projeto_basico: Optional[str] = Query(None, description='Apelido do empreendimento'),
    situacao_projeto_basico: Optional[Literal["SCP","ACT","EMH","SCC","COM","ELA","ANL","REJ","HOM","HAS","EAN"]] = Query(None, description='Situação do Projeto Básico'),
    situacao_spa: Optional[Literal["Homologada","Não Homologada"]] = Query(None, description='Situação do SPA'),
    data_aceite_projeto_basico: Optional[str] = Query(None, description='Data do aceite do Projeto Básico (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.ProjetoBasicoAcffoModuloEmpresas).where(
            and_(
                models.ProjetoBasicoAcffoModuloEmpresas.id_acffo == id_acffo if id_acffo is not None else True,
                models.ProjetoBasicoAcffoModuloEmpresas.id_proposta == id_proposta if id_proposta is not None else True,
                models.ProjetoBasicoAcffoModuloEmpresas.ultima_versao_projeto_basico == ultima_versao_projeto_basico if ultima_versao_projeto_basico is not None else True,
                models.ProjetoBasicoAcffoModuloEmpresas.apelido_empreendimento_projeto_basico.ilike(f"%{apelido_empreendimento_projeto_basico}%") if apelido_empreendimento_projeto_basico is not None else True,
                models.ProjetoBasicoAcffoModuloEmpresas.situacao_projeto_basico == situacao_projeto_basico if situacao_projeto_basico is not None else True,
                models.ProjetoBasicoAcffoModuloEmpresas.situacao_spa == situacao_spa if situacao_spa is not None else True,
                cast(models.ProjetoBasicoAcffoModuloEmpresas.data_aceite_projeto_basico, Date) == date.fromisoformat(data_aceite_projeto_basico) if data_aceite_projeto_basico is not None else True,
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

