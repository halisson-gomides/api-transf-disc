from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedObtvConvenenteResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

obtv_convenente_router = APIRouter(tags=["Movimentação Financeira"])
config = Settings()


@obtv_convenente_router.get("/obtv-convenente",
                           status_code=status.HTTP_200_OK,
                           description="Retorna uma Lista Paginada dos dados dos OBTVs do Convenente.",
                           response_description="Lista Paginada de OBTVs do Convenente",
                           response_model=PaginatedObtvConvenenteResponse
                           )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_obtv_convenente(
    nr_mov_fin: Optional[int] = Query(None, description='Número identificador da movimentação financeira', gt=0),
    identif_favorecido_obtv_conv: Optional[str] = Query(None, description='CNPJ/CPF do Favorecido recebedor do pagamento'),
    nm_favorecido_obtv_conv: Optional[str] = Query(None, description='Nome do Favorecido recebedor do pagamento'),
    tp_aquisicao: Optional[str] = Query(None, description='Tipo de Aquisição'),
    vl_pago_obtv_conv: Optional[float] = Query(None, description='Valor pago ao favorecido', gt=0),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]  # Exclude pagination and dbsession
    epsilon = 0.0001

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                           detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.ObtvConvenente).where(
            and_(
                models.ObtvConvenente.nr_mov_fin == nr_mov_fin if nr_mov_fin is not None else True,
                models.ObtvConvenente.identif_favorecido_obtv_conv.ilike(f"%{identif_favorecido_obtv_conv}%") if identif_favorecido_obtv_conv is not None else True,
                models.ObtvConvenente.nm_favorecido_obtv_conv.ilike(f"%{nm_favorecido_obtv_conv}%") if nm_favorecido_obtv_conv is not None else True,
                models.ObtvConvenente.tp_aquisicao.ilike(f"%{tp_aquisicao}%") if tp_aquisicao is not None else True,
                models.ObtvConvenente.vl_pago_obtv_conv >= (vl_pago_obtv_conv - epsilon) if vl_pago_obtv_conv is not None else True,
                models.ObtvConvenente.vl_pago_obtv_conv <= (vl_pago_obtv_conv + epsilon) if vl_pago_obtv_conv is not None else True,
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
                                         response_schema=PaginatedObtvConvenenteResponse,
                                         current_page=pagina,
                                         records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                           detail=config.ERROR_MESSAGE_INTERNAL) # e.__repr__()