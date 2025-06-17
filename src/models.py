from datetime import date, datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

db_schema = 'api_transferegov_discricionarias'

class BaseModel(SQLModel, table=False):
    __table_args__ = {"schema": db_schema}

# Tabela programa_proponente
class ProgramaProponentes(BaseModel, table=True):
    __tablename__ = "programa_proponentes"
    
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa", primary_key=True)
    id_proponente: int = Field(foreign_key=f"{db_schema}.proponentes.id_proponente", primary_key=True)

# Tabela programa_proposta
class ProgramaProposta(BaseModel, table=True):
    __tablename__ = "programa_proposta"
    
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa", primary_key=True)
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)

# Tabela programa
class Programa(BaseModel, table=True):
    __tablename__ = "programa"
    
    id: int = Field(primary_key=True)
    id_programa: int = Field(primary_key=True)
    cod_orgao_sup_programa: str | None = None
    desc_orgao_sup_programa: str | None = None
    cod_programa: str | None = None
    nome_programa: str | None = None
    sit_programa: str | None = None
    data_disponibilizacao: date | None = None
    ano_disponibilizacao: str | None = None
    dt_prog_ini_receb_prop: date | None = None
    dt_prog_fim_receb_prop: date | None = None
    dt_prog_ini_emenda_par: date | None = None
    dt_prog_fim_emenda_par: date | None = None
    dt_prog_ini_benef_esp: date | None = None
    dt_prog_fim_benef_esp: date | None = None
    modalidade_programa: str | None = None
    natureza_juridica_programa: str | None = None
    uf_programa: str | None = None
    acao_orcamentaria: str | None = None
    nome_subtipo_programa: str | None = None
    descricao_subtipo_programa: str | None = None
    
    # Add relationship to proponentes
    proponentes: list["Proponente"] = Relationship(
        back_populates="programas",
        link_model=ProgramaProponentes
    )
    # Add relationship to propostas
    propostas: list["Proposta"] = Relationship(
        back_populates="programas",
        link_model=ProgramaProposta
    )

# Tabela proponente
class Proponente(BaseModel, table=True):
    __tablename__ = "proponentes"
    
    id_proponente: int = Field(primary_key=True)
    identif_proponente: str | None = None
    nm_proponente: str | None = None
    municipio_proponente: str | None = None
    uf_proponente: str | None = None
    endereco_proponente: str | None = None
    bairro_proponente: str | None = None
    cep_proponente: str | None = None
    email_proponente: str | None = None
    telefone_proponente: str | None = None
    fax_proponente: str | None = None
    
    # Add relationship to programas
    programas: list["Programa"] = Relationship(
        back_populates="proponentes",
        link_model=ProgramaProponentes
    )

# Tabela proposta
class Proposta(BaseModel, table=True):
    __tablename__ = "proposta"
    
    id_proposta: int = Field(primary_key=True)
    id_proponente: int = Field(foreign_key=f"{db_schema}.proponentes.id_proponente")
    uf_proponente: str | None = None
    munic_proponente: str | None = None
    cod_munic_ibge: str | None = None
    cod_orgao_sup: str | None = None
    desc_orgao_sup: str | None = None
    natureza_juridica: str | None = None
    nr_proposta: str | None = None
    dia_prop: str | None = None
    mes_prop: str | None = None
    ano_prop: str | None = None
    dia_proposta: date | None = None
    cod_orgao: str | None = None
    desc_orgao: str | None = None
    modalidade: str | None = None
    identif_proponente: str | None = None
    nm_proponente: str | None = None
    cep_proponente: str | None = None
    endereco_proponente: str | None = None
    bairro_proponente: str | None = None
    nm_banco: str | None = None
    situacao_conta: str | None = None
    situacao_projeto_basico: str | None = None
    sit_proposta: str | None = None
    dia_inic_vigencia_proposta: date | None = None
    dia_fim_vigencia_proposta: date | None = None
    objeto_proposta: str | None = None
    item_investimento: str | None = None
    enviada_mandataria: str | None = None
    vl_global_prop: float | None = None
    vl_repasse_prop: float | None = None
    vl_contrapartida_prop: float | None = None
    nome_subtipo_proposta: str | None = None
    descricao_subtipo_proposta: str | None = None
    cd_agencia: str | None = None
    cd_conta: str | None = None
    
    # Add relationship to programas
    programas: list["Programa"] = Relationship(
        back_populates="propostas",
        link_model=ProgramaProposta
    )

