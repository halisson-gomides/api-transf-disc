from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

pg_router = APIRouter(tags=["Programa"])
config = Settings()


@pg_router.get("/programa",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Programas - Discricionárias e Legais.",
                response_description="Lista Paginada de Programas - Discricionárias e Legais",
                response_model=PaginatedProgramaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_programa(
    id_programa: Optional[int] = Query(None, description="Código Sequencial do Sistema para um Programa"),
    cod_orgao_sup_programa: Optional[str] = Query(None, description="Código do Órgão executor do Programa"),
    desc_orgao_sup_programa: Optional[str] = Query(None, description="Nome do Órgão executor do Programa"),
    cod_programa: Optional[str] = Query(None, description="Chave que identifica o programa composta por: (Cód.Órgão+Ano+Cód.Sequencial do Sistema)"),
    nome_programa: Optional[str] = Query(None, description="Descrição do Programa de Governo"),
    sit_programa: Literal['Cadastrado', 'Disponibilizado', 'Inativo'] = Query(None, description="Situação atual do Programa."),
    data_disponibilizacao: Optional[str] = Query(None, description="Data de disponibilização do Programa", pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    ano_disponibilizacao: Optional[int] = Query(None, description="Ano de disponibilização do Programa", gt=0),
    dt_prog_ini_receb_prop: Optional[str] = Query(None, description="Data Início para o recebimento das propostas voluntárias para o Programa", pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_prog_fim_receb_prop: Optional[str] = Query(None, description="Data Fim para o recebimento das propostas voluntárias para o Programa", pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_prog_ini_emenda_par: Optional[str] = Query(None, description="Data Início para o recebimento das propostas de Emenda Parlamentar para o Programa", pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_prog_fim_emenda_par: Optional[str] = Query(None, description="Data Fim para o recebimento das propostas de Emenda Parlamentar para o Programa", pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_prog_ini_benef_esp: Optional[str] = Query(None, description="Data Início para o recebimento das propostas de beneficiário específico para o Programa", pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dt_prog_fim_benef_esp: Optional[str] = Query(None, description="Data Fim para o recebimento das propostas de beneficiário específico para o Programa", pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    modalidade_programa: Literal['CONTRATO DE REPASSE', 'CONVENIO', 'TERMO DE COLABORACAO', 'TERMO DE FOMENTO', 'TERMO DE PARCERIA'] = Query(None, description="Modalidade do Programa."),
    natureza_juridica_programa: Optional[str] = Query(None, description="Natureza Jurídica Atendida pelo Programa. Domínio: Administração Pública Estadual ou do Distrito Federal, Administração Pública Municipal, Consórcio Público, Empresa pública/Sociedade de economia mista e Organização da Sociedade Civil"),
    uf_programa: Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'] = Query(None, description="Ufs Habilitadas para o Programa. Quando o valor é nulo, o programa atende a todo o Brasil"),
    acao_orcamentaria: Optional[str] = Query(None, description="Número da Ação Orçamentária"),
    nome_subtipo_programa: Optional[str] = Query(None, description="Nome do subtipo de instrumento"),
    descricao_subtipo_programa: Optional[str] = Query(None, description="Descrição do subtipo do instrumento"),
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
        query = select(models.Programa).options(
            selectinload(models.Programa.proponentes),
            selectinload(models.Programa.propostas)
        ).where(
            and_(
                models.Programa.id_programa == id_programa if id_programa is not None else True,
                models.Programa.cod_orgao_sup_programa == cod_orgao_sup_programa if cod_orgao_sup_programa is not None else True,
                models.Programa.desc_orgao_sup_programa.ilike(f"%{desc_orgao_sup_programa}%") if desc_orgao_sup_programa is not None else True,
                models.Programa.cod_programa == cod_programa if cod_programa is not None else True,
                models.Programa.nome_programa.ilike(f"%{nome_programa}%") if nome_programa is not None else True,
                models.Programa.sit_programa.ilike(f"%{sit_programa}%") if sit_programa is not None else True,
                cast(models.Programa.data_disponibilizacao, Date) == date.fromisoformat(data_disponibilizacao) if data_disponibilizacao is not None else True,
                models.Programa.ano_disponibilizacao == str(ano_disponibilizacao) if ano_disponibilizacao is not None else True,
                cast(models.Programa.dt_prog_ini_receb_prop, Date) == date.fromisoformat(dt_prog_ini_receb_prop) if dt_prog_ini_receb_prop is not None else True,
                cast(models.Programa.dt_prog_fim_receb_prop, Date) == date.fromisoformat(dt_prog_fim_receb_prop) if dt_prog_fim_receb_prop is not None else True,
                cast(models.Programa.dt_prog_ini_emenda_par, Date) == date.fromisoformat(dt_prog_ini_emenda_par) if dt_prog_ini_emenda_par is not None else True,
                cast(models.Programa.dt_prog_fim_emenda_par, Date) == date.fromisoformat(dt_prog_fim_emenda_par) if dt_prog_fim_emenda_par is not None else True,
                cast(models.Programa.dt_prog_ini_benef_esp, Date) == date.fromisoformat(dt_prog_ini_benef_esp) if dt_prog_ini_benef_esp is not None else True,
                cast(models.Programa.dt_prog_fim_benef_esp, Date) == date.fromisoformat(dt_prog_fim_benef_esp) if dt_prog_fim_benef_esp is not None else True,
                models.Programa.modalidade_programa == modalidade_programa if modalidade_programa is not None else True,
                models.Programa.natureza_juridica_programa == natureza_juridica_programa if natureza_juridica_programa is not None else True,
                models.Programa.uf_programa == uf_programa if uf_programa is not None else True,
                models.Programa.acao_orcamentaria == acao_orcamentaria if acao_orcamentaria is not None else True,
                models.Programa.nome_subtipo_programa == nome_subtipo_programa if nome_subtipo_programa is not None else True,
                models.Programa.descricao_subtipo_programa == descricao_subtipo_programa if descricao_subtipo_programa is not None else True
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
                            detail=e.__repr__())