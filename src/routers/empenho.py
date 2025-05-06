from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedEmpenhoResponse 
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

empenho_router = APIRouter(tags=["Empenho"])
config = Settings()


@empenho_router.get("/empenho", # Changed endpoint path
                    status_code=status.HTTP_200_OK,
                    description="Retorna uma Lista Paginada dos dados de Empenho.", 
                    response_description="Lista Paginada de Empenhos", 
                    response_model=PaginatedEmpenhoResponse 
                    )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_empenho( # Changed function name
    id_empenho: Optional[int] = Query(None, description='Identificador único gerado pelo Sistema para o Empenho', gt=0),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    nr_empenho: Optional[str] = Query(None, description='Número da Nota de Empenho'),
    tipo_nota: Optional[str] = Query(None, description='Código do Tipo de Empenho'),
    desc_tipo_nota: Optional[str] = Query(None, description='Descrição do Tipo de Empenho'),
    data_emissao: Optional[str] = Query(None, description='Data de emissão do Empenho (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    cod_situacao_empenho: Optional[str] = Query(None, description='Código da Situação atual do empenho'),
    desc_situacao_empenho: Optional[str] = Query(None, description='Descrição da Situação atual do empenho'),
    ug_emitente: Optional[str] = Query(None, description='Unidade Gestora Emitente'),
    ug_responsavel: Optional[str] = Query(None, description='Unidade Gestora Responsável'),
    fonte_recurso: Optional[str] = Query(None, description='Fonte de Recurso da Nota de Empenho'),
    natureza_despesa: Optional[str] = Query(None, description='Código da natureza de despesa'),
    plano_interno: Optional[str] = Query(None, description='Plano Interno'),
    ptres: Optional[str] = Query(None, description='Programa de Trabalho Resumido'),
    valor_empenho: Optional[float] = Query(None, description='Valor empenhado', gt=0),
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
        query = select(models.Empenho).where( # Changed model
            and_(
                models.Empenho.id_empenho == id_empenho if id_empenho is not None else True,
                models.Empenho.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.Empenho.nr_empenho.ilike(f"%{nr_empenho}%") if nr_empenho is not None else True,
                models.Empenho.tipo_nota.ilike(f"%{tipo_nota}%") if tipo_nota is not None else True,
                models.Empenho.desc_tipo_nota.ilike(f"%{desc_tipo_nota}%") if desc_tipo_nota is not None else True,
                cast(models.Empenho.data_emissao, Date) == date.fromisoformat(data_emissao) if data_emissao is not None else True,
                models.Empenho.cod_situacao_empenho.ilike(f"%{cod_situacao_empenho}%") if cod_situacao_empenho is not None else True,
                models.Empenho.desc_situacao_empenho.ilike(f"%{desc_situacao_empenho}%") if desc_situacao_empenho is not None else True,
                models.Empenho.ug_emitente.ilike(f"%{ug_emitente}%") if ug_emitente is not None else True,
                models.Empenho.ug_responsavel.ilike(f"%{ug_responsavel}%") if ug_responsavel is not None else True,
                models.Empenho.fonte_recurso.ilike(f"%{fonte_recurso}%") if fonte_recurso is not None else True,
                models.Empenho.natureza_despesa.ilike(f"%{natureza_despesa}%") if natureza_despesa is not None else True,
                models.Empenho.plano_interno.ilike(f"%{plano_interno}%") if plano_interno is not None else True,
                models.Empenho.ptres.ilike(f"%{ptres}%") if ptres is not None else True,
                models.Empenho.valor_empenho == valor_empenho if valor_empenho is not None else True,
            )
        )
        
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedEmpenhoResponse,
                                          current_page=pagina,
                                          records_per_page=tamanho_da_pagina)
        return result

    # except ValueError as ve: # Catch potential date parsing errors
    #      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"Formato de data inválido: {ve}. Utilize o formato AAAA-MM-DD.")
    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)