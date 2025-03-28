
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
    ]
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 200
    ERROR_MESSAGE_NO_PARAMS: str = "Nenhum parâmetro de consulta foi informado."
    ERROR_MESSAGE_INTERNAL: str = "Erro Interno Inesperado."
    STATS_USER: str 
    STATS_PASSWORD: str 