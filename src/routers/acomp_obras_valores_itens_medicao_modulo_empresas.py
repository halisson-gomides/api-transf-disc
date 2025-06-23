from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedAcompObrasValoresItensMedicaoModuloEmpresasResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

acomp_obras_valores_itens_medicao_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@acomp_obras_valores_itens_medicao_modulo_empresas_router.get(
    "/acomp-obras-valores-itens-medicao-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada dos valores dos itens de medição das obras (Módulo Empresas).",
    response_description="Lista Paginada dos valores dos itens de medição das obras (Módulo Empresas)",
    response_model=PaginatedAcompObrasValoresItensMedicaoModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_acomp_obras_valores_itens_medicao_modulo_empresas(
    id_submeta_vrpl: Optional[int] = Query(None, description='Identificador único da submeta', ge=1),
    id_contrato_medicao_acompanhamento_obra: Optional[int] = Query(None, description='Identificador único do contrato de medição', ge=1),
    valor_execucao_fisica_acumulada_total_acompanhamento_obra: Optional[float] = Query(None, description='Somatório do Valor Total Acumulado da Execução Física da Obra', ge=0),
    valor_execucao_fisica_acumulada_concedente_acompanhamento_obra: Optional[float] = Query(None, description='Somatório do Valor Acumulado da Execução Física por parte do Concedente da Obra', ge=0),
    valor_execucao_fisica_acumulada_convenente_acompanhamento_obra: Optional[float] = Query(None, description='Somatório do Valor Acumulado da Execução Física por parte do Convenente da Obra', ge=0),
    valor_execucao_fisica_acumulada_empresa_acompanhamento_obra: Optional[float] = Query(None, description='Somatório do Valor Acumulado da Execução Física por parte da Empresa da Obra', ge=0),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.AcompObrasValoresItensMedicaoModuloEmpresas).where(
            and_(
                models.AcompObrasValoresItensMedicaoModuloEmpresas.id_submeta_vrpl == id_submeta_vrpl if id_submeta_vrpl is not None else True,
                models.AcompObrasValoresItensMedicaoModuloEmpresas.id_contrato_medicao_acompanhamento_obra == id_contrato_medicao_acompanhamento_obra if id_contrato_medicao_acompanhamento_obra is not None else True,
                models.AcompObrasValoresItensMedicaoModuloEmpresas.valor_execucao_fisica_acumulada_total_acompanhamento_obra == valor_execucao_fisica_acumulada_total_acompanhamento_obra if valor_execucao_fisica_acumulada_total_acompanhamento_obra is not None else True,
                models.AcompObrasValoresItensMedicaoModuloEmpresas.valor_execucao_fisica_acumulada_concedente_acompanhamento_obra == valor_execucao_fisica_acumulada_concedente_acompanhamento_obra if valor_execucao_fisica_acumulada_concedente_acompanhamento_obra is not None else True,
                models.AcompObrasValoresItensMedicaoModuloEmpresas.valor_execucao_fisica_acumulada_convenente_acompanhamento_obra == valor_execucao_fisica_acumulada_convenente_acompanhamento_obra if valor_execucao_fisica_acumulada_convenente_acompanhamento_obra is not None else True,
                models.AcompObrasValoresItensMedicaoModuloEmpresas.valor_execucao_fisica_acumulada_empresa_acompanhamento_obra == valor_execucao_fisica_acumulada_empresa_acompanhamento_obra if valor_execucao_fisica_acumulada_empresa_acompanhamento_obra is not None else True,
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
