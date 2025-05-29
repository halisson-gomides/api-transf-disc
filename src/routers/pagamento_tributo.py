from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedPagamentoTributoResponse
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

pagamento_tributo_router = APIRouter(tags=["Movimentação Financeira"])
config = Settings()


@pagamento_tributo_router.get("/pagamento-tributo",
                            status_code=status.HTTP_200_OK,
                            description="Retorna uma Lista Paginada dos dados dos Pagamentos de Tributos.",
                            response_description="Lista Paginada de Pagamentos de Tributos",
                            response_model=PaginatedPagamentoTributoResponse
                            )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_pagamento_tributo(
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    data_tributo: Optional[str] = Query(None, description='Data da realização do pagamento do tributo (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    vl_pag_tributos: Optional[float] = Query(None, description='Valor do tributo', gt=0),
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
        query = select(models.PagamentoTributo).where(
            and_(
                models.PagamentoTributo.nr_convenio == nr_convenio if nr_convenio is not None else True,
                cast(models.PagamentoTributo.data_tributo, Date) == date.fromisoformat(data_tributo) if data_tributo is not None else True,
                models.PagamentoTributo.vl_pag_tributos >= (vl_pag_tributos - epsilon) if vl_pag_tributos is not None else True,
                models.PagamentoTributo.vl_pag_tributos <= (vl_pag_tributos + epsilon) if vl_pag_tributos is not None else True,
            )
        )

        result = await get_paginated_data(query=query,
                                         dbsession=dbsession,
                                         response_schema=PaginatedPagamentoTributoResponse,
                                         current_page=pagina,
                                         records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                           detail=config.ERROR_MESSAGE_INTERNAL)  # e.__repr__()