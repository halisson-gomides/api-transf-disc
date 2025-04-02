from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedPlanoAplicacaoDetalhadoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

plapdet_router = APIRouter(tags=["Plano de Trabalho"])
config = Settings()


@plapdet_router.get("/plano_aplicacao_detalhado",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Plano de Aplicação Detalhado.",
                response_description="Lista Paginada de Planos de Aplicação Detalhado",
                response_model=PaginatedPlanoAplicacaoDetalhadoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_plano_aplicacao_detalhado(
    id_proposta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Proposta'),
    sigla: Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'] = Query(None, description='UF cadastrada referente a localidade do item'),
    municipio: Optional[str] = Query(None, description='Município cadastrado referente a localidade do item'),
    natureza_aquisicao: Optional[int] = Query(None, description='Código de natureza de aquisição', ge=1, le=3),
    descricao_item: Optional[str] = Query(None, description='Descrição do Item'),
    cep_item: Optional[str] = Query(None, description='CEP cadastrado referente a localidade do item'),
    endereco_item: Optional[str] = Query(None, description='Endereço cadastrado referente a localidade do item'),
    tipo_despesa_item: Literal['SERVICO', 'BEM', 'OUTROS', 'TRIBUTO', 'OBRA', 'DESPESA_ADMINISTRATIVA'] = Query(None, description='Tipo da Despesa'),
    natureza_despesa: Optional[str] = Query(None, description='Natureza da Despesa referente ao item'),
    sit_item: Literal['APROVADO','EM_COMPLEMENTACAO', ''] = Query(None, description='Situação atual do Item'),
    cod_natureza_despesa: Optional[str] = Query(None, description='Código da natureza da despesa'),
    qtd_item: Optional[int] = Query(None, description='Quantidade de Itens'),
    valor_unitario_item: Optional[float] = Query(None, description='Valor unitário do item', ge=0),
    valor_total_item: Optional[float] = Query(None, description='Valor total do item', ge=0),
    id_item_pad: Optional[int] = Query(None, description='Identificador único do item do plano de aplicação'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]    
    
    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)
    
    try:
        query = select(models.PlanoAplicacaoDetalhado).where(
            and_(
                models.PlanoAplicacaoDetalhado.id_proposta == id_proposta if id_proposta is not None else True,
                models.PlanoAplicacaoDetalhado.sigla == sigla if sigla is not None else True,
                models.PlanoAplicacaoDetalhado.municipio.ilike(f"%{municipio}%") if municipio is not None else True,
                models.PlanoAplicacaoDetalhado.natureza_aquisicao == natureza_aquisicao if natureza_aquisicao is not None else True,
                models.PlanoAplicacaoDetalhado.descricao_item.ilike(f"%{descricao_item}%") if descricao_item is not None else True,
                models.PlanoAplicacaoDetalhado.cep_item == cep_item if cep_item is not None else True,
                models.PlanoAplicacaoDetalhado.endereco_item.ilike(f"%{endereco_item}%") if endereco_item is not None else True,
                models.PlanoAplicacaoDetalhado.tipo_despesa_item == tipo_despesa_item if tipo_despesa_item is not None else True,
                models.PlanoAplicacaoDetalhado.natureza_despesa == natureza_despesa if natureza_despesa is not None else True,
                models.PlanoAplicacaoDetalhado.sit_item == sit_item if sit_item is not None else True,
                models.PlanoAplicacaoDetalhado.cod_natureza_despesa == cod_natureza_despesa if cod_natureza_despesa is not None else True,
                models.PlanoAplicacaoDetalhado.qtd_item == qtd_item if qtd_item is not None else True,
                models.PlanoAplicacaoDetalhado.valor_unitario_item == valor_unitario_item if valor_unitario_item is not None else True,
                models.PlanoAplicacaoDetalhado.valor_total_item == valor_total_item if valor_total_item is not None else True,
                models.PlanoAplicacaoDetalhado.id_item_pad == id_item_pad if id_item_pad is not None else True,
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)