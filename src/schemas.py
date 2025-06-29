from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Any
from datetime import date, datetime


# Template para paginacao
class PaginatedResponseTemplate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    data: List[Any]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int
# --------------------------------------


class ProponenteSimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    id_proponente: Optional[int]


class ProponenteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proponente: Optional[int]
    identif_proponente: Optional[str]
    nm_proponente: Optional[str]
    municipio_proponente: Optional[str]
    uf_proponente: Optional[str]
    endereco_proponente: Optional[str]
    bairro_proponente: Optional[str]
    cep_proponente: Optional[str]
    email_proponente: Optional[str]
    telefone_proponente: Optional[str]
    fax_proponente: Optional[str]


class PaginatedProponenteResponse(PaginatedResponseTemplate):
    data: List[ProponenteResponse]


class PropostaSimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    id_proposta: Optional[int]


class PropostaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    id_proponente: Optional[int]    
    uf_proponente: Optional[str]
    munic_proponente: Optional[str]
    cod_munic_ibge: Optional[str]
    cod_orgao_sup: Optional[str]
    desc_orgao_sup: Optional[str]
    natureza_juridica: Optional[str]
    nr_proposta: Optional[str]
    dia_prop: Optional[str]
    mes_prop: Optional[str]
    ano_prop: Optional[str]
    dia_proposta: Optional[date]
    cod_orgao: Optional[str]
    desc_orgao: Optional[str]
    modalidade: Optional[str]
    identif_proponente: Optional[str]
    nm_proponente: Optional[str]
    cep_proponente: Optional[str]
    endereco_proponente: Optional[str]
    bairro_proponente: Optional[str]
    nm_banco: Optional[str]
    situacao_conta: Optional[str]
    situacao_projeto_basico: Optional[str]
    sit_proposta: Optional[str]
    dia_inic_vigencia_proposta: Optional[date]
    dia_fim_vigencia_proposta: Optional[date]
    objeto_proposta: Optional[str]
    item_investimento: Optional[str]
    enviada_mandataria: Optional[str]
    vl_global_prop: Optional[float]
    vl_repasse_prop: Optional[float]
    vl_contrapartida_prop: Optional[float]
    nome_subtipo_proposta: Optional[str]
    descricao_subtipo_proposta: Optional[str]
    cd_agencia: Optional[str]
    cd_conta: Optional[str]


class PaginatedPropostaResponse(PaginatedResponseTemplate):
    data: List[PropostaResponse]


class ProgramaResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id: Optional[int] = Field(exclude=True)
    id_programa: Optional[int]
    cod_orgao_sup_programa: Optional[str]
    desc_orgao_sup_programa: Optional[str]
    cod_programa: Optional[str]
    nome_programa: Optional[str]
    sit_programa: Optional[str]
    data_disponibilizacao: Optional[date]
    ano_disponibilizacao: Optional[str]
    dt_prog_ini_receb_prop: Optional[date]
    dt_prog_fim_receb_prop: Optional[date]
    dt_prog_ini_emenda_par: Optional[date]
    dt_prog_fim_emenda_par: Optional[date]
    dt_prog_ini_benef_esp: Optional[date]
    dt_prog_fim_benef_esp: Optional[date]
    modalidade_programa: Optional[str]
    natureza_juridica_programa: Optional[str]
    uf_programa: Optional[str]
    acao_orcamentaria: Optional[str]
    nome_subtipo_programa: Optional[str]
    descricao_subtipo_programa: Optional[str]
    proponentes: Optional[List[ProponenteSimpleResponse]] = []
    propostas: Optional[List[PropostaSimpleResponse]] = []


class PaginatedProgramaResponse(PaginatedResponseTemplate):
    data: List[ProgramaResponse]


class JustificativasPropostaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    caracterizacao_interesses_reci: Optional[str]
    publico_alvo: Optional[str]
    problema_a_ser_resolvido: Optional[str]
    resultados_esperados: Optional[str]
    relacao_proposta_objetivos_pro: Optional[str]
    capacidade_tecnica: Optional[str]
    justificativa: Optional[str]
   

class PaginatedJustificativasPropostaResponse(PaginatedResponseTemplate):
    data: List[JustificativasPropostaResponse]


class PropostaCanceladaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    uf_proponente: Optional[str]
    munic_proponente: Optional[str]
    cod_munic_ibge: Optional[str]
    cod_orgao_sup: Optional[str]
    desc_orgao_sup: Optional[str]
    natureza_juridica: Optional[str]
    nr_proposta: Optional[str]
    dia_prop: Optional[int]
    mes_prop: Optional[int]
    ano_prop: Optional[int]
    dia_proposta: Optional[date]
    cod_orgao: Optional[str]
    desc_orgao: Optional[str]
    modalidade: Optional[str]
    identif_proponente: Optional[str]
    nm_proponente: Optional[str]
    cep_proponente: Optional[str]
    endereco_proponente: Optional[str]
    bairro_proponente: Optional[str]
    nm_banco: Optional[str]
    situacao_conta: Optional[str]
    situacao_projeto_basico: Optional[str]
    sit_proposta: Optional[str]
    dia_inic_vigencia_proposta: Optional[date]
    dia_fim_vigencia_proposta: Optional[date]
    objeto_proposta: Optional[str]
    item_investimento: Optional[str]
    enviada_mandataria: Optional[str]
    vl_global_prop: Optional[float]
    vl_repasse_prop: Optional[float]
    vl_contrapartida_prop: Optional[float]
    nome_subtipo_proposta: Optional[str]
    descricao_subtipo_proposta: Optional[str]


class PaginatedPropostaCanceladaResponse(PaginatedResponseTemplate):
    data: List[PropostaCanceladaResponse]


class PropostaSelecaoPacResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta_selecao_pac: Optional[int]
    id_programa: Optional[int]
    id_proponente: Optional[int]
    nr_proposta_selecao_pac: Optional[str]
    data_cadastro_proposta_selecao_pac: Optional[datetime]
    data_envio_proposta_selecao_pac: Optional[datetime]
    objeto_proposta_selecao_pac: Optional[str]
    situacao_proposta_selecao_pac: Optional[str]
    valor_total_proposta_selecao_pac: Optional[float]
    justificativa_proposta_selecao_pac: Optional[str]
    tem_anexo_proposta_selecao_pac: Optional[str]


class PaginatedPropostaSelecaoPacResponse(PaginatedResponseTemplate):
    data: List[PropostaSelecaoPacResponse]


class PerguntaSelecaoPacResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_pergunta_selecao_pac: Optional[int]
    id_programa: Optional[int]
    pergunta_selecao_pac: Optional[str]


class PaginatedPerguntaSelecaoPacResponse(PaginatedResponseTemplate):
    data: List[PerguntaSelecaoPacResponse]


class RespostaSelecaoPacResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_pergunta_selecao_pac: Optional[int]
    id_proposta_selecao_pac: Optional[int]
    resposta_selecao_pac: Optional[str]


class PaginatedRespostaSelecaoPacResponse(PaginatedResponseTemplate):
    data: List[RespostaSelecaoPacResponse]


class PropostaFormalizacaoPacResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta_selecao_pac: Optional[int]
    id_proposta: Optional[int]
    nr_reservado_pac: Optional[str]


class PaginatedPropostaFormalizacaoPacResponse(PaginatedResponseTemplate):
    data: List[PropostaFormalizacaoPacResponse]


class PlanoAplicacaoDetalhadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    sigla: Optional[str]
    municipio: Optional[str]
    natureza_aquisicao: Optional[int]
    descricao_item: Optional[str]
    cep_item: Optional[str]
    endereco_item: Optional[str]
    tipo_despesa_item: Optional[str]
    natureza_despesa: Optional[str]
    sit_item: Optional[str]
    cod_natureza_despesa: Optional[str]
    qtd_item: Optional[int]
    valor_unitario_item: Optional[float]
    valor_total_item: Optional[float]
    id_item_pad: Optional[int]


class PaginatedPlanoAplicacaoDetalhadoResponse(PaginatedResponseTemplate):
    data: List[PlanoAplicacaoDetalhadoResponse]


class EmendaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    qualif_proponente: Optional[str]
    cod_programa_emenda: Optional[str]
    nr_emenda: Optional[int]
    nome_parlamentar: Optional[str]
    beneficiario_emenda: Optional[str]
    ind_impositivo: Optional[str]
    tipo_parlamentar: Optional[str]
    valor_repasse_proposta_emenda: Optional[float]
    valor_repasse_emenda: Optional[float]


class PaginatedEmendaResponse(PaginatedResponseTemplate):
    data: List[EmendaResponse]


class ConvenioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    nr_convenio: Optional[int]
    id_proposta: Optional[int]
    dia: Optional[int]
    mes: Optional[int]
    ano: Optional[int]
    dia_assin_conv: Optional[date]
    sit_convenio: Optional[str]
    subsituacao_conv: Optional[str]
    situacao_publicacao: Optional[str]
    instrumento_ativo: Optional[str]
    ind_opera_obtv: Optional[str]
    nr_processo: Optional[str]
    ug_emitente: Optional[str]
    dia_publ_conv: Optional[date]
    dia_inic_vigenc_conv: Optional[date]
    dia_fim_vigenc_conv: Optional[date]
    dia_fim_vigenc_original_conv: Optional[date]
    dias_prest_contas: Optional[int]
    dia_limite_prest_contas: Optional[date]
    data_suspensiva: Optional[date]
    data_retirada_suspensiva: Optional[date]
    dias_clausula_suspensiva: Optional[int]
    situacao_contratacao: Optional[str]
    ind_assinado: Optional[str]
    motivo_suspensao: Optional[str]
    ind_foto: Optional[str]
    qtde_convenios: Optional[int]
    qtd_ta: Optional[int]
    qtd_proroga: Optional[int]
    vl_global_conv: Optional[float]
    vl_repasse_conv: Optional[float]
    vl_contrapartida_conv: Optional[float]
    vl_empenhado_conv: Optional[float]
    vl_desembolsado_conv: Optional[float]
    vl_saldo_reman_tesouro: Optional[float]
    vl_saldo_reman_convenente: Optional[float]
    vl_rendimento_aplicacao: Optional[float]
    vl_ingresso_contrapartida: Optional[float]
    vl_saldo_conta: Optional[float]
    valor_global_original_conv: Optional[float]


class PaginatedConvenioResponse(PaginatedResponseTemplate):
    data: List[ConvenioResponse]


class IngressoContrapartidaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    nr_convenio: Optional[int]
    dt_ingresso_contrapartida: Optional[date]
    vl_ingresso_contrapartida: Optional[float]


class PaginatedIngressoContrapartidaResponse(PaginatedResponseTemplate):
    data: List[IngressoContrapartidaResponse]


class MetaCronoFisicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_meta: Optional[int]
    id_proposta: Optional[int]
    nr_convenio: Optional[int]
    cod_programa: Optional[str]
    nome_programa: Optional[str]
    nr_meta: Optional[str]
    tipo_meta: Optional[str]
    desc_meta: Optional[str]
    data_inicio_meta: Optional[date]
    data_fim_meta: Optional[date]
    uf_meta: Optional[str]
    municipio_meta: Optional[str]
    endereco_meta: Optional[str]
    cep_meta: Optional[str]
    qtd_meta: Optional[int]
    und_fornecimento_meta: Optional[str]
    vl_meta: Optional[float]


class PaginatedMetaCronoFisicoResponse(PaginatedResponseTemplate):
    data: List[MetaCronoFisicoResponse] 


class EtapaCronoFisicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_etapa: Optional[int]
    id_meta: Optional[int]
    nr_etapa: Optional[int]
    desc_etapa: Optional[str]
    data_inicio_etapa: Optional[date]
    data_fim_etapa: Optional[date]
    uf_etapa: Optional[str]
    municipio_etapa: Optional[str]
    endereco_etapa: Optional[str]
    cep_etapa: Optional[str]
    qtd_etapa: Optional[int]
    und_fornecimento_etapa: Optional[str]
    vl_etapa: Optional[float]


class PaginatedEtapaCronoFisicoResponse(PaginatedResponseTemplate):
    data: List[EtapaCronoFisicoResponse] 


class HistoricoSituacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    nr_convenio: Optional[int]
    dia_historico_sit: Optional[datetime]
    historico_sit: Optional[str]
    dias_historico_sit: Optional[int]
    cod_historico_sit: Optional[int]


