from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedLicitacaoResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

licitacao_router = APIRouter(tags=["Licitação/Contrato"])
config = Settings()


@licitacao_router.get("/licitacao",
                    status_code=status.HTTP_200_OK,
                    description="Retorna uma Lista Paginada dos dados de Licitação.",
                    response_description="Lista Paginada de Licitações",
                    response_model=PaginatedLicitacaoResponse
                    )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_licitacao(
    id_licitacao: Optional[int] = Query(None, description='Identificador único da licitação', gt=0),
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    nr_licitacao: Optional[str] = Query(None, description='Número do Processo de Execução'),
    modalidade_licitacao: Optional[Literal['Convite', 'Tomada de Preços', 'Concorrência', 'Concurso', 'Pregão']] = Query(None, description='Modalidade da Licitação'),
    tp_processo_compra: Optional[Literal['Dispensa de Licitação', 'Inexigibilidade', 'Licitação', 'Cotação Prévia', 'Pesquisa de Mercado']] = Query(None, description='Processo de Compras'),
    tipo_licitacao: Optional[str] = Query(None, description='Tipo da Licitação'),
    nr_processo_licitacao: Optional[str] = Query(None, description='Número do Processo informado pelo usuário'),
    data_publicacao_licitacao: Optional[str] = Query(None, description='Data de publicação do Processo de Execução', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_abertura_licitacao: Optional[str] = Query(None, description='Data de abertura do Processo de Execução', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_encerramento_licitacao: Optional[str] = Query(None, description='Data de encerramento do Processo de Execução', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_homologacao_licitacao: Optional[str] = Query(None, description='Data de homologação do Processo de Execução', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    status_licitacao: Optional[Literal['Concluído', 'Em Elaboração']] = Query(None, description='Status da Licitação'),
    situacao_aceite_processo_execu: Optional[str] = Query(None, description='Situação do aceite do processo de execução'),
    sistema_origem: Optional[str] = Query(None, description='Nome do Sistema de Origem da Licitação'),
    situacao_sistema: Optional[str] = Query(None, description='Descrição da Situação da Licitação no Sistema de Compras Externo'),
    valor_licitacao: Optional[float] = Query(None, description='Valor da Licitação', gt=0),
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
        query = select(models.Licitacao).where(
            and_(
                models.Licitacao.id_licitacao == id_licitacao if id_licitacao is not None else True,
                models.Licitacao.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.Licitacao.nr_licitacao.ilike(f"%{nr_licitacao}%") if nr_licitacao is not None else True,
                models.Licitacao.modalidade_licitacao == modalidade_licitacao if modalidade_licitacao is not None else True,
                models.Licitacao.tp_processo_compra == tp_processo_compra if tp_processo_compra is not None else True,
                models.Licitacao.tipo_licitacao.ilike(f"%{tipo_licitacao}%") if tipo_licitacao is not None else True,
                models.Licitacao.nr_processo_licitacao.ilike(f"%{nr_processo_licitacao}%") if nr_processo_licitacao is not None else True,
                cast(models.Licitacao.data_publicacao_licitacao, Date) == date.fromisoformat(data_publicacao_licitacao) if data_publicacao_licitacao is not None else True,
                cast(models.Licitacao.data_abertura_licitacao, Date) == date.fromisoformat(data_abertura_licitacao) if data_abertura_licitacao is not None else True,
                cast(models.Licitacao.data_encerramento_licitacao, Date) == date.fromisoformat(data_encerramento_licitacao) if data_encerramento_licitacao is not None else True,
                cast(models.Licitacao.data_homologacao_licitacao, Date) == date.fromisoformat(data_homologacao_licitacao) if data_homologacao_licitacao is not None else True,
                models.Licitacao.status_licitacao == status_licitacao if status_licitacao is not None else True,
                models.Licitacao.situacao_aceite_processo_execu.ilike(f"%{situacao_aceite_processo_execu}%") if situacao_aceite_processo_execu is not None else True,
                models.Licitacao.sistema_origem.ilike(f"%{sistema_origem}%") if sistema_origem is not None else True,
                models.Licitacao.situacao_sistema.ilike(f"%{situacao_sistema}%") if situacao_sistema is not None else True,
                models.Licitacao.valor_licitacao == valor_licitacao if valor_licitacao is not None else True,
            )
        )
        
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedLicitacaoResponse,
                                          current_page=pagina,
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)