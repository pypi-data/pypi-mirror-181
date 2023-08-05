from sqlalchemy import create_engine
from .configuration import Config

class Engine:
    """
        create engine to connect to a database based on the config
        by default, engine uses the dev configs from config object
        @param config_file_path (str) : full path to config file
        @param echo (bool) : expose sql query
        @param env (str) : 'DEV' or 'PROD' which are config types in config file
    """
    engine = ''
    def __init__(self, config_file_path, echo=False, env='DEV'):
        self.config = Config(config_file_path, env=env).ConfMap
        self.echo = echo
        self.__engine_db()

    def __engine_db(self):
        """
            create engine, connect to the database
        """
        self.engine = create_engine(
                    f"{self.config['SQL_TYPE_DB']}://{self.config['SQL_USER']}:{self.config['SQL_PASSWORD']}@{self.config['SQL_HOST']}:{self.config['SQL_PORT']}/{self.config['SQL_DATABASE']}",
                    echo=self.echo
                )

    def __repr__(self):
        # return str(self.config)
        return f"<Engine:{self.config['SQL_USER']} - {self.config['SQL_HOST']} - {self.config['SQL_DATABASE']}"

    __str__ = __repr__