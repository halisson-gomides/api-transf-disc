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