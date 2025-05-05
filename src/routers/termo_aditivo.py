from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedTermoAditivoResponse, PaginatedResponseTemplate
from datetime import date
from typing import Optional
from appconfig import Settings
from src.cache import cache

termo_aditivo_router = APIRouter(tags=["Instrumento"])
config = Settings()


@termo_aditivo_router.get("/termo_aditivo",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Termo Aditivo.",
                response_description="Lista Paginada de Termos Aditivos",
                response_model=PaginatedTermoAditivoResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_termo_aditivo(
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    id_solicitacao: Optional[int] = Query(None, description='Identificador único da solicitação de alteração', gt=0),
    numero_ta: Optional[str] = Query(None, description='Número do Termo Aditivo'),
    tipo_ta: Optional[str] = Query(None, description='Tipo do Termo Aditivo'),
    dt_assinatura_ta: Optional[str] = Query(None, description='Data da assinatura do Termo Aditivo (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_inicio_ta: Optional[str] = Query(None, description='Data Início de Vigência do Termo Aditivo (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_fim_ta: Optional[str] = Query(None, description='Data Fim de Vigência do Termo Aditivo (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    justificativa_ta: Optional[str] = Query(None, description='Justificativa para a realização do Termo Aditivo'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    # Exclude pagination params and dbsession from the check
    params_list = list(params.keys())[:-3] 
    
    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=config.ERROR_MESSAGE_NO_PARAMS)
    
    try:
        query = select(models.TermoAditivo).where(
            and_(
                models.TermoAditivo.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.TermoAditivo.id_solicitacao == id_solicitacao if id_solicitacao is not None else True,
                models.TermoAditivo.numero_ta.ilike(f"%{numero_ta}%") if numero_ta is not None else True,
                models.TermoAditivo.tipo_ta.ilike(f"%{tipo_ta}%") if tipo_ta is not None else True,
                cast(models.TermoAditivo.dt_assinatura_ta, Date) == date.fromisoformat(dt_assinatura_ta) if dt_assinatura_ta is not None else True,
                cast(models.TermoAditivo.dt_inicio_ta, Date) == date.fromisoformat(dt_inicio_ta) if dt_inicio_ta is not None else True,
                cast(models.TermoAditivo.dt_fim_ta, Date) == date.fromisoformat(dt_fim_ta) if dt_fim_ta is not None else True,
                models.TermoAditivo.justificativa_ta.ilike(f"%{justificativa_ta}%") if justificativa_ta is not None else True,
            )
        )
        
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        # # Explicitly set the data type for the response model
        # result.data = [models.TermoAditivo.model_validate(item) for item in result.data]
        return result
    
    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)