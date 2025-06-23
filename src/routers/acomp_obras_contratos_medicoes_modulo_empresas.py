from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedAcompObrasContratosMedicoesModuloEmpresasResponse
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

acomp_obras_contratos_medicoes_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@acomp_obras_contratos_medicoes_modulo_empresas_router.get(
    "/acomp-obras-contratos-medicoes-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada dos dados de Acompanhamento de Obras, Contratos e Medições (Módulo Empresas).",
    response_description="Lista Paginada de Acompanhamento de Obras, Contratos e Medições (Módulo Empresas)",
    response_model=PaginatedAcompObrasContratosMedicoesModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_acomp_obras_contratos_medicoes_modulo_empresas(
    id_proposta: Optional[int] = Query(None, description='Identificador único da proposta', ge=1),
    id_contrato_medicao_acompanhamento_obra: Optional[int] = Query(None, description='Identificador único do contrato de medição', ge=1),
    id_medicao_acompanhamento_obra: Optional[int] = Query(None, description='Identificador único da medição', ge=1),
    data_inicio_obra_contrato_acompanhamento_obra: Optional[str] = Query(None, description='Data de Início da Obra do Contrato (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    cnpj_fornecedor_contrato_acompanhamento_obra: Optional[str] = Query(None, description='CNJP do Fornecedor'),
    numero_medicao_acompanhamento_obra: Optional[int] = Query(None, description='Número Sequencial da Medição', ge=1),
    nr_ultima_medicao_acompanhamento_obra: Optional[int] = Query(None, description='Número da última Medição', ge=1),
    situacao_medicao_acompanhamento_obra: Optional[str] = Query(None, description='Situação da Medição'),
    data_inicio_medicao_objeto_acompanhamento_obra: Optional[str] = Query(None, description='Data Inicial da Medição (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_fim_medicao_objeto_acompanhamento_obra: Optional[str] = Query(None, description='Data Final da Medição (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    qtd_dias_sem_medicao_acompanhamento_obra: Optional[int] = Query(None, description='Quantidade de Dias sem Medição no Acompanhamento da Obra', ge=1),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.AcompObrasContratosMedicoesModuloEmpresas).where(
            and_(
                models.AcompObrasContratosMedicoesModuloEmpresas.id_proposta == id_proposta if id_proposta is not None else True,
                models.AcompObrasContratosMedicoesModuloEmpresas.id_contrato_medicao_acompanhamento_obra == id_contrato_medicao_acompanhamento_obra if id_contrato_medicao_acompanhamento_obra is not None else True,
                models.AcompObrasContratosMedicoesModuloEmpresas.id_medicao_acompanhamento_obra == id_medicao_acompanhamento_obra if id_medicao_acompanhamento_obra is not None else True,
                cast(models.AcompObrasContratosMedicoesModuloEmpresas.data_inicio_obra_contrato_acompanhamento_obra, Date) == date.fromisoformat(data_inicio_obra_contrato_acompanhamento_obra) if data_inicio_obra_contrato_acompanhamento_obra is not None else True,
                models.AcompObrasContratosMedicoesModuloEmpresas.cnpj_fornecedor_contrato_acompanhamento_obra == cnpj_fornecedor_contrato_acompanhamento_obra if cnpj_fornecedor_contrato_acompanhamento_obra is not None else True,
                models.AcompObrasContratosMedicoesModuloEmpresas.numero_medicao_acompanhamento_obra == numero_medicao_acompanhamento_obra if numero_medicao_acompanhamento_obra is not None else True,
                models.AcompObrasContratosMedicoesModuloEmpresas.nr_ultima_medicao_acompanhamento_obra == nr_ultima_medicao_acompanhamento_obra if nr_ultima_medicao_acompanhamento_obra is not None else True,
                models.AcompObrasContratosMedicoesModuloEmpresas.situacao_medicao_acompanhamento_obra.ilike(f"%{situacao_medicao_acompanhamento_obra}%") if situacao_medicao_acompanhamento_obra is not None else True,
                cast(models.AcompObrasContratosMedicoesModuloEmpresas.data_inicio_medicao_objeto_acompanhamento_obra, Date) == date.fromisoformat(data_inicio_medicao_objeto_acompanhamento_obra) if data_inicio_medicao_objeto_acompanhamento_obra is not None else True,
                cast(models.AcompObrasContratosMedicoesModuloEmpresas.data_fim_medicao_objeto_acompanhamento_obra, Date) == date.fromisoformat(data_fim_medicao_objeto_acompanhamento_obra) if data_fim_medicao_objeto_acompanhamento_obra is not None else True,
                models.AcompObrasContratosMedicoesModuloEmpresas.qtd_dias_sem_medicao_acompanhamento_obra == qtd_dias_sem_medicao_acompanhamento_obra if qtd_dias_sem_medicao_acompanhamento_obra is not None else True,
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