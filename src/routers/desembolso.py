from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedDesembolsoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

desembolso_router = APIRouter(tags=["Desembolso"]) # Tagging as Financeiro
config = Settings()


@desembolso_router.get("/desembolso",
                        status_code=status.HTTP_200_OK,
                        description="Retorna uma Lista Paginada dos dados de Desembolso.",
                        response_description="Lista Paginada de Desembolsos",
                        response_model=PaginatedDesembolsoResponse
                        )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_desembolso(
    id_desembolso: Optional[int] = Query(None, description='Identificador único gerado pelo Sistema para o Desembolso', gt=0),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    dt_ult_desembolso: Optional[str] = Query(None, description='Data da última Ordem Bancária gerada (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    qtd_dias_sem_desembolso: Optional[Literal[90, 180, 365]] = Query(None, description='Indicador de dias sem desembolso'), # Using Literal for specific domain values
    data_desembolso: Optional[str] = Query(None, description='Data da Ordem Bancária (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    ano_desembolso: Optional[int] = Query(None, description='Ano da Ordem Bancária', gt=1900, lt=2100),
    mes_desembolso: Optional[int] = Query(None, description='Mês da Ordem Bancária', ge=1, le=12),
    nr_siafi: Optional[str] = Query(None, description='Número do Documento no SIAFI'),
    ug_emitente_dh: Optional[str] = Query(None, description='Código da Unidade Gestora responsável pela emissão do documento.'),
    observacao_dh: Optional[str] = Query(None, description='Observação a respeito do documento hábil.'),
    vl_desembolsado: Optional[float] = Query(None, description='Valor disponibilizado pelo Governo Federal para a conta do instrumento', gt=0),
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
        query = select(models.Desembolso).where(
            and_(
                models.Desembolso.id_desembolso == id_desembolso if id_desembolso is not None else True,
                models.Desembolso.nr_convenio == nr_convenio if nr_convenio is not None else True,
                cast(models.Desembolso.dt_ult_desembolso, Date) == date.fromisoformat(dt_ult_desembolso) if dt_ult_desembolso is not None else True,
                models.Desembolso.qtd_dias_sem_desembolso == qtd_dias_sem_desembolso if qtd_dias_sem_desembolso is not None else True,
                cast(models.Desembolso.data_desembolso, Date) == date.fromisoformat(data_desembolso) if data_desembolso is not None else True,
                models.Desembolso.ano_desembolso == ano_desembolso if ano_desembolso is not None else True,
                models.Desembolso.mes_desembolso == mes_desembolso if mes_desembolso is not None else True,
                models.Desembolso.nr_siafi.ilike(f"%{nr_siafi}%") if nr_siafi is not None else True,
                models.Desembolso.ug_emitente_dh.ilike(f"%{ug_emitente_dh}%") if ug_emitente_dh is not None else True,
                models.Desembolso.observacao_dh.ilike(f"%{observacao_dh}%") if observacao_dh is not None else True,
                models.Desembolso.vl_desembolsado == vl_desembolsado if vl_desembolsado is not None else True,
            )
        )#.order_by(models.Desembolso.id_desembolso)
        
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedDesembolsoResponse,
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