class PaginatedHistoricoSituacaoResponse(PaginatedResponseTemplate):
    data: List[HistoricoSituacaoResponse] 


class SolicitacaoAlteracaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_solicitacao: Optional[int]
    nr_convenio: Optional[int]
    nr_solicitacao: Optional[str]
    situacao_solicitacao: Optional[str]
    objeto_solicitacao: Optional[str]
    data_solicitacao: Optional[date]


class PaginatedSolicitacaoAlteracaoResponse(PaginatedResponseTemplate):
    data: List[SolicitacaoAlteracaoResponse]


class TermoAditivoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    nr_convenio: Optional[int]
    id_solicitacao: Optional[int]
    numero_ta: Optional[str]
    tipo_ta: Optional[str]
    vl_global_ta: Optional[float]
    vl_repasse_ta: Optional[float]
    vl_contrapartida_ta: Optional[float]
    dt_assinatura_ta: Optional[date]
    dt_inicio_ta: Optional[date]
    dt_fim_ta: Optional[date]
    justificativa_ta: Optional[str]


class PaginatedTermoAditivoResponse(PaginatedResponseTemplate):
    data: List[TermoAditivoResponse] 


class ProrrogaOficioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    nr_convenio: Optional[int]
    nr_prorroga: Optional[str]
    dt_inicio_prorroga: Optional[date]
    dt_fim_prorroga: Optional[date]
    dias_prorroga: Optional[int]
    dt_assinatura_prorroga: Optional[date]
    sit_prorroga: Optional[str]


class PaginatedProrrogaOficioResponse(PaginatedResponseTemplate):
    data: List[ProrrogaOficioResponse] 


class EmpenhoDesembolsoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_desembolso: Optional[int]
    valor_grupo: Optional[float]

    
class EmpenhoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_empenho: Optional[int]
    nr_convenio: Optional[int]
    nr_empenho: Optional[str]
    tipo_nota: Optional[str]
    desc_tipo_nota: Optional[str]
    data_emissao: Optional[date]
    cod_situacao_empenho: Optional[str]
    desc_situacao_empenho: Optional[str]
    ug_emitente: Optional[str]
    ug_responsavel: Optional[str]
    fonte_recurso: Optional[str]
    natureza_despesa: Optional[str]
    plano_interno: Optional[str]
    ptres: Optional[str]
    valor_empenho: Optional[float]
    desembolsos: Optional[List[EmpenhoDesembolsoResponse]] = []


class PaginatedEmpenhoResponse(PaginatedResponseTemplate):
    data: List[EmpenhoResponse] 


class DesembolsoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_desembolso: Optional[int]
    nr_convenio: Optional[int]
    dt_ult_desembolso: Optional[date]
    qtd_dias_sem_desembolso: Optional[int]
    data_desembolso: Optional[date]
    ano_desembolso: Optional[int]
    mes_desembolso: Optional[int]
    nr_siafi: Optional[str]
    ug_emitente_dh: Optional[str]
    observacao_dh: Optional[str]
    vl_desembolsado: Optional[float]


class PaginatedDesembolsoResponse(PaginatedResponseTemplate):
    data: List[DesembolsoResponse]


class DesbloqueioCrResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    nr_convenio: Optional[int]
    nr_ob: Optional[str]
    data_cadastro: Optional[datetime]
    data_envio: Optional[datetime]
    tipo_recurso_desbloqueio: Optional[str]
    vl_total_desbloqueio: Optional[float]
    vl_desbloqueado: Optional[float]
    vl_bloqueado: Optional[float]


class PaginatedDesbloqueioCrResponse(PaginatedResponseTemplate):
    data: List[DesbloqueioCrResponse]


class CronogramaDesembolsoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    nr_convenio: Optional[int]
    nr_parcela_crono_desembolso: Optional[int]
    mes_crono_desembolso: Optional[int]
    ano_crono_desembolso: Optional[int]
    tipo_resp_crono_desembolso: Optional[str]
    valor_parcela_crono_desembolso: Optional[float]


