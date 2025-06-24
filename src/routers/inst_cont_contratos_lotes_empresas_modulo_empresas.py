from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedInstContContratosLotesEmpresasModuloEmpresasResponse
from datetime import date
from typing import Any, Optional, Literal
from appconfig import Settings
from src.cache import cache

inst_cont_contratos_lotes_empresas_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@inst_cont_contratos_lotes_empresas_modulo_empresas_router.get(
    "/inst-cont-contratos-lotes-empresas-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada dos Contratos/Lotes dos Instrumentos Contratuais (Módulo Empresas).",
    response_description="Lista Paginada dos Contratos/Lotes dos Instrumentos Contratuais (Módulo Empresas)",
    response_model=PaginatedInstContContratosLotesEmpresasModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_inst_cont_contratos_lotes_empresas_modulo_empresas(
    id_contrato_instrumento_contratual: Optional[int] = Query(None, description='Identificador único do contrato', ge=1),
    id_proposta_instrumento_contratual: Optional[int] = Query(None, description='Identificador único da proposta do instrumento contratual', ge=1),
    id_lote_instrumento_contratual: Optional[int] = Query(None, description='Identificador único da tabela instrumentos_contratuais_VBL.lote', ge=1),
    numero_instrumento_contratual: Optional[str] = Query(None, description='Número do Instrumento Contratual'),
    situacao_instrumento_contratual: Optional[Literal['Concluído','Outros','Rascunho']] = Query(None, description='Situação do Instrumento Contratual'),
    data_assinatura_instrumento_contratual: Optional[str] = Query(None, description='Data de Assinatura do Instrumento Contratual', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_inicio_vigencia_instrumento_contratual: Optional[str] = Query(None, description='Data do Início da Vigência do Instrumento Contratual', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_fim_vigencia_instrumento_contratual: Optional[str] = Query(None, description='Data do Fim da Vigência do Instrumento Contratual', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    numero_lote_instrumento_contratual: Optional[int] = Query(None, description='Número do Lote do Instrumento Contratual', ge=1),
    razao_social_empresa_executora_instrumento_contratual: Optional[str] = Query(None, description='Razão Social do Executor do Instrumento Contratual'),
    tipo_identificacao_empresa_executora_instrumento_contratual: Optional[Literal['CNPJ','CPF','IG']] = Query(None, description='Tipo de Identificação (CPF, CNPJ, IG) do Executor do Instrumento Contratual'),
    identificacao_empresa_executora_instrumento_contratual: Optional[str] = Query(None, description='CPF ou CNPJ do Executor do Instrumento Contratual'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.InstContContratosLotesEmpresasModuloEmpresas).where(
            and_(
                models.InstContContratosLotesEmpresasModuloEmpresas.id_contrato_instrumento_contratual == id_contrato_instrumento_contratual if id_contrato_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.id_proposta_instrumento_contratual == id_proposta_instrumento_contratual if id_proposta_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.id_lote_instrumento_contratual == id_lote_instrumento_contratual if id_lote_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.numero_instrumento_contratual.ilike(f"%{numero_instrumento_contratual}%") if numero_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.situacao_instrumento_contratual == situacao_instrumento_contratual if situacao_instrumento_contratual is not None else True,
                cast(models.InstContContratosLotesEmpresasModuloEmpresas.data_assinatura_instrumento_contratual, Date) == date.fromisoformat(data_assinatura_instrumento_contratual) if data_assinatura_instrumento_contratual is not None else True,
                cast(models.InstContContratosLotesEmpresasModuloEmpresas.data_inicio_vigencia_instrumento_contratual, Date) == date.fromisoformat(data_inicio_vigencia_instrumento_contratual) if data_inicio_vigencia_instrumento_contratual is not None else True,
                cast(models.InstContContratosLotesEmpresasModuloEmpresas.data_fim_vigencia_instrumento_contratual, Date) == date.fromisoformat(data_fim_vigencia_instrumento_contratual) if data_fim_vigencia_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.numero_lote_instrumento_contratual == numero_lote_instrumento_contratual if numero_lote_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.razao_social_empresa_executora_instrumento_contratual.ilike(f"%{razao_social_empresa_executora_instrumento_contratual}%") if razao_social_empresa_executora_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.tipo_identificacao_empresa_executora_instrumento_contratual == tipo_identificacao_empresa_executora_instrumento_contratual if tipo_identificacao_empresa_executora_instrumento_contratual is not None else True,
                models.InstContContratosLotesEmpresasModuloEmpresas.identificacao_empresa_executora_instrumento_contratual.ilike(f"%{identificacao_empresa_executora_instrumento_contratual}%") if identificacao_empresa_executora_instrumento_contratual is not None else True,
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