# Tabela justificativas_proposta
class JustificativasProposta(BaseModel, table=True):
    __tablename__ = "justificativas_proposta"
    
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)    
    caracterizacao_interesses_reci: str | None = None
    publico_alvo: str | None = None
    problema_a_ser_resolvido: str | None = None
    resultados_esperados: str | None = None
    relacao_proposta_objetivos_pro: str | None = None
    capacidade_tecnica: str | None = None
    justificativa: str | None = None

# Tabela proposta_cancelada
class PropostaCancelada(BaseModel, table=True):
    __tablename__ = "proposta_cancelada"
    
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)
    uf_proponente: str | None = None
    munic_proponente: str | None = None
    cod_munic_ibge: str | None = None
    cod_orgao_sup: str | None = None
    desc_orgao_sup: str | None = None
    natureza_juridica: str | None = None
    nr_proposta: str | None = None
    dia_prop: int | None = None
    mes_prop: int | None = None
    ano_prop: int | None = None
    dia_proposta: date | None = None
    cod_orgao: str | None = None
    desc_orgao: str | None = None
    modalidade: str | None = None
    identif_proponente: str | None = None
    nm_proponente: str | None = None
    cep_proponente: str | None = None
    endereco_proponente: str | None = None
    bairro_proponente: str | None = None
    nm_banco: str | None = None
    situacao_conta: str | None = None
    situacao_projeto_basico: str | None = None
    sit_proposta: str | None = None
    dia_inic_vigencia_proposta: date | None = None
    dia_fim_vigencia_proposta: date | None = None
    objeto_proposta: str | None = None
    item_investimento: str | None = None
    enviada_mandataria: str | None = None
    vl_global_prop: float | None = None
    vl_repasse_prop: float | None = None
    vl_contrapartida_prop: float | None = None
    nome_subtipo_proposta: str | None = None
    descricao_subtipo_proposta: str | None = None


class PropostaSelecaoPac(BaseModel, table=True):
    __tablename__ = "proposta_selecao_pac"
    
    id_proposta_selecao_pac: int = Field(primary_key=True)
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa")
    id_proponente: int = Field(foreign_key=f"{db_schema}.proponentes.id_proponente")
    nr_proposta_selecao_pac: str | None = None
    data_cadastro_proposta_selecao_pac: datetime | None = None
    data_envio_proposta_selecao_pac: datetime | None = None
    objeto_proposta_selecao_pac: str | None = None
    situacao_proposta_selecao_pac: str | None = None
    valor_total_proposta_selecao_pac: float | None = None
    justificativa_proposta_selecao_pac: str | None = None
    tem_anexo_proposta_selecao_pac: str | None = None


class PerguntaSelecaoPac(BaseModel, table=True):
    __tablename__ = "pergunta_selecao_pac"
    
    id_pergunta_selecao_pac: int = Field(primary_key=True)
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa")
    pergunta_selecao_pac: str | None = None


class RespostaSelecaoPac(BaseModel, table=True):
    __tablename__ = "resposta_selecao_pac"

    id_pergunta_selecao_pac: int = Field(primary_key=True, foreign_key=f"{db_schema}.pergunta_selecao_pac.id_pergunta_selecao_pac")
    id_proposta_selecao_pac: int = Field(primary_key=True, foreign_key=f"{db_schema}.proposta_selecao_pac.id_proposta_selecao_pac")
    resposta_selecao_pac: str | None = None
    

class PropostaFormalizacaoPac(BaseModel, table=True):
    __tablename__ = "proposta_formalizacao_pac"
    
    id_proposta_selecao_pac: int = Field(foreign_key=f"{db_schema}.proposta_selecao_pac.id_proposta_selecao_pac", primary_key=True)
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)
    nr_reservado_pac: str | None = None


