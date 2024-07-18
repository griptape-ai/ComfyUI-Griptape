import os

from griptape.drivers import OpenAiEmbeddingDriver, PgVectorVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

default_user_env = "POSTGRES_USER"
default_pass_env = "POSTGRES_PASSWORD"
default_host_env = "POSTGRES_HOST"
default_port_env = "POSTGRES_PORT"
default_name_env = "POSTGRES_DB"
default_table_name = "griptape_vectors"


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
                "host_env": ("STRING", {"default": default_host_env}),
                "user_env": ("STRING", {"default": default_user_env}),
                "pass_env": ("STRING", {"default": default_pass_env}),
                "port_env": ("STRING", {"default": default_port_env}),
                "name_env": ("STRING", {"default": default_name_env}),
                "table_name": ("STRING", {"default": default_table_name}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        host_env = kwargs.get("host_env", default_host_env)
        user_env = kwargs.get("user_env", default_user_env)
        pass_env = kwargs.get("pass_env", default_pass_env)
        port_env = kwargs.get("port_env", default_port_env)
        name_env = kwargs.get("name_env", default_name_env)
        table_name = kwargs.get("table_name", default_table_name)

        if host_env:
            host = os.getenv(host_env)
        if user_env:
            user = os.getenv(user_env)
        if pass_env:
            password = os.getenv(pass_env)
        if port_env:
            port = os.getenv(port_env)
        if name_env:
            name = os.getenv(name_env)

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
            params["embedding_driver"] = default_embedding_driver
        driver = PgVectorVectorStoreDriver(**params)
        return (driver,)
