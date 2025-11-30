import os

oauth_config = {
    "novixx": {
        "client_id": os.getenv("NOVIXXIA_CLIENT_ID", "clientid"),
        "client_secret": os.getenv("NOVIXXIA_CLIENT_SECRET", "clientsecret"),
        "oauth_authorize_url": "https://accounts.novixx.com/authorize.php?token=clientid&bid=BIDHERE&PERMISSION_USERNAME=true",
        "oauth_token_url": "https://accounts.novixx.com/token.php?bid=BIDHERE&businesstoken=clientsecret",
        "scope": "username",
        "account_api_url": "https://accounts.novixx.com/get.php?bid=BIDHERE&businesstoken=clientsecret",
    },
    "lichess": {
        "client_id": os.getenv("LICHESS_CLIENT_ID", "Chess"),
        "client_secret": os.getenv("CLIENT_SECRET", "secretnbgttoken"),
        "oauth_authorize_url": "https://lichess.org/oauth",
        "oauth_token_url": "https://lichess.org/api/token",
        "scope": "",
        "account_api_url": "https://lichess.org/api/account",
    }
}
