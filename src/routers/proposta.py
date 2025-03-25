from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedResponseTemplate, PaginatedPropostaResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

prtas_router = APIRouter(tags=["Proposta"])
config = Settings()


@prtas_router.get("/proposta",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Propostas.",
                response_description="Lista Paginada de Propostas",
                response_model=PaginatedPropostaResponse
                )
@cache(ttl=config.CACHE_TTL, lock=True)
async def consulta_proposta(
    id_proposta: Optional[int] = Query(None, description='Código Sequencial do Sistema para uma Proposta'),
    id_proponente: Optional[int] = Query(None, description='Identificador único do proponente'),
    uf_proponente: Literal['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'] = Query(None, description='UF do Proponente.'),
    munic_proponente: Optional[str] = Query(None, description='Município do Proponente'),
    cod_munic_ibge: Optional[str] = Query(None, description='Código IBGE do Município'),
    cod_orgao_sup: Optional[str] = Query(None, description='Código do Órgão Superior do Concedente'),
    desc_orgao_sup: Optional[str] = Query(None, description='Nome do Órgão Superior do Concedente'),
    natureza_juridica: Literal['Administração Pública Estadual ou do Distrito Federal', 'Administração Pública Municipal', 'Consórcio Público', 'Empresa pública/Sociedade de economia mista e Organização da Sociedade Civil'] = Query(None, description='Natureza Jurídica do Proponente.'),
    nr_proposta: Optional[str] = Query(None, description='Número da Proposta gerado pelo Siconv'),
    dia_prop: Optional[str] = Query(None, description='Dia do cadastro da Proposta'),
    mes_prop: Optional[str] = Query(None, description='Mês do cadastro da Proposta'),
    ano_prop: Optional[str] = Query(None, description='Ano do cadastro da Proposta'),
    dia_proposta: Optional[str] = Query(None, description='Data do cadastro da Proposta', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    cod_orgao: Optional[str] = Query(None, description='Código do Órgão ou Entidade Concedente'),
    desc_orgao: Optional[str] = Query(None, description='Nome do Órgão ou Entidade Concedente'),
    modalidade: Literal['CONTRATO DE REPASSE', 'CONVENIO', 'TERMO DE COLABORACAO', 'TERMO DE FOMENTO', 'TERMO DE PARCERIA'] = Query(None, description='Modalidade da Proposta'),
    identif_proponente: Optional[str] = Query(None, description='CNPJ do Proponente'),
    nm_proponente: Optional[str] = Query(None, description='Nome da Entidade Proponente'),
    cep_proponente: Optional[str] = Query(None, description='CEP do Proponente'),
    endereco_proponente: Optional[str] = Query(None, description='Endereço do Proponente'),
    bairro_proponente: Optional[str] = Query(None, description='Bairro do Proponente'),
    nm_banco: Optional[str] = Query(None, description='Nome do Banco para depósito do recurso da Transferência Voluntária'),
    situacao_conta: Literal['Aguardando Retorno do Banco', 'Enviada', 'Cadastrada', 'Registrada', 'Erro na Abertura de Conta', 'Regularizada', 'A Verificar', 'Aguardando Envio', 'Pendente de Regularização'] = Query(None, description='Situação atual da conta bancária do instrumento.'),
    situacao_projeto_basico: Literal['Aguardando Projeto Básico', 'Não Cadastrado', 'Projeto Básico Aprovado', 'Projeto Básico em Análise', 'Projeto Básico em Complementação', 'Projeto Básico Rejeitado'] = Query(None, description='Situação atual do Projeto Básico/Termo de Referência.'),
    sit_proposta: Literal['Proposta/Plano de Trabalho Cadastrados', 'Proposta/Plano de Trabalho em Análise', 'Proposta/Plano de Trabalho Rejeitados', 'Proposta/Plano de Trabalho Aprovados'] = Query(None, description='Situação atual da Proposta.'),
    dia_inic_vigencia_proposta: Optional[str] = Query(None, description='Data Início da Vigência da Proposta', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    dia_fim_vigencia_proposta: Optional[str] = Query(None, description='Data Fim da Vigência da Proposta', pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    objeto_proposta: Optional[str] = Query(None, description='Descrição do Objeto da Proposta'),
    item_investimento: Optional[str] = Query(None, description='Itens de Investimento da proposta'),
    enviada_mandataria: Literal['SIM', 'NÃO', 'NÃO APLICÁVEL'] = Query(None, description='Campo que indica se o Contrato de Repasse foi enviado para Instituição Mandatária.'),
    vl_global_prop: Optional[float] = Query(None, description='Valor Global da proposta cadastrada (Valor de Repasse Proposta + Valor Contrapartida Proposta)', ge=0),
    vl_repasse_prop: Optional[float] = Query(None, description='Valor de Repasse do Governo Federal referente a proposta cadastrada', ge=0),
    vl_contrapartida_prop: Optional[float] = Query(None, description='Valor da Contrapartida apresentada na proposta pelo convenente', ge=0),
    nome_subtipo_proposta: Optional[str] = Query(None, description='Nome do subtipo de instrumento'),
    descricao_subtipo_proposta: Optional[str] = Query(None, description='Descrição do subtipo do instrumento'),
    cd_agencia: Optional[str] = Query(None, description='Código da Agência'),
    cd_conta: Optional[str] = Query(None, description='Código da Conta'),
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
        query = select(models.Proposta).where(
            and_(
                models.Proposta.id_proposta == id_proposta if id_proposta is not None else True,
                models.Proposta.id_proponente == id_proponente if id_proponente is not None else True,
                models.Proposta.uf_proponente == uf_proponente if uf_proponente is not None else True,
                models.Proposta.munic_proponente.ilike(f"%{munic_proponente}%") if munic_proponente is not None else True,
                models.Proposta.cod_munic_ibge == cod_munic_ibge if cod_munic_ibge is not None else True,
                models.Proposta.cod_orgao_sup == cod_orgao_sup if cod_orgao_sup is not None else True,
                models.Proposta.desc_orgao_sup.ilike(f"%{desc_orgao_sup}%") if desc_orgao_sup is not None else True,
                models.Proposta.natureza_juridica == natureza_juridica if natureza_juridica is not None else True,
                models.Proposta.nr_proposta == nr_proposta if nr_proposta is not None else True,
                models.Proposta.dia_prop == dia_prop if dia_prop is not None else True,
                models.Proposta.mes_prop == mes_prop if mes_prop is not None else True,
                models.Proposta.ano_prop == ano_prop if ano_prop is not None else True,
                cast(models.Proposta.dia_proposta, Date) == date.fromisoformat(dia_proposta) if dia_proposta is not None else True,
                models.Proposta.cod_orgao == cod_orgao if cod_orgao is not None else True,
                models.Proposta.desc_orgao.ilike(f"%{desc_orgao}%") if desc_orgao is not None else True,
                models.Proposta.modalidade == modalidade if modalidade is not None else True,
                models.Proposta.identif_proponente == identif_proponente if identif_proponente is not None else True,
                models.Proposta.nm_proponente.ilike(f"%{nm_proponente}%") if nm_proponente is not None else True,
                models.Proposta.cep_proponente == cep_proponente if cep_proponente is not None else True,
                models.Proposta.endereco_proponente.ilike(f"%{endereco_proponente}%") if endereco_proponente is not None else True,
                models.Proposta.bairro_proponente.ilike(f"%{bairro_proponente}%")    if bairro_proponente is not None else True,
                models.Proposta.nm_banco.ilike(f"%{nm_banco}%") if nm_banco is not None else True,
                models.Proposta.situacao_conta == situacao_conta if situacao_conta is not None else True,
                models.Proposta.situacao_projeto_basico == situacao_projeto_basico if situacao_projeto_basico is not None else True,
                models.Proposta.sit_proposta == sit_proposta if sit_proposta is not None else True,
                cast(models.Proposta.dia_inic_vigencia_proposta, Date) == date.fromisoformat(dia_inic_vigencia_proposta) if dia_inic_vigencia_proposta is not None else True,
                cast(models.Proposta.dia_fim_vigencia_proposta, Date) == date.fromisoformat(dia_fim_vigencia_proposta) if dia_fim_vigencia_proposta is not None else True,
                models.Proposta.objeto_proposta.ilike(f"%{objeto_proposta}%")    if objeto_proposta is not None else True,
                models.Proposta.item_investimento == item_investimento if item_investimento is not None else True,
                models.Proposta.enviada_mandataria == enviada_mandataria if enviada_mandataria is not None else True,
                models.Proposta.vl_global_prop == vl_global_prop if vl_global_prop is not None else True,
                models.Proposta.vl_repasse_prop == vl_repasse_prop if vl_repasse_prop is not None else True,
                models.Proposta.vl_contrapartida_prop == vl_contrapartida_prop if vl_contrapartida_prop is not None else True,
                models.Proposta.nome_subtipo_proposta.ilike(f"%{nome_subtipo_proposta}%") if nome_subtipo_proposta is not None else True,
                models.Proposta.descricao_subtipo_proposta.ilike(f"%{descricao_subtipo_proposta}%") if descricao_subtipo_proposta is not None else True,
                models.Proposta.cd_agencia == cd_agencia if cd_agencia is not None else True,
                models.Proposta.cd_conta == cd_conta if cd_conta is not None else True                
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