class PlanoAplicacaoDetalhado(BaseModel, table=True):
    __tablename__ = "plano_aplicacao_detalhado"
    
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)
    sigla: str | None = None
    municipio: str | None = None
    natureza_aquisicao: int | None = None
    descricao_item: str | None = None
    cep_item: str | None = None
    endereco_item: str | None = None
    tipo_despesa_item: str | None = None
    natureza_despesa: str | None = None
    sit_item: str | None = None
    cod_natureza_despesa: str | None = None
    qtd_item: int | None = None
    valor_unitario_item: float | None = None
    valor_total_item: float | None = None
    id_item_pad: int = Field(primary_key=True)


class Emenda(BaseModel, table=True):
    __tablename__ = "emenda"
    
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)
    qualif_proponente: str | None = None
    cod_programa_emenda: str = Field(primary_key=True)
    nr_emenda: int | None = Field(primary_key=True)
    nome_parlamentar: str | None = None
    beneficiario_emenda: str | None = None
    ind_impositivo: str | None = None
    tipo_parlamentar: str | None = None
    valor_repasse_proposta_emenda: float | None = None
    valor_repasse_emenda: float | None = None


class Convenio(BaseModel, table=True):
    __tablename__ = "convenio"

    nr_convenio: int = Field(primary_key=True)
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)
    dia: int | None = None
    mes: int | None = None
    ano: int | None = None
    dia_assin_conv: date | None = None
    sit_convenio: str | None = None
    subsituacao_conv: str | None = None
    situacao_publicacao: str | None = None
    instrumento_ativo: str | None = None
    ind_opera_obtv: str | None = None
    nr_processo: str | None = None
    ug_emitente: str | None = None
    dia_publ_conv: date | None = None
    dia_inic_vigenc_conv: date | None = None
    dia_fim_vigenc_conv: date | None = None
    dia_fim_vigenc_original_conv: date | None = None
    dias_prest_contas: int | None = None
    dia_limite_prest_contas: date | None = None
    data_suspensiva: date | None = None
    data_retirada_suspensiva: date | None = None
    dias_clausula_suspensiva: int | None = None
    situacao_contratacao: str | None = None
    ind_assinado: str | None = None
    motivo_suspensao: str | None = None
    ind_foto: str | None = None
    qtde_convenios: int | None = None
    qtd_ta: int | None = None
    qtd_proroga: int | None = None
    vl_global_conv: float | None = None
    vl_repasse_conv: float | None = None
    vl_contrapartida_conv: float | None = None
    vl_empenhado_conv: float | None = None
    vl_desembolsado_conv: float | None = None
    vl_saldo_reman_tesouro: float | None = None
    vl_saldo_reman_convenente: float | None = None
    vl_rendimento_aplicacao: float | None = None
    vl_ingresso_contrapartida: float | None = None
    vl_saldo_conta: float | None = None
    valor_global_original_conv: float | None = None


class IngressoContrapartida(BaseModel, table=True):
    __tablename__ = "ingresso_contrapartida"
    
    nr_convenio: int = Field(foreign_key=f"{db_schema}.convenio.nr_convenio", primary_key=True)
    dt_ingresso_contrapartida: date | None = Field(primary_key=True)
    vl_ingresso_contrapartida: float | None = Field(primary_key=True)


class MetaCronoFisico(BaseModel, table=True):
    __tablename__ = "meta_crono_fisico"
    
    id_meta: int = Field(primary_key=True)
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta")
    nr_convenio: int = Field(foreign_key=f"{db_schema}.convenio.nr_convenio")
    cod_programa: str | None = None
    nome_programa: str | None = None
    nr_meta: str | None = None
    tipo_meta: str | None = None
    desc_meta: str | None = None
    data_inicio_meta: date | None = None
    data_fim_meta: date | None = None
    uf_meta: str | None = None
    municipio_meta: str | None = None
    endereco_meta: str | None = None
    cep_meta: str | None = None
    qtd_meta: int | None = None
    und_fornecimento_meta: str | None = None
    vl_meta: float | None = None


class EtapaCronoFisico(BaseModel, table=True):
    __tablename__ = "etapa_crono_fisico"
    
    id_etapa: int = Field(primary_key=True)
    id_meta: int = Field(foreign_key=f"{db_schema}.meta_crono_fisico.id_meta")
    nr_etapa: int | None = None
    desc_etapa: str | None = None
    data_inicio_etapa: date | None = None
    data_fim_etapa: date | None = None
    uf_etapa: str | None = None
    municipio_etapa: str | None = None
    endereco_etapa: str | None = None
    cep_etapa: str | None = None
    qtd_etapa: int | None = None
    und_fornecimento_etapa: str | None = None
    vl_etapa: float | None = None


