from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedPropostaSelecaoPacResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

psp_router = APIRouter(tags=["PAC"])
config = Settings()


@psp_router.get("/proposta_selecao_pac",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Propostas Selecionadas do PAC.",
                response_description="Lista Paginada de Propostas Selecionadas do PAC",
                response_model=PaginatedPropostaSelecaoPacResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_proposta_selecao_pac(
    id_proposta_selecao_pac: Optional[int] = Query(None, description='Identificador único da Proposta do Novo PAC', gt=0),
    id_programa: Optional[int] = Query(None, description='Código Sequencial do Sistema para um Programa', gt=0),
    id_proponente: Optional[int] = Query(None, description='Identificador único do proponente', gt=0),
    nr_proposta_selecao_pac: Optional[str] = Query(None, description='Número da Proposta do Novo PAC'),
    data_cadastro_proposta_selecao_pac: Optional[str] = Query(None, description='Data de Cadastro da Proposta do Novo PAC', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_envio_proposta_selecao_pac: Optional[str] = Query(None, description='Data de Envio da Proposta do Novo PAC', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    objeto_proposta_selecao_pac: Optional[str] = Query(None, description='Objeto da Proposta do Novo PAC'),
    situacao_proposta_selecao_pac: Optional[str] = Query(None, description='Situação da Proposta do Novo PAC'),
    valor_total_proposta_selecao_pac: Optional[float] = Query(None, description='Valor Total da Proposta do Novo PAC'),
    justificativa_proposta_selecao_pac: Optional[str] = Query(None, description='Justificativa da Proposta do Novo PAC'),
    tem_anexo_proposta_selecao_pac: Literal['SIM', 'NÃO'] = Query(None, description='Indica se a Proposta do Novo PAC tem anexos'),
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
        query = select(models.PropostaSelecaoPac).where(
            and_(
                models.PropostaSelecaoPac.id_proposta_selecao_pac == id_proposta_selecao_pac if id_proposta_selecao_pac is not None else True,
                models.PropostaSelecaoPac.id_programa == id_programa if id_programa is not None else True,
                models.PropostaSelecaoPac.id_proponente == id_proponente if id_proponente is not None else True,
                models.PropostaSelecaoPac.nr_proposta_selecao_pac == nr_proposta_selecao_pac if nr_proposta_selecao_pac is not None else True,
                cast(models.PropostaSelecaoPac.data_cadastro_proposta_selecao_pac, Date) == date.fromisoformat(data_cadastro_proposta_selecao_pac) if data_cadastro_proposta_selecao_pac is not None else True,
                cast(models.PropostaSelecaoPac.data_envio_proposta_selecao_pac, Date) == date.fromisoformat(data_envio_proposta_selecao_pac) if data_envio_proposta_selecao_pac is not None else True,
                models.PropostaSelecaoPac.objeto_proposta_selecao_pac.ilike(f"%{objeto_proposta_selecao_pac}%") if objeto_proposta_selecao_pac is not None else True,
                models.PropostaSelecaoPac.situacao_proposta_selecao_pac.ilike(f"%{situacao_proposta_selecao_pac}%") if situacao_proposta_selecao_pac is not None else True,
                models.PropostaSelecaoPac.valor_total_proposta_selecao_pac == valor_total_proposta_selecao_pac if valor_total_proposta_selecao_pac is not None else True,
                models.PropostaSelecaoPac.justificativa_proposta_selecao_pac.ilike(f"%{justificativa_proposta_selecao_pac}%") if justificativa_proposta_selecao_pac is not None else True,
                models.PropostaSelecaoPac.tem_anexo_proposta_selecao_pac == tem_anexo_proposta_selecao_pac if tem_anexo_proposta_selecao_pac is not None else True,
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