class PaginatedCronogramaDesembolsoResponse(PaginatedResponseTemplate):
    data: List[CronogramaDesembolsoResponse]


class PagamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    nr_mov_fin: Optional[int]
    nr_convenio: Optional[int]
    identif_fornecedor: Optional[str]
    nome_fornecedor: Optional[str]
    tp_mov_financeira: Optional[str]
    data_pag: Optional[date]
    nr_dl: Optional[str]
    desc_dl: Optional[str]
    vl_pago: Optional[float]


class PaginatedPagamentoResponse(PaginatedResponseTemplate):
    data: List[PagamentoResponse]


class ObtvConvenenteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nr_mov_fin: Optional[int]
    identif_favorecido_obtv_conv: Optional[str]
    nm_favorecido_obtv_conv: Optional[str]
    tp_aquisicao: Optional[str]
    vl_pago_obtv_conv: Optional[float]


class PaginatedObtvConvenenteResponse(PaginatedResponseTemplate):
    data: list[ObtvConvenenteResponse]


class PagamentoTributoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nr_convenio: Optional[int]
    data_tributo: Optional[date]
    vl_pag_tributos: Optional[float]


class PaginatedPagamentoTributoResponse(PaginatedResponseTemplate):
    data: list[PagamentoTributoResponse]


class LicitacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_licitacao: Optional[int]
    nr_convenio: Optional[int]
    nr_licitacao: Optional[str]
    modalidade_licitacao: Optional[str]
    tp_processo_compra: Optional[str]
    tipo_licitacao: Optional[str]
    nr_processo_licitacao: Optional[str]
    data_publicacao_licitacao: Optional[date]
    data_abertura_licitacao: Optional[date]
    data_encerramento_licitacao: Optional[date]
    data_homologacao_licitacao: Optional[date]
    status_licitacao: Optional[str]
    situacao_aceite_processo_execu: Optional[str]
    sistema_origem: Optional[str]
    situacao_sistema: Optional[str]
    valor_licitacao: Optional[float]


class PaginatedLicitacaoResponse(PaginatedResponseTemplate):
    data: List[LicitacaoResponse]


class ContratoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_licitacao: Optional[int]
    nr_contrato: Optional[int]
    data_publicacao_contrato: Optional[str]
    data_assinatura_contrato: Optional[date]
    data_inicio_vigencia_contrato: Optional[date]
    data_fim_vigencia_contrato: Optional[date]
    objeto_contrato: Optional[str]
    tipo_aquisicao_contrato: Optional[str]
    valor_global_contrato: Optional[float]
    id_fornecedor_contrato: Optional[str]
    nome_fornecedor_contrato: Optional[str]


class PaginatedContratoResponse(PaginatedResponseTemplate):
    data: List[ContratoResponse]


class HistoricoProjetoBasicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    data_hist_pb_tr: Optional[date]
    situacao_hist_pb_tr: Optional[str]
    evento_hist_pb_tr: Optional[str]
    versao_doc_pb_tr: Optional[int]


class PaginatedHistoricoProjetoBasicoResponse(PaginatedResponseTemplate):
    data: List[HistoricoProjetoBasicoResponse]


class ResumoFisicoFinanceiroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    valor_total_resumo_fisico_financeiro: Optional[float]
    valor_realizado_resumo_fisico_financeiro: Optional[float]
    percentual_execucao_resumo_fisico_financeiro: Optional[float]


class PaginatedResumoFisicoFinanceiroResponse(PaginatedResponseTemplate):
    data: List[ResumoFisicoFinanceiroResponse]


class SolicitacaoAjustePtResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_ajuste_pt: Optional[int]
    id_proposta: Optional[int]
    nr_ajuste_pt: Optional[str]
    data_solicitacao_ajuste_pt: Optional[date]
    situacao_solicitacao_ajuste_pt: Optional[str]


class PaginatedSolicitacaoAjustePtResponse(PaginatedResponseTemplate):
    data: List[SolicitacaoAjustePtResponse]


class SolicitacaoRendimentoAplicacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_solicitacao_rend_aplicacao: Optional[int]
    nr_convenio: Optional[int]
    nr_solicitacao_rend_aplicacao: Optional[int]
    status_solicitacao_rend_aplicacao: Optional[str]
    data_solicitacao_rend_aplicacao: Optional[date]
    valor_solicitacao_rend_aplicacao: Optional[float]
    valor_aprovado_solicitacao_rend_aplicacao: Optional[float]


