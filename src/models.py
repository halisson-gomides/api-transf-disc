from datetime import date, datetime
from decimal import Decimal
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
    cod_orgao_sup_programa: str
    desc_orgao_sup_programa: str
    cod_programa: str
    nome_programa: str
    sit_programa: str
    data_disponibilizacao: date
    ano_disponibilizacao: str
    dt_prog_ini_receb_prop: date
    dt_prog_fim_receb_prop: date
    dt_prog_ini_emenda_par: date
    dt_prog_fim_emenda_par: date
    dt_prog_ini_benef_esp: date
    dt_prog_fim_benef_esp: date
    modalidade_programa: str
    natureza_juridica_programa: str
    uf_programa: str
    acao_orcamentaria: str
    nome_subtipo_programa: str
    descricao_subtipo_programa: str
    
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
    identif_proponente: str
    nm_proponente: str
    municipio_proponente: str
    uf_proponente: str
    endereco_proponente: str
    bairro_proponente: str
    cep_proponente: str
    email_proponente: str
    telefone_proponente: str
    fax_proponente: str
    
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
    uf_proponente: str
    munic_proponente: str
    cod_munic_ibge: str
    cod_orgao_sup: str
    desc_orgao_sup: str
    natureza_juridica: str
    nr_proposta: str
    dia_prop: str
    mes_prop: str
    ano_prop: str
    dia_proposta: date
    cod_orgao: str
    desc_orgao: str
    modalidade: str
    identif_proponente: str
    nm_proponente: str
    cep_proponente: str
    endereco_proponente: str
    bairro_proponente: str
    nm_banco: str
    situacao_conta: str
    situacao_projeto_basico: str
    sit_proposta: str
    dia_inic_vigencia_proposta: date
    dia_fim_vigencia_proposta: date
    objeto_proposta: str
    item_investimento: str
    enviada_mandataria: str
    vl_global_prop: float
    vl_repasse_prop: float
    vl_contrapartida_prop: float
    nome_subtipo_proposta: str
    descricao_subtipo_proposta: str
    cd_agencia: str
    cd_conta: str
    
    # Add relationship to programas
    programas: list["Programa"] = Relationship(
        back_populates="propostas",
        link_model=ProgramaProposta
    )

# Tabela justificativas_proposta
class JustificativasProposta(BaseModel, table=True):
    __tablename__ = "justificativas_proposta"
    
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)    
    caracterizacao_interesses_reci: str
    publico_alvo: str
    problema_a_ser_resolvido: str
    resultados_esperados: str
    relacao_proposta_objetivos_pro: str
    capacidade_tecnica: str
    justificativa: str

# Tabela proposta_cancelada
class PropostaCancelada(BaseModel, table=True):
    __tablename__ = "proposta_cancelada"
    
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)
    uf_proponente: str
    munic_proponente: str
    cod_munic_ibge: str
    cod_orgao_sup: str
    desc_orgao_sup: str
    natureza_juridica: str
    nr_proposta: str
    dia_prop: int
    mes_prop: int
    ano_prop: int
    dia_proposta: date
    cod_orgao: str
    desc_orgao: str
    modalidade: str
    identif_proponente: str
    nm_proponente: str
    cep_proponente: str
    endereco_proponente: str
    bairro_proponente: str
    nm_banco: str
    situacao_conta: str
    situacao_projeto_basico: str
    sit_proposta: str
    dia_inic_vigencia_proposta: date
    dia_fim_vigencia_proposta: date
    objeto_proposta: str
    item_investimento: str
    enviada_mandataria: str
    vl_global_prop: float
    vl_repasse_prop: float
    vl_contrapartida_prop: float
    nome_subtipo_proposta: str
    descricao_subtipo_proposta: str


class PropostaSelecaoPac(BaseModel, table=True):
    __tablename__ = "proposta_selecao_pac"
    
    id_proposta_selecao_pac: int = Field(primary_key=True)
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa")
    id_proponente: int = Field(foreign_key=f"{db_schema}.proponentes.id_proponente")
    nr_proposta_selecao_pac: str
    data_cadastro_proposta_selecao_pac: datetime
    data_envio_proposta_selecao_pac: datetime
    objeto_proposta_selecao_pac: str
    situacao_proposta_selecao_pac: str
    valor_total_proposta_selecao_pac: float
    justificativa_proposta_selecao_pac: str
    tem_anexo_proposta_selecao_pac: str


class PerguntaSelecaoPac(BaseModel, table=True):
    __tablename__ = "pergunta_selecao_pac"
    
    id_pergunta_selecao_pac: int = Field(primary_key=True)
    id_programa: int = Field(foreign_key=f"{db_schema}.programa.id_programa")
    pergunta_selecao_pac: str


class RespostaSelecaoPac(BaseModel, table=True):
    __tablename__ = "resposta_selecao_pac"

    id_pergunta_selecao_pac: int = Field(primary_key=True, foreign_key=f"{db_schema}.pergunta_selecao_pac.id_pergunta_selecao_pac")
    id_proposta_selecao_pac: int = Field(primary_key=True, foreign_key=f"{db_schema}.proposta_selecao_pac.id_proposta_selecao_pac")
    resposta_selecao_pac: str = Field(default=None, description="Resposta da pergunta da Proposta do Novo PAC")
    

class PropostaFormalizacaoPac(BaseModel, table=True):
    __tablename__ = "proposta_formalizacao_pac"
    
    id_proposta_selecao_pac: int = Field(foreign_key=f"{db_schema}.proposta_selecao_pac.id_proposta_selecao_pac", primary_key=True)
    id_proposta: int = Field(foreign_key=f"{db_schema}.proposta.id_proposta", primary_key=True)
    nr_reservado_pac: str 