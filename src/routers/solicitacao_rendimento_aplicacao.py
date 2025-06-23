from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedSolicitacaoRendimentoAplicacaoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

solicitacao_rendimento_aplicacao_router = APIRouter(tags=["Outros"])
config = Settings()

@solicitacao_rendimento_aplicacao_router.get(
    "/solicitacao-rendimento-aplicacao",
    status_code=status.HTTP_200_OK,
    description="Retorna uma Lista Paginada das Solicitações de Uso de Rendimento de Aplicação.",
    response_description="Lista Paginada de Solicitações de Uso de Rendimento de Aplicação",
    response_model=PaginatedSolicitacaoRendimentoAplicacaoResponse
)
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_solicitacao_rendimento_aplicacao(
    id_solicitacao_rend_aplicacao: Optional[int] = Query(None, description='Identificador único do registro de solicitação de uso de rendimento de aplicação.', ge=1),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Faixa reservada: 700000 a 999999', ge=1),
    nr_solicitacao_rend_aplicacao: Optional[int] = Query(None, description='Número único da solicitação por instrumento.'),
    status_solicitacao_rend_aplicacao: Optional[Literal['Aguardando Análise do Concedente', 'Autorizada (Aguardando ajuste PT)', 'Cadastrado', 'Cancelado pelo Convenente', 'Em Análise pelo Concedente', 'Em Complementação pelo Convenente', 'Enviado para o SIAFI', 'Pendente de Envio ao SIAFI', 'PT Ajustado (aguardando aprovação do Concedente)', 'PT Ajustado e Aprovado (Aguardando atualização Agendador)', 'PT Ajustado e Aprovado', 'PT Ajustado e Pendente de Envio ao SIAFI', 'PT Reprovado e Cancelado', 'Recusada pelo Concedente']] = Query(None, description='Situação da solicitação de uso do rendimento de aplicação.'),
    data_solicitacao_rend_aplicacao: Optional[str] = Query(None, description='Data da solicitação de uso de rendimento de aplicação (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    valor_solicitacao_rend_aplicacao: Optional[float] = Query(None, description='Valor da solicitação de uso de rendimento de aplicação.'),
    valor_aprovado_solicitacao_rend_aplicacao: Optional[float] = Query(None, description='Valor aprovado pelo Concedente para uso do rendimento de aplicação.'),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]

    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.ERROR_MESSAGE_NO_PARAMS)

    try:
        query = select(models.SolicitacaoRendimentoAplicacao).where(
            and_(
                models.SolicitacaoRendimentoAplicacao.id_solicitacao_rend_aplicacao == id_solicitacao_rend_aplicacao if id_solicitacao_rend_aplicacao is not None else True,
                models.SolicitacaoRendimentoAplicacao.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.SolicitacaoRendimentoAplicacao.nr_solicitacao_rend_aplicacao == nr_solicitacao_rend_aplicacao if nr_solicitacao_rend_aplicacao is not None else True,
                models.SolicitacaoRendimentoAplicacao.status_solicitacao_rend_aplicacao == status_solicitacao_rend_aplicacao if status_solicitacao_rend_aplicacao is not None else True,
                cast(models.SolicitacaoRendimentoAplicacao.data_solicitacao_rend_aplicacao, Date) == date.fromisoformat(data_solicitacao_rend_aplicacao) if data_solicitacao_rend_aplicacao is not None else True,
                models.SolicitacaoRendimentoAplicacao.valor_solicitacao_rend_aplicacao == valor_solicitacao_rend_aplicacao if valor_solicitacao_rend_aplicacao is not None else True,
                models.SolicitacaoRendimentoAplicacao.valor_aprovado_solicitacao_rend_aplicacao == valor_aprovado_solicitacao_rend_aplicacao if valor_aprovado_solicitacao_rend_aplicacao is not None else True,
            )
        )
        result = await get_paginated_data(
            query=query,
            dbsession=dbsession,
            response_schema=PaginatedResponseTemplate,
            current_page=pagina,
            records_per_page=tamanho_da_pagina
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=config.ERROR_MESSAGE_INTERNAL)