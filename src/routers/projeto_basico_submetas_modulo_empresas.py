from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from datetime import date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedProjetoBasicoSubmetasModuloEmpresasResponse, PaginatedResponseTemplate
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

projeto_basico_submetas_modulo_empresas_router = APIRouter(tags=["Módulo Empresas"])
config = Settings()

@projeto_basico_submetas_modulo_empresas_router.get(
    "/projeto-basico-submetas-modulo-empresas",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Submetas do Projeto Básico.",
    response_description="Lista Paginada de Submetas do Projeto Básico",
    response_model=PaginatedProjetoBasicoSubmetasModuloEmpresasResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_projeto_basico_submetas_modulo_empresas(
    id_submeta_projeto_basico: Optional[int] = Query(None, description='Identificador único da submeta do projeto básico', ge=1),
    id_meta_projeto_basico: Optional[int] = Query(None, description='Identificador único da meta do projeto básico', ge=1),
    lote_submeta_projeto_basico: Optional[int] = Query(None, description='Número do Lote'),
    numero_submeta_projeto_basico: Optional[str] = Query(None, description='Número da Submeta'),
    descricao_submeta_projeto_basico: Optional[str] = Query(None, description='Descrição da Submeta'),
    situacao_submeta_projeto_basico: Optional[Literal["ACL","ANL","COM","EAN","ELA","EMH","HAS","HOM","REJ","SCC","SCP"]] = Query(None, description='Indicador da Situação'),
    valor_repasse_submeta_projeto_basico: Optional[float] = Query(None, description='Valor do Repasse'),
    valor_contrapartida_submeta_projeto_basico: Optional[float] = Query(None, description='Valor da Contrapartida'),
    valor_outros_submeta_projeto_basico: Optional[float] = Query(None, description='Valor Outros'),
    valor_total_submeta_projeto_basico: Optional[float] = Query(None, description='Valor Total'),
    data_previsao_inicio_obra_projeto_basico: Optional[str] = Query(None, description='Data de previsão do início da obra (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    quantidade_meses_duracao_obra_projeto_basico: Optional[int] = Query(None, description='Quantidade de meses de duração da obra'),
    database_obra_projeto_basico: Optional[str] = Query(None, description='Data-base da PO (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    sigla_localidade_obra_projeto_basico: Optional[Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']] = Query(None, description='Sigla da localidade'),
    obra_acompanhada_por_evento_projeto_basico: Optional[Literal["Não","Sim"]] = Query(None, description='Indicador de acompanhamento de eventos'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        filters = [
            models.ProjetoBasicoSubmetasModuloEmpresas.id_submeta_projeto_basico == id_submeta_projeto_basico if id_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.id_meta_projeto_basico == id_meta_projeto_basico if id_meta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.lote_submeta_projeto_basico == lote_submeta_projeto_basico if lote_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.numero_submeta_projeto_basico == numero_submeta_projeto_basico if numero_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.descricao_submeta_projeto_basico.ilike(f"%{descricao_submeta_projeto_basico}%") if descricao_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.situacao_submeta_projeto_basico == situacao_submeta_projeto_basico if situacao_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.valor_repasse_submeta_projeto_basico == valor_repasse_submeta_projeto_basico if valor_repasse_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.valor_contrapartida_submeta_projeto_basico == valor_contrapartida_submeta_projeto_basico if valor_contrapartida_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.valor_outros_submeta_projeto_basico == valor_outros_submeta_projeto_basico if valor_outros_submeta_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.valor_total_submeta_projeto_basico == valor_total_submeta_projeto_basico if valor_total_submeta_projeto_basico is not None else True,
            cast(models.ProjetoBasicoSubmetasModuloEmpresas.data_previsao_inicio_obra_projeto_basico, Date) == date.fromisoformat(data_previsao_inicio_obra_projeto_basico) if data_previsao_inicio_obra_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.quantidade_meses_duracao_obra_projeto_basico == quantidade_meses_duracao_obra_projeto_basico if quantidade_meses_duracao_obra_projeto_basico is not None else True,
            cast(models.ProjetoBasicoSubmetasModuloEmpresas.database_obra_projeto_basico, Date) == date.fromisoformat(database_obra_projeto_basico) if database_obra_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.sigla_localidade_obra_projeto_basico == sigla_localidade_obra_projeto_basico if sigla_localidade_obra_projeto_basico is not None else True,
            models.ProjetoBasicoSubmetasModuloEmpresas.obra_acompanhada_por_evento_projeto_basico == obra_acompanhada_por_evento_projeto_basico if obra_acompanhada_por_evento_projeto_basico is not None else True,
        ]
        query = select(models.ProjetoBasicoSubmetasModuloEmpresas).where(and_(*filters))
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
