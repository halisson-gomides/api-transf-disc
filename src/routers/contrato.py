from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedContratoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

contrato_router = APIRouter(tags=["Licitação/Contrato"])
config = Settings()


@contrato_router.get("/contrato",
                    status_code=status.HTTP_200_OK,
                    description="Retorna uma Lista Paginada dos dados de Contrato.",
                    response_description="Lista Paginada de Contratos",
                    response_model=PaginatedContratoResponse
                    )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_contrato(
    id_licitacao: Optional[int] = Query(None, description='Identificador único da tabela licitação', gt=0),
    nr_contrato: Optional[int] = Query(None, description='Número do contrato, gerado sequencialmente pelo Sistema', gt=0),
    data_publicacao_contrato: Optional[str] = Query(None, description='Data da publicação do contrato'),
    data_assinatura_contrato: Optional[str] = Query(None, description='Data da assinatura do contrato', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_inicio_vigencia_contrato: Optional[str] = Query(None, description='Data de início de vigência do contrato', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_fim_vigencia_contrato: Optional[str] = Query(None, description='Data fim de vigência do contrato', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    objeto_contrato: Optional[str] = Query(None, description='Objeto do contrato'),
    tipo_aquisicao_contrato: Optional[Literal['SERVICO_DE_ENGENHARIA', 'SERVICO', 'MATERIAL_SERVICO', 'OBRAS', 'MATERIAL']] = Query(None, description='Tipo da aquisição envolvida no contrato'),
    valor_global_contrato: Optional[float] = Query(None, description='Valor global do contrato', gt=0),
    id_fornecedor_contrato: Optional[str] = Query(None, description='Identificação do fornecedor, podendo ser o número do CNPJ, número do CPF ou número da Inscrição Genérica'),
    nome_fornecedor_contrato: Optional[str] = Query(None, description='Razão Social do fornecedor'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]  # Exclude pagination and dbsession

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.Contrato).where(
            and_(
                models.Contrato.id_licitacao == id_licitacao if id_licitacao is not None else True,
                models.Contrato.nr_contrato == nr_contrato if nr_contrato is not None else True,
                models.Contrato.data_publicacao_contrato.ilike(f"%{data_publicacao_contrato}%") if data_publicacao_contrato is not None else True,
                cast(models.Contrato.data_assinatura_contrato, Date) == date.fromisoformat(data_assinatura_contrato) if data_assinatura_contrato is not None else True,
                cast(models.Contrato.data_inicio_vigencia_contrato, Date) == date.fromisoformat(data_inicio_vigencia_contrato) if data_inicio_vigencia_contrato is not None else True,
                cast(models.Contrato.data_fim_vigencia_contrato, Date) == date.fromisoformat(data_fim_vigencia_contrato) if data_fim_vigencia_contrato is not None else True,
                models.Contrato.objeto_contrato.ilike(f"%{objeto_contrato}%") if objeto_contrato is not None else True,
                models.Contrato.tipo_aquisicao_contrato == tipo_aquisicao_contrato if tipo_aquisicao_contrato is not None else True,
                models.Contrato.valor_global_contrato == valor_global_contrato if valor_global_contrato is not None else True,
                models.Contrato.id_fornecedor_contrato.ilike(f"%{id_fornecedor_contrato}%") if id_fornecedor_contrato is not None else True,
                models.Contrato.nome_fornecedor_contrato.ilike(f"%{nome_fornecedor_contrato}%") if nome_fornecedor_contrato is not None else True,
            )
        )
        # compiled_query_str = query.compile(
        #         dialect=dbsession.bind.dialect, 
        #         compile_kwargs={"literal_binds": True}
        #     )
        # print("--- SQL Query Gerada ---")
        # print(compiled_query_str)
        # print("------------------------")
        
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate,
                                          current_page=pagina,
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)