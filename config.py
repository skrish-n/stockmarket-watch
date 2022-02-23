class Config:
    MONGODB_HOST = ""
    MONGODB_DB = 'StockWatchDB'
    JWT_SECRET_KEY = "jwt-secret-string"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    REGISTER_SECRET_KEY = 'qww'
    REGISTER_SECURITY_PASSWORD_SALT = 'qwe'

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'saitest101@gmail.com'
    MAIL_PASSWORD = 'saitest101adobe'

    MAIL_DEFAULT_SENDER = 'saitest101@gmail.com'

    # Alphavantage stock api key
    FINNHUB_KEY = 'bt8b6hv48v6srkbhggl0'
