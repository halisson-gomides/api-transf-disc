from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedEmendaResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

emenda_router = APIRouter(tags=["Emenda"])
config = Settings()


@emenda_router.get("/emenda",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Emendas.",
                response_description="Lista Paginada de Emendas Parlamentares",
                response_model=PaginatedEmendaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_emenda(
    id_proposta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Proposta'),
    qualif_proponente: Optional[str] = Query(None, description='Qualificação do proponente'),
    cod_programa_emenda: Optional[str] = Query(None, description='Chave que identifica o programa composta por: (Cód.Órgão+Ano+Cód.Sequencial do Sistema)'),
    nr_emenda: Optional[int] = Query(None, description='Número da Emenda Parlamentar'),
    nome_parlamentar: Optional[str] = Query(None, description='Nome do Parlamentar'),
    beneficiario_emenda: Optional[str] = Query(None, description='CNPJ do Proponente'),
    ind_impositivo: Optional[Literal['SIM', 'NÃO']] = Query(None, description='Indicativo de Orçamento Impositivo (Tipo Parlamentar igual a INDIVIDUAL + Ano de Cadastro da Proposta >= 2014)'),
    tipo_parlamentar: Optional[Literal['INDIVIDUAL', 'COMISSAO', 'BANCADA']] = Query(None, description='Tipo do Parlamentar'),
    valor_repasse_proposta_emenda: Optional[float] = Query(None, description='Valor da Emenda cadastrada na proposta', ge=0),
    valor_repasse_emenda: Optional[float] = Query(None, description='Valor da Emenda assinada', ge=0),
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
        query = select(models.Emenda).where(
            and_(
                models.Emenda.id_proposta == id_proposta if id_proposta is not None else True,
                models.Emenda.qualif_proponente.ilike(f"%{qualif_proponente}%") if qualif_proponente is not None else True,
                models.Emenda.cod_programa_emenda == cod_programa_emenda if cod_programa_emenda is not None else True,
                models.Emenda.nr_emenda == nr_emenda if nr_emenda is not None else True,
                models.Emenda.nome_parlamentar.ilike(f"%{nome_parlamentar}%") if nome_parlamentar is not None else True,
                models.Emenda.beneficiario_emenda == beneficiario_emenda if beneficiario_emenda is not None else True,
                models.Emenda.ind_impositivo == ind_impositivo if ind_impositivo is not None else True,
                models.Emenda.tipo_parlamentar == tipo_parlamentar if tipo_parlamentar is not None else True,
                models.Emenda.valor_repasse_proposta_emenda == valor_repasse_proposta_emenda if valor_repasse_proposta_emenda is not None else True,
                models.Emenda.valor_repasse_emenda == valor_repasse_emenda if valor_repasse_emenda is not None else True,
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