class HistoricoSituacao(BaseModel, table=True):
    __tablename__ = "historico_situacao"

    id_proposta: int = Field(primary_key=True, foreign_key=f"{db_schema}.proposta.id_proposta")
    nr_convenio: int = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    dia_historico_sit: datetime | None  = Field(primary_key=True)
    historico_sit: str | None = None
    dias_historico_sit: int | None = None
    cod_historico_sit: int | None = None


class SolicitacaoAlteracao(BaseModel, table=True):
    __tablename__ = "solicitacao_alteracao"

    id_solicitacao: int = Field(primary_key=True)
    nr_convenio: int | None = Field(foreign_key=f"{db_schema}.convenio.nr_convenio")
    nr_solicitacao: str | None = None
    situacao_solicitacao: str | None = None
    objeto_solicitacao: str | None = None
    data_solicitacao: date | None = None


class TermoAditivo(BaseModel, table=True):
    __tablename__ = "termo_aditivo"

    # Assuming composite primary key based on DDL constraints and common patterns
    # Adjust if the actual primary key is different
    nr_convenio: int | None = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    id_solicitacao: int | None = Field(primary_key=True, foreign_key=f"{db_schema}.solicitacao_alteracao.id_solicitacao")
    numero_ta: str | None = Field(primary_key=True) # Assuming numero_ta helps form uniqueness    
    tipo_ta: str | None = None
    vl_global_ta: float | None = None
    vl_repasse_ta: float | None = None
    vl_contrapartida_ta: float | None = None
    dt_assinatura_ta: date | None = None
    dt_inicio_ta: date | None = None
    dt_fim_ta: date | None = None
    justificativa_ta: str | None = None


class ProrrogaOficio(BaseModel, table=True):
    __tablename__ = "prorroga_oficio"

    nr_convenio: int = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    nr_prorroga: str = Field(primary_key=True) # Assuming nr_prorroga is part of a composite PK
    dt_inicio_prorroga: date | None = None
    dt_fim_prorroga: date = Field(primary_key=True)
    dias_prorroga: int | None = None
    dt_assinatura_prorroga: date | None = None
    sit_prorroga: str | None = None


class EmpenhoDesembolso(BaseModel, table=True):
    __tablename__ = "empenho_desembolso"

    id_desembolso: int = Field(primary_key=True, foreign_key=f"{db_schema}.desembolso.id_desembolso")
    id_empenho: int = Field(primary_key=True, foreign_key=f"{db_schema}.empenho.id_empenho")
    valor_grupo: float | None = None 

    # Relationships back to Empenho and Desembolso
    # empenho_model refers to the Empenho instance this link object belongs to.
    empenho_model: Optional["Empenho"] = Relationship(back_populates="desembolsos") 
    # desembolso_model refers to the Desembolso instance this link object belongs to.
    desembolso_model: Optional["Desembolso"] = Relationship(back_populates="empenho_details")


class Empenho(BaseModel, table=True):
    __tablename__ = "empenho"

    id_empenho: int = Field(primary_key=True)
    nr_convenio: int = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    nr_empenho: str | None = None
    tipo_nota: str | None = None
    desc_tipo_nota: str | None = None
    data_emissao: date | None = None
    cod_situacao_empenho: str | None = None 
    desc_situacao_empenho: str | None = None
    ug_emitente: str | None = None
    ug_responsavel: str | None = None
    fonte_recurso: str | None = None
    natureza_despesa: str | None = None
    plano_interno: str | None = None
    ptres: str | None = None
    valor_empenho: float | None = None

    # This relationship will provide a list of EmpenhoDesembolso (link model) instances.
    # The name 'desembolsos' matches the field in EmpenhoResponse schema.
    desembolsos: list["EmpenhoDesembolso"] = Relationship(back_populates="empenho_model")


