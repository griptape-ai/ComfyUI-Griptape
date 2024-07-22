from griptape.drivers import PgVectorVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_USER_ENV = "POSTGRES_USER"
DEFAULT_PASS_ENV = "POSTGRES_PASSWORD"
DEFAULT_HOST_ENV = "POSTGRES_HOST"
DEFAULT_PORT_ENV = "POSTGRES_PORT"
DEFAULT_NAME_ENV = "POSTGRES_DB"
DEFAULT_TABLE_NAME = "griptape_vectors"


class gtUIPgVectorVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = (
        "Griptape PGVector Vector Store Driver: https://github.com/pgvector/pgvector"
    )

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "table_name": ("STRING", {"default": DEFAULT_TABLE_NAME}),
                "host_env": ("STRING", {"default": DEFAULT_HOST_ENV}),
                "user_env": ("STRING", {"default": DEFAULT_USER_ENV}),
                "pass_env": ("STRING", {"default": DEFAULT_PASS_ENV}),
                "port_env": ("STRING", {"default": DEFAULT_PORT_ENV}),
                "name_env": ("STRING", {"default": DEFAULT_NAME_ENV}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        host_env = kwargs.get("host_env", DEFAULT_HOST_ENV)
        user_env = kwargs.get("user_env", DEFAULT_USER_ENV)
        pass_env = kwargs.get("pass_env", DEFAULT_PASS_ENV)
        port_env = kwargs.get("port_env", DEFAULT_PORT_ENV)
        name_env = kwargs.get("name_env", DEFAULT_NAME_ENV)
        table_name = kwargs.get("table_name", DEFAULT_TABLE_NAME)

        if host_env:
            host = self.getenv(host_env)
        if user_env:
            user = self.getenv(user_env)
        if pass_env:
            password = self.getenv(pass_env)
        if port_env:
            port = self.getenv(port_env)
        if name_env:
            name = self.getenv(name_env)

        params = {}

        if user and password and host and port and name:
            params["connection_string"] = (
                f"postgresql://{user}:{password}@{host}:{port}/{name}"
            )
        if table_name:
            params["table_name"] = table_name
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()
        driver = PgVectorVectorStoreDriver(**params)
        return (driver,)
