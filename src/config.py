from dataclasses import dataclass


@dataclass
class COMMUNICATION_CONF:
    DOMAIN = "https://openapi.koreainvestment.com:9443"
    OAUTH_ROUTING = "/oauth2/Approval"
    GEN_TOKEN_ROUTING = "/oauth2/tokenP"
    REVOKE_TOKEN_ROUTING = "/oauth2/revokeP"
    PRIMARY_SEARCH_ROUTING = "/uapi/domestic-stock/v1/quotations/search-stock-info"
    ACCOUNT_ROUTING = "/uapi/domestic-stock/v1/trading/inquire-balance"
    ACCOUNT_BALANCE_ROUTING = "/uapi/domestic-stock/v1/trading/inquire-balance"

    WEBSOCKET_DOMAIN = "ws://ops.koreainvestment.com:21000"
    REALTIME_PRICE_ROUTING = "/tryitout/H0STCNT0"

    OAUTH_URL = DOMAIN + OAUTH_ROUTING
    GEN_TOKEN_URL = DOMAIN + GEN_TOKEN_ROUTING
    REVOKE_TOKEN_URL = DOMAIN + REVOKE_TOKEN_ROUTING
    PRIMARY_SEARCH_URL = DOMAIN + PRIMARY_SEARCH_ROUTING
    ACCOUNT_URL = DOMAIN + ACCOUNT_ROUTING
    ACCOUNT_BALANCE_URL = DOMAIN + ACCOUNT_BALANCE_ROUTING

    REALTIME_PRICE_URL = WEBSOCKET_DOMAIN + REALTIME_PRICE_ROUTING

@dataclass
class DB:
    DB_NAME = "autostocktrader.db"
    CERTIFICATION = "certification"