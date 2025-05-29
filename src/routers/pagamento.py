from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedPagamentoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

pagamento_router = APIRouter(tags=["Movimentação Financeira"])
config = Settings()


@pagamento_router.get("/pagamento",
                      status_code=status.HTTP_200_OK,
                      description="Retorna uma Lista Paginada dos dados dos Pagamentos.",
                      response_description="Lista Paginada de Pagamentos",
                      response_model=PaginatedPagamentoResponse
                      )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_pagamento(
    nr_mov_fin: Optional[int] = Query(None, description='Número identificador da movimentação financeira', gt=0),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    identif_fornecedor: Optional[str] = Query(None, description='CNPJ/CPF do Fornecedor'),
    nome_fornecedor: Optional[str] = Query(None, description='Nome do Fornecedor'),
    tp_mov_financeira: Optional[Literal['PAGAMENTO A FAVORECIDO', 'PAGAMENTO A FAVORECIDO COM OBTV']] = Query(None, description='Tipo da movimentação financeira realizada'),
    data_pag: Optional[str] = Query(None, description='Data da realização do pagamento (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    nr_dl: Optional[str] = Query(None, description='Número identificador do Documento de Liquidação'),
    desc_dl: Optional[Literal['DIÁRIAS', 'DUPLICATA', 'FATURA', 'FOLHA DE PAGAMENTO', 'NOTA FISCAL', 'NOTA FISCAL / FATURA', 'OBTV PARA EXECUTOR', 'OBTV PARA O CONVENENTE']] = Query(None, description='Descrição do Documento de Liquidação'),
    vl_pago: Optional[float] = Query(None, description='Valor do pagamento', gt=0),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3] # Exclude pagination and dbsession

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.Pagamento).where(
            and_(
                models.Pagamento.nr_mov_fin == nr_mov_fin if nr_mov_fin is not None else True,
                models.Pagamento.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.Pagamento.identif_fornecedor.ilike(f"%{identif_fornecedor}%") if identif_fornecedor is not None else True,
                models.Pagamento.nome_fornecedor.ilike(f"%{nome_fornecedor}%") if nome_fornecedor is not None else True,
                models.Pagamento.tp_mov_financeira == tp_mov_financeira if tp_mov_financeira is not None else True,
                cast(models.Pagamento.data_pag, Date) == date.fromisoformat(data_pag) if data_pag is not None else True,
                models.Pagamento.nr_dl.ilike(f"%{nr_dl}%") if nr_dl is not None else True,
                models.Pagamento.desc_dl == desc_dl if desc_dl is not None else True,
                models.Pagamento.vl_pago == vl_pago if vl_pago is not None else True,
            )
        )

        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedPagamentoResponse,
                                          current_page=pagina,
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)