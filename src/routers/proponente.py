from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedProponenteResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

prop_router = APIRouter(tags=["Proponente"])
config = Settings()


@prop_router.get("/proponente",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Proponentes.",
                response_description="Lista Paginada de Proponentes",
                response_model=PaginatedProponenteResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_proponente(
    id_proponente: Optional[int] = Query(None, description='Identificador único do proponente'),
    identif_proponente: Optional[str] = Query(None, description='CNPJ do Proponente'),
    nm_proponente: Optional[str] = Query(None, description='Nome da Entidade Proponente'),
    municipio_proponente: Optional[str] = Query(None, description='Município do Proponente'),
    uf_proponente: Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'] = Query(None, description=' UF do Proponente.'),
    endereco_proponente: Optional[str] = Query(None, description='Endereço do Proponente'),
    bairro_proponente: Optional[str] = Query(None, description='Bairro do Proponente'),
    cep_proponente: Optional[str] = Query(None, description='CEP do Proponente'),
    email_proponente: Optional[str] = Query(None, description='E-mail do Proponente'),
    telefone_proponente: Optional[str] = Query(None, description='Telefone do Proponente'),
    fax_proponente: Optional[str] = Query(None, description='Fax do Proponente'),
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
        query = select(models.Proponente).where(
            and_(
                models.Proponente.id_proponente == id_proponente if id_proponente is not None else True,
                models.Proponente.identif_proponente == identif_proponente if identif_proponente is not None else True,
                models.Proponente.nm_proponente.ilike(f"%{nm_proponente}%") if nm_proponente is not None else True,
                models.Proponente.municipio_proponente.ilike(f"%{municipio_proponente}%") if municipio_proponente is not None else True,
                models.Proponente.uf_proponente == uf_proponente if uf_proponente is not None else True,
                models.Proponente.endereco_proponente.ilike(f"%{endereco_proponente}%") if endereco_proponente is not None else True,
                models.Proponente.bairro_proponente.ilike(f"%{bairro_proponente}%") if bairro_proponente is not None else True,
                models.Proponente.cep_proponente == cep_proponente if cep_proponente is not None else True,
                models.Proponente.email_proponente.ilike(f"%{email_proponente}%") if email_proponente is not None else True,
                models.Proponente.telefone_proponente == telefone_proponente if telefone_proponente is not None else True,
                models.Proponente.fax_proponente == fax_proponente if fax_proponente is not None else True,
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
