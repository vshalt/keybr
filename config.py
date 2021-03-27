class Config:
    def init_app(self):
        pass


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {"development": DevelopmentConfig, "production": ProductionConfig}