class Desembolso(BaseModel, table=True):
    __tablename__ = "desembolso"

    id_desembolso: int = Field(primary_key=True)
    nr_convenio: int | None = Field(foreign_key=f"{db_schema}.convenio.nr_convenio")
    dt_ult_desembolso: date | None = None
    qtd_dias_sem_desembolso: int | None = None
    data_desembolso: date | None = None
    ano_desembolso: int | None = None
    mes_desembolso: int | None = None
    nr_siafi: str | None = None
    ug_emitente_dh: str | None = None
    observacao_dh: str | None = None
    vl_desembolsado: float | None = None

    empenho_details: list["EmpenhoDesembolso"] = Relationship(back_populates="desembolso_model")


class DesbloqueioCr(BaseModel, table=True):
    __tablename__ = "desbloqueio_cr"

    nr_convenio: int = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    nr_ob: str | None = Field(primary_key=True)
    data_cadastro: datetime | None = Field(primary_key=True)
    data_envio: datetime | None = None
    tipo_recurso_desbloqueio: str | None = None
    vl_total_desbloqueio: float | None = None
    vl_desbloqueado: float | None = None
    vl_bloqueado: float | None = None


class CronogramaDesembolso(BaseModel, table=True):
    __tablename__ = "cronograma_desembolso"
    
    id_proposta: int = Field(primary_key=True, foreign_key=f"{db_schema}.proposta.id_proposta")
    nr_convenio: int | None = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    nr_parcela_crono_desembolso: int | None = Field(primary_key=True)
    mes_crono_desembolso: int | None = None
    ano_crono_desembolso: int | None = None
    tipo_resp_crono_desembolso: str | None = None
    valor_parcela_crono_desembolso: float | None = None


class Pagamento(BaseModel, table=True):
    __tablename__ = "pagamento"

    nr_mov_fin: int = Field(primary_key=True)
    nr_convenio: int | None = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    identif_fornecedor: str | None = None
    nome_fornecedor: str | None = None
    tp_mov_financeira: str | None = None
    data_pag: date | None = None
    nr_dl: str | None = None
    desc_dl: str | None = None
    vl_pago: float | None = None


class ObtvConvenente(BaseModel, table=True):
    __tablename__ = "obtv_convenente"

    nr_mov_fin: Optional[int] = Field(primary_key=True, foreign_key=f"{db_schema}.pagamento.nr_mov_fin")
    identif_favorecido_obtv_conv: str | None = Field(primary_key=True)
    nm_favorecido_obtv_conv: str | None = None
    tp_aquisicao: str | None = None
    vl_pago_obtv_conv: float | None = None


class PagamentoTributo(BaseModel, table=True):
    __tablename__ = "pagamento_tributo"

    nr_convenio: int = Field(primary_key=True, foreign_key=f"{db_schema}.convenio.nr_convenio")
    data_tributo: date | None = Field(primary_key=True)
    vl_pag_tributos: float | None = None


class Licitacao(BaseModel, table=True):
    __tablename__ = "licitacao"
    
    id_licitacao: int = Field(primary_key=True)
    nr_convenio: int = Field(foreign_key=f"{db_schema}.convenio.nr_convenio")
    nr_licitacao: str | None = None
    modalidade_licitacao: str | None = None
    tp_processo_compra: str | None = None
    tipo_licitacao: str | None = None
    nr_processo_licitacao: str | None = None
    data_publicacao_licitacao: date | None = None
    data_abertura_licitacao: date | None = None
    data_encerramento_licitacao: date | None = None
    data_homologacao_licitacao: date | None = None
    status_licitacao: str | None = None
    situacao_aceite_processo_execu: str | None = None
    sistema_origem: str | None = None
    situacao_sistema: str | None = None
    valor_licitacao: float | None = None


class Contrato(BaseModel, table=True):
    __tablename__ = "contrato"
    
    id_licitacao: int = Field(foreign_key=f"{db_schema}.licitacao.id_licitacao", primary_key=True)
    nr_contrato: int = Field(primary_key=True)
    data_publicacao_contrato: str | None = None
    data_assinatura_contrato: date | None = None
    data_inicio_vigencia_contrato: date | None = None
    data_fim_vigencia_contrato: date | None = None
    objeto_contrato: str | None = None
    tipo_aquisicao_contrato: str | None = None
    valor_global_contrato: float | None = None
    id_fornecedor_contrato: str | None = None
    nome_fornecedor_contrato: str | None = None