class PaginatedSolicitacaoRendimentoAplicacaoResponse(PaginatedResponseTemplate):
    data: List[SolicitacaoRendimentoAplicacaoResponse]


class CoordenadasObraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    nome_projeto_cadastro_obra: Optional[str]
    latitude_cadastro_obra: Optional[float]
    longitude_cadastro_obra: Optional[float]


class PaginatedCoordenadasObraResponse(PaginatedResponseTemplate):
    data: List[CoordenadasObraResponse]


class AcompObrasContratosMedicoesModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta: Optional[int]
    id_contrato_medicao_acompanhamento_obra: Optional[int]
    id_medicao_acompanhamento_obra: Optional[int]
    data_inicio_obra_contrato_acompanhamento_obra: Optional[date]
    cnpj_fornecedor_contrato_acompanhamento_obra: Optional[str]
    numero_medicao_acompanhamento_obra: Optional[int]
    nr_ultima_medicao_acompanhamento_obra: Optional[int]
    situacao_medicao_acompanhamento_obra: Optional[str]
    data_inicio_medicao_objeto_acompanhamento_obra: Optional[date]
    data_fim_medicao_objeto_acompanhamento_obra: Optional[date]
    qtd_dias_sem_medicao_acompanhamento_obra: Optional[int]

class PaginatedAcompObrasContratosMedicoesModuloEmpresasResponse(PaginatedResponseTemplate):
    data: list[AcompObrasContratosMedicoesModuloEmpresasResponse]


class AcompObrasValoresItensMedicaoModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_submeta_vrpl: Optional[int]
    id_contrato_medicao_acompanhamento_obra: Optional[int]
    valor_execucao_fisica_acumulada_total_acompanhamento_obra: Optional[float]
    valor_execucao_fisica_acumulada_concedente_acompanhamento_obra: Optional[float]
    valor_execucao_fisica_acumulada_convenente_acompanhamento_obra: Optional[float]
    valor_execucao_fisica_acumulada_empresa_acompanhamento_obra: Optional[float]

class PaginatedAcompObrasValoresItensMedicaoModuloEmpresasResponse(PaginatedResponseTemplate):
    data: list[AcompObrasValoresItensMedicaoModuloEmpresasResponse]


class InstContPropostaAioModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_proposta_instrumento_contratual: Optional[int]
    id_proposta: Optional[int]
    id_aio_instrumento_contratual: Optional[int]
    situacao_aio_instrumento_contratual: Optional[str]
    data_emissao_aio_instrumento_contratual: Optional[date]

class PaginatedInstContPropostaAioModuloEmpresasResponse(PaginatedResponseTemplate):
    data: list[InstContPropostaAioModuloEmpresasResponse]


class InstContContratosLotesEmpresasModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_contrato_instrumento_contratual: Optional[int]
    id_proposta_instrumento_contratual: Optional[int]
    id_lote_instrumento_contratual: Optional[int]
    numero_instrumento_contratual: Optional[str]
    situacao_instrumento_contratual: Optional[str]
    data_assinatura_instrumento_contratual: Optional[date]
    data_inicio_vigencia_instrumento_contratual: Optional[date]
    data_fim_vigencia_instrumento_contratual: Optional[date]
    numero_lote_instrumento_contratual: Optional[int]
    razao_social_empresa_executora_instrumento_contratual: Optional[str]
    tipo_identificacao_empresa_executora_instrumento_contratual: Optional[str]
    identificacao_empresa_executora_instrumento_contratual: Optional[str]

class PaginatedInstContContratosLotesEmpresasModuloEmpresasResponse(PaginatedResponseTemplate):
    data: list[InstContContratosLotesEmpresasModuloEmpresasResponse]


class InstContMetasSubmetasPoModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")
    
    id_meta_instrumento_contratual: Optional[int]
    id_submeta_instrumento_contratual: Optional[int]
    id_po_instrumento_contratual: Optional[int]
    id_proposta_instrumento_contratual: Optional[int]
    id_lote_instrumento_contratual: Optional[int]
    numero_meta_instrumento_contratual: Optional[int]
    descricao_meta_instrumento_contratual: Optional[str]
    numero_submeta_instrumento_contratual: Optional[str]
    descricao_submeta_instrumento_contratual: Optional[str]
    situacao_submeta_instrumento_contratual: Optional[str]
    valor_total_licitado_instrumento_contratual: Optional[float]
    data_previsao_inicio_obra_instrumento_contratual: Optional[date]
    database_po_vrpl_instrumento_contratual: Optional[date]
    sigla_localidade_po_instrumento_contratual: Optional[str]
    acompanhado_por_evento_po_instrumento_contratual: Optional[int]

class PaginatedInstContMetasSubmetasPoModuloEmpresasResponse(PaginatedResponseTemplate):
    data: list[InstContMetasSubmetasPoModuloEmpresasResponse]


class ProjetoBasicoAcffoModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_acffo: Optional[int]
    id_proposta: Optional[int]
    ultima_versao_projeto_basico: Optional[int]
    apelido_empreendimento_projeto_basico: Optional[str]
    situacao_projeto_basico: Optional[str]
    situacao_spa: Optional[str]
    data_aceite_projeto_basico: Optional[datetime]

class PaginatedProjetoBasicoAcffoModuloEmpresasResponse(PaginatedResponseTemplate):
    data: List[ProjetoBasicoAcffoModuloEmpresasResponse]


class ProjetoBasicoLaeModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_qci_acffo: Optional[int]
    id_acffo: Optional[int]
    id_proposta: Optional[int]
    situacao_lae_projeto_basico: Optional[str]
    emissao_lae_projeto_basico: Optional[str]
    data_emissao_lae_projeto_basico: Optional[datetime]

class PaginatedProjetoBasicoLaeModuloEmpresasResponse(PaginatedResponseTemplate):
    data: List[ProjetoBasicoLaeModuloEmpresasResponse]


class ProjetoBasicoMetasModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_meta_projeto_basico: Optional[int]
    id_qci_acffo: Optional[int]
    numero_meta_projeto_basico: Optional[int]
    descricao_meta_projeto_basico: Optional[str]
    nome_item_investimento_meta: Optional[str]
    descricao_subitem_investimento_meta: Optional[str]
    quantidade_itens_meta_projeto_basico: Optional[float]
    unidade_item_investimento_meta: Optional[str]

class PaginatedProjetoBasicoMetasModuloEmpresasResponse(PaginatedResponseTemplate):
    data: List[ProjetoBasicoMetasModuloEmpresasResponse]


class ProjetoBasicoPropostaModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_proposta_acffo: Optional[int]
    id_proposta: Optional[int]
    valor_global_proposta_projeto_basico: Optional[float]

class PaginatedProjetoBasicoPropostaModuloEmpresasResponse(PaginatedResponseTemplate):
    data: List[ProjetoBasicoPropostaModuloEmpresasResponse]


class ProjetoBasicoSubmetasModuloEmpresasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_submeta_projeto_basico: Optional[int]
    id_meta_projeto_basico: Optional[int]
    lote_submeta_projeto_basico: Optional[int]
    numero_submeta_projeto_basico: Optional[str]
    descricao_submeta_projeto_basico: Optional[str]
    situacao_submeta_projeto_basico: Optional[str]
    valor_repasse_submeta_projeto_basico: Optional[float]
    valor_contrapartida_submeta_projeto_basico: Optional[float]
    valor_outros_submeta_projeto_basico: Optional[float]
    valor_total_submeta_projeto_basico: Optional[float]
    data_previsao_inicio_obra_projeto_basico: Optional[date]
    quantidade_meses_duracao_obra_projeto_basico: Optional[int]
    database_obra_projeto_basico: Optional[date]
    sigla_localidade_obra_projeto_basico: Optional[str]
    obra_acompanhada_por_evento_projeto_basico: Optional[str]

class PaginatedProjetoBasicoSubmetasModuloEmpresasResponse(PaginatedResponseTemplate):
    data: List[ProjetoBasicoSubmetasModuloEmpresasResponse]


