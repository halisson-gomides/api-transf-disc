from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedInstContPropostaAioModuloEmpresasResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

inst_cont_proposta_aio_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@inst_cont_proposta_aio_modulo_empresas_router.get(
    "/inst-cont-proposta-aio-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Propostas AIO dos Instrumentos Contratuais (Módulo Empresas).",
    response_description="Lista Paginada das Propostas AIO dos Instrumentos Contratuais (Módulo Empresas)",
    response_model=PaginatedInstContPropostaAioModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_inst_cont_proposta_aio_modulo_empresas(
    id_proposta_instrumento_contratual: Optional[int] = Query(None, description='Identificador único da proposta do instrumento contratual', ge=1),
    id_proposta: Optional[int] = Query(None, description='Identificador único da proposta', ge=1),
    id_aio_instrumento_contratual: Optional[int] = Query(None, description='Identificador único do AIO', ge=1),
    situacao_aio_instrumento_contratual: Optional[Literal['Emitida', 'Não Emitida']] = Query(None, description='Situação da Emissão do AIO'),
    data_emissao_aio_instrumento_contratual: Optional[str] = Query(None, description='Data de Emissão do AIO', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.InstContPropostaAioModuloEmpresas).where(
            and_(
                models.InstContPropostaAioModuloEmpresas.id_proposta_instrumento_contratual == id_proposta_instrumento_contratual if id_proposta_instrumento_contratual is not None else True,
                models.InstContPropostaAioModuloEmpresas.id_proposta == id_proposta if id_proposta is not None else True,
                models.InstContPropostaAioModuloEmpresas.id_aio_instrumento_contratual == id_aio_instrumento_contratual if id_aio_instrumento_contratual is not None else True,
                models.InstContPropostaAioModuloEmpresas.situacao_aio_instrumento_contratual == situacao_aio_instrumento_contratual if situacao_aio_instrumento_contratual is not None else True,
                cast(models.InstContPropostaAioModuloEmpresas.data_emissao_aio_instrumento_contratual, Date) == date.fromisoformat(data_emissao_aio_instrumento_contratual) if data_emissao_aio_instrumento_contratual is not None else True,
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