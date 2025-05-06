from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedConvenioResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

convenio_router = APIRouter(tags=["Instrumento"])
config = Settings()


@convenio_router.get("/convenio",
                      status_code=status.HTTP_200_OK,
                      description="Retorna uma Lista Paginada dos dados dos Convênios.",
                      response_description="Lista Paginada de Convênios",
                      response_model=PaginatedConvenioResponse
                      )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_convenio(
    nr_convenio: Optional[int] = Query(None, description='Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999', gt=0),
    id_proposta: Optional[int] = Query(None, description='ID da Proposta associada ao Convênio', gt=0),
    dia_assin_conv: Optional[str] = Query(None, description='Data de assinatura do Convênio (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    sit_convenio: Optional[str] = Query(None, description='Situação do Convênio'),
    subsituacao_conv: Optional[Literal['Convênio', 'Convênio Cancelado', 'Convênio Encerrado', 'Proposta', 'Em aditivação']] = Query(None, description='Subsituação do Convênio'),
    situacao_publicacao: Optional[Literal['Publicado', 'Transferido para IN']] = Query(None, description='Situação atual da Publicação do instrumento'),
    instrumento_ativo: Optional[Literal['SIM', 'NÃO']] = Query(None, description='Indica se o instrumento está ativo'), 
    ind_opera_obtv: Optional[Literal['SIM', 'NÃO']] = Query(None, description='Indicativo de que o Convênio opera com OBTV'),
    nr_processo: Optional[str] = Query(None, description='Número interno do processo do instrumento'),
    ug_emitente: Optional[str] = Query(None, description='Unidade Gestora Emitente'),
    dia_publ_conv: Optional[str] = Query(None, description='Data de publicação do Convênio (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dia_inic_vigenc_conv: Optional[str] = Query(None, description='Data de início da vigência do Convênio (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dia_fim_vigenc_conv: Optional[str] = Query(None, description='Data de fim da vigência do Convênio (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dia_fim_vigenc_original_conv: Optional[str] = Query(None, description='Data de fim da vigência original do Convênio (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dia_limite_prest_contas: Optional[str] = Query(None, description='Data limite para Prestação de Contas (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_suspensiva: Optional[str] = Query(None, description='Data prevista para resolução da Cláusula Suspensiva (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    data_retirada_suspensiva: Optional[str] = Query(None, description='Data de retirada do instrumento da situação de Cláusula Suspensiva (AAAA-MM-DD)', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    situacao_contratacao: Optional[Literal['Cláusula Suspensiva', 'Liminar Judicial', 'Normal', 'Sob Liminar Judicial e Cláusula Suspensiva']] = Query(None, description='Situação atual da Contratação'),
    ind_assinado: Optional[Literal['SIM', 'NÃO']] = Query(None, description='Indica se o convênio está assinado'), 
    motivo_suspensao: Optional[str] = Query(None, description='Descrição do motivo de suspensão referente a cláusula suspensiva'),
    qtde_convenios: Optional[int] = Query(None, description='Quantidade de Instrumentos Assinados', gt=0),
    qtd_ta: Optional[int] = Query(None, description='Quantidade de Termos Aditivos', gt=0),
    qtd_proroga: Optional[int] = Query(None, description='Quantidade de Prorrogas de Ofício', gt=0),
    ind_foto: Optional[Literal['SIM', 'NÃO']] = Query(None, description='Indicador se o Convênio possui Foto'), 
    vl_global_conv: Optional[float] = Query(None, description='Valor Global do Convênio', gt=0),
    vl_repasse_conv: Optional[float] = Query(None, description='Valor de Repasse do Convênio', gt=0),
    vl_contrapartida_conv: Optional[float] = Query(None, description='Valor da Contrapartida do Convênio', gt=0),
    valor_global_original_conv: Optional[float] = Query(None, description='Valor Global Original do Instrumento', gt=0),
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
        query = select(models.Convenio).where(
            and_(
                models.Convenio.nr_convenio == nr_convenio if nr_convenio is not None else True,
                models.Convenio.id_proposta == id_proposta if id_proposta is not None else True,
                cast(models.Convenio.dia_assin_conv, Date) == date.fromisoformat(dia_assin_conv) if dia_assin_conv is not None else True,
                models.Convenio.sit_convenio.ilike(f"%{sit_convenio}%") if sit_convenio is not None else True,
                models.Convenio.subsituacao_conv == subsituacao_conv if subsituacao_conv is not None else True,
                models.Convenio.situacao_publicacao == situacao_publicacao if situacao_publicacao is not None else True,
                models.Convenio.instrumento_ativo == instrumento_ativo if instrumento_ativo is not None else True,
                models.Convenio.ind_opera_obtv == ind_opera_obtv if ind_opera_obtv is not None else True,
                models.Convenio.nr_processo.ilike(f"%{nr_processo}%") if nr_processo is not None else True,
                models.Convenio.ug_emitente.ilike(f"%{ug_emitente}%") if ug_emitente is not None else True,
                cast(models.Convenio.dia_publ_conv, Date) == date.fromisoformat(dia_publ_conv) if dia_publ_conv is not None else True,
                cast(models.Convenio.dia_inic_vigenc_conv, Date) == date.fromisoformat(dia_inic_vigenc_conv) if dia_inic_vigenc_conv is not None else True,
                cast(models.Convenio.dia_fim_vigenc_conv, Date) == date.fromisoformat(dia_fim_vigenc_conv) if dia_fim_vigenc_conv is not None else True,
                cast(models.Convenio.dia_fim_vigenc_original_conv, Date) == date.fromisoformat(dia_fim_vigenc_original_conv) if dia_fim_vigenc_original_conv is not None else True,
                cast(models.Convenio.dia_limite_prest_contas, Date) == date.fromisoformat(dia_limite_prest_contas) if dia_limite_prest_contas is not None else True,
                cast(models.Convenio.data_suspensiva, Date) == date.fromisoformat(data_suspensiva) if data_suspensiva is not None else True,
                cast(models.Convenio.data_retirada_suspensiva, Date) == date.fromisoformat(data_retirada_suspensiva) if data_retirada_suspensiva is not None else True,
                models.Convenio.situacao_contratacao == situacao_contratacao if situacao_contratacao is not None else True,
                models.Convenio.ind_assinado == ind_assinado if ind_assinado is not None else True,
                models.Convenio.motivo_suspensao.ilike(f"%{motivo_suspensao}%") if motivo_suspensao is not None else True,
                models.Convenio.ind_foto == ind_foto if ind_foto is not None else True,
                models.Convenio.qtde_convenios == qtde_convenios if qtde_convenios is not None else True,
                models.Convenio.qtd_ta == qtd_ta if qtd_ta is not None else True,
                models.Convenio.qtd_proroga == qtd_proroga if qtd_proroga is not None else True,
                models.Convenio.vl_global_conv == vl_global_conv if vl_global_conv is not None else True,
                models.Convenio.vl_repasse_conv == vl_repasse_conv if vl_repasse_conv is not None else True,
                models.Convenio.vl_contrapartida_conv == vl_contrapartida_conv if vl_contrapartida_conv is not None else True,
                models.Convenio.valor_global_original_conv == valor_global_original_conv if valor_global_original_conv is not None else True,
            )
        )

        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedConvenioResponse,
                                          current_page=pagina,
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        # Log the exception e for debugging purposes if needed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)
