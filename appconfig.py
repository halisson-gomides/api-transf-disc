
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    CACHE_SERVER_URL: str        
    CACHE_TTL: str = "30m"      
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_TAGS: list = [
        {
            "name": "Programa",
            "description": "Dados relativos aos Programas - Discricionárias e Legais.",
        },
        {
            "name": "Proponente",
            "description": "Dados relativos aos Proponentes dos Programas - Discricionárias e Legais.",
        },
        {
            "name": "Proposta",
            "description": "Dados relativos às Propostas - Discricionárias e Legais.",
        },     
        {
            "name": "PAC",
            "description": "Dados relativos ao PAC - Discricionárias e Legais.",
        },
        {
            "name": "Plano de Trabalho",
            "description": "Dados relativos aos Planos de Trabalho - Discricionárias e Legais.",
        },  
        {
            "name": "Instrumento",
            "description": "Dados relativos a Instrumentos de Convêncios - Discricionárias e Legais.",
        },
        {
            "name": "Empenho",
            "description": "Dados relativos a Empenho Orçamentário - Discricionárias e Legais.",
        },
        {
            "name": "Desembolso",
            "description": "Dados relativos a Desembolso Orçamentário - Discricionárias e Legais.",
        },
        {
            "name": "Movimentação Financeira",
            "description": "Dados relativos a Movimentação Financeira - Discricionárias e Legais.",
        },
        {
            "name": "Emenda",
            "description": "Dados relativos a Emendas Parlamentares - Discricionárias e Legais.",
        },
        {
            "name": "Licitação/Contrato",
            "description": "Dados relativos a Licitações e Contratos - Discricionárias e Legais.",
        },
        {
            "name": "Outros",
            "description": "Dados relativos aos demais tópicos - Discricionárias e Legais.",
        },
        {
            "name": "Módulo Empresas",
            "description": "Dados relativos ao módulo de empresas - Discricionárias e Legais.",
        }
        
    ]
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000
    ERROR_MESSAGE_NO_PARAMS: str = "Nenhum parâmetro de consulta foi informado."
    ERROR_MESSAGE_INTERNAL: str = "Erro Interno Inesperado."
    STATS_USER: str 
    STATS_PASSWORD: str 