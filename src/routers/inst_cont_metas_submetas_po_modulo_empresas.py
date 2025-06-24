from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedInstContMetasSubmetasPoModuloEmpresasResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

inst_cont_metas_submetas_po_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@inst_cont_metas_submetas_po_modulo_empresas_router.get(
    "/inst-cont-metas-submetas-po-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Metas, Submetas e POs do Módulo Empresas.",
    response_description="Lista Paginada de Metas, Submetas e POs do Módulo Empresas",
    response_model=PaginatedInstContMetasSubmetasPoModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_inst_cont_metas_submetas_po_modulo_empresas(
    id_meta_instrumento_contratual: Optional[int] = Query(None, description='Identificador único da meta do instrumento contratual', ge=1),
    id_submeta_instrumento_contratual: Optional[int] = Query(None, description='Identificador único da submeta do instrumento contratual', ge=1),
    id_po_instrumento_contratual: Optional[int] = Query(None, description='Identificador único do PO do instrumento contratual', ge=1),
    id_proposta_instrumento_contratual: Optional[int] = Query(None, description='Identificador único da proposta do instrumento contratual', ge=1),
    id_lote_instrumento_contratual: Optional[int] = Query(None, description='Identificador único do lote do instrumento contratual', ge=1),
    numero_meta_instrumento_contratual: Optional[int] = Query(None, description='Número da Meta do Instrumento Contratual', ge=1),
    descricao_meta_instrumento_contratual: Optional[str] = Query(None, description='Descrição da Meta do Instrumento Contratual'),
    numero_submeta_instrumento_contratual: Optional[str] = Query(None, description='Número da Submeta do Instrumento Contratual'),
    descricao_submeta_instrumento_contratual: Optional[str] = Query(None, description='Descrição da Submeta do Instrumento Contratual'),
    situacao_submeta_instrumento_contratual: Optional[Literal['AAI','ACT']] = Query(None, description='Situação da Submeta do Instrumento Contratual'),
    valor_total_licitado_instrumento_contratual: Optional[float] = Query(None, description='Valor Total Licitado do Instrumento Contratual', ge=0),
    data_previsao_inicio_obra_instrumento_contratual: Optional[str] = Query(None, description='Data de Previsão do Início da Obra do Instrumento Contratual (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    database_po_vrpl_instrumento_contratual: Optional[str] = Query(None, description='Data-base do Instrumento Contratual (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    sigla_localidade_po_instrumento_contratual: Optional[Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']] = Query(None, description='Sigla da Localidade do Instrumento Contratual'),
    acompanhado_por_evento_po_instrumento_contratual: Optional[int] = Query(None, description='Indicador se o PO é acompanhado por eventos no Instrumento Contratual', ge=0, le=1),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.InstContMetasSubmetasPoModuloEmpresas).where(
            and_(
                models.InstContMetasSubmetasPoModuloEmpresas.id_meta_instrumento_contratual == id_meta_instrumento_contratual if id_meta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.id_submeta_instrumento_contratual == id_submeta_instrumento_contratual if id_submeta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.id_po_instrumento_contratual == id_po_instrumento_contratual if id_po_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.id_proposta_instrumento_contratual == id_proposta_instrumento_contratual if id_proposta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.id_lote_instrumento_contratual == id_lote_instrumento_contratual if id_lote_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.numero_meta_instrumento_contratual == numero_meta_instrumento_contratual if numero_meta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.descricao_meta_instrumento_contratual.ilike(f"%{descricao_meta_instrumento_contratual}%") if descricao_meta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.numero_submeta_instrumento_contratual == numero_submeta_instrumento_contratual if numero_submeta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.descricao_submeta_instrumento_contratual.ilike(f"%{descricao_submeta_instrumento_contratual}%") if descricao_submeta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.situacao_submeta_instrumento_contratual == situacao_submeta_instrumento_contratual if situacao_submeta_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.valor_total_licitado_instrumento_contratual == valor_total_licitado_instrumento_contratual if valor_total_licitado_instrumento_contratual is not None else True,
                cast(models.InstContMetasSubmetasPoModuloEmpresas.data_previsao_inicio_obra_instrumento_contratual, Date) == date.fromisoformat(data_previsao_inicio_obra_instrumento_contratual) if data_previsao_inicio_obra_instrumento_contratual is not None else True,
                cast(models.InstContMetasSubmetasPoModuloEmpresas.database_po_vrpl_instrumento_contratual, Date) == date.fromisoformat(database_po_vrpl_instrumento_contratual) if database_po_vrpl_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.sigla_localidade_po_instrumento_contratual == sigla_localidade_po_instrumento_contratual if sigla_localidade_po_instrumento_contratual is not None else True,
                models.InstContMetasSubmetasPoModuloEmpresas.acompanhado_por_evento_po_instrumento_contratual == acompanhado_por_evento_po_instrumento_contratual if acompanhado_por_evento_po_instrumento_contratual is not None else True,
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