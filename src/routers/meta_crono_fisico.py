from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedMetaCronoFisicoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

meta_crono_fisico_router = APIRouter(tags=["Plano de Trabalho"])
config = Settings()


@meta_crono_fisico_router.get("/meta_crono_fisico",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados do Cronograma Físico de Metas.",
                response_description="Lista Paginada de Metas do Cronograma Físico",
                response_model=PaginatedMetaCronoFisicoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_meta_crono_fisico(
    id_meta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Meta', gt=0),
    id_proposta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Proposta', gt=0),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    cod_programa: Optional[str] = Query(None, description='Chave que identifica o programa composta por: (Cód.Órgão+Ano+Cód.Sequencial do Sistema)'),
    nome_programa: Optional[str] = Query(None, description='Descrição do Programa de Governo'),
    nr_meta: Optional[str] = Query(None, description='Número da Meta gerada pelo Sistema'),
    tipo_meta: Literal['NORMAL','APLICAÇÃO'] = Query(None, description='Tipo da Meta'),
    desc_meta: Optional[str] = Query(None, description='Especificação da Meta do Cronograma Físico'),
    data_inicio_meta: Optional[str] = Query(None, description='Data de início da Meta', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_fim_meta: Optional[str] = Query(None, description='Data de término da Meta', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    uf_meta: Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'] = Query(None, description='UF cadastrada para a Meta'),
    municipio_meta: Optional[str] = Query(None, description='Município cadastrado para a Meta'),
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
        query = select(models.MetaCronoFisico).where(
            and_(
                models.MetaCronoFisico.id_meta == id_meta if id_meta is not None else True,
                models.MetaCronoFisico.id_proposta == id_proposta if id_proposta is not None else True,
                models.MetaCronoFisico.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.MetaCronoFisico.cod_programa.ilike(f"%{cod_programa}%") if cod_programa is not None else True,
                models.MetaCronoFisico.nome_programa.ilike(f"%{nome_programa}%") if nome_programa is not None else True,
                models.MetaCronoFisico.nr_meta.ilike(f"%{nr_meta}%") if nr_meta is not None else True,
                models.MetaCronoFisico.tipo_meta == tipo_meta if tipo_meta is not None else True,
                models.MetaCronoFisico.desc_meta.ilike(f"%{desc_meta}%") if desc_meta is not None else True,
                cast(models.MetaCronoFisico.data_inicio_meta, Date) == date.fromisoformat(data_inicio_meta) if data_inicio_meta is not None else True,
                cast(models.MetaCronoFisico.data_fim_meta, Date) == date.fromisoformat(data_fim_meta) if data_fim_meta is not None else True,
                models.MetaCronoFisico.uf_meta.ilike(f"%{uf_meta}%") if uf_meta is not None else True,
                models.MetaCronoFisico.municipio_meta.ilike(f"%{municipio_meta}%") if municipio_meta is not None else True,
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