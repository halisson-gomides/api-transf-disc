-- api_transferegov_discricionarias.solicitacao_alteracao definição

-- Drop table

-- DROP TABLE api_transferegov_discricionarias.solicitacao_alteracao;

CREATE TABLE api_transferegov_discricionarias.solicitacao_alteracao (
	id_solicitacao int4 NOT NULL, -- Identificador único da tabela solicitacao_alteracao
	nr_convenio int4 NULL, -- Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999
	nr_solicitacao varchar NULL, -- Número sequencial juntamente com o ano da solicitação de alteração do Convenente para o Concedente, via termo aditivo.
	situacao_solicitacao varchar NULL, -- Situação da solicitação de alteração do Convenente para o Concedente, via termo aditivo: “ACEITA”, “RECUSADA”, “EM_ANALISE”, “CADASTRADA”
	objeto_solicitacao varchar NULL, -- Objeto de alteração da solicitação de alteração do Convenente para o Concedente, via termo aditivo.
	data_solicitacao date NULL, -- Data da solicitação de alteração do convenente para o concedente, via termo aditivo.
	CONSTRAINT solicitacao_pk PRIMARY KEY (id_solicitacao),
	CONSTRAINT convenio_fk FOREIGN KEY (nr_convenio) REFERENCES api_transferegov_discricionarias.convenio(nr_convenio)
);

-- Column comments

COMMENT ON COLUMN api_transferegov_discricionarias.solicitacao_alteracao.id_solicitacao IS 'Identificador único da tabela solicitacao_alteracao';
COMMENT ON COLUMN api_transferegov_discricionarias.solicitacao_alteracao.nr_convenio IS 'Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999';
COMMENT ON COLUMN api_transferegov_discricionarias.solicitacao_alteracao.nr_solicitacao IS 'Número sequencial juntamente com o ano da solicitação de alteração do Convenente para o Concedente, via termo aditivo.';
COMMENT ON COLUMN api_transferegov_discricionarias.solicitacao_alteracao.situacao_solicitacao IS 'Situação da solicitação de alteração do Convenente para o Concedente, via termo aditivo: “ACEITA”, “RECUSADA”, “EM_ANALISE”, “CADASTRADA”';
COMMENT ON COLUMN api_transferegov_discricionarias.solicitacao_alteracao.objeto_solicitacao IS 'Objeto de alteração da solicitação de alteração do Convenente para o Concedente, via termo aditivo.';
COMMENT ON COLUMN api_transferegov_discricionarias.solicitacao_alteracao.data_solicitacao IS 'Data da solicitação de alteração do convenente para o concedente, via termo aditivo.';