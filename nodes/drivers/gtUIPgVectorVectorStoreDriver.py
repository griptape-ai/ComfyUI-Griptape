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
                "table_name": (
                    "STRING",
                    {
                        "default": DEFAULT_TABLE_NAME,
                        "tooltip": "Name of the table to store vectors",
                    },
                ),
                "host_env": (
                    "STRING",
                    {
                        "default": DEFAULT_HOST_ENV,
                        "tooltip": "Environment variable name for the PostgreSQL host",
                    },
                ),
                "user_env": (
                    "STRING",
                    {
                        "default": DEFAULT_USER_ENV,
                        "tooltip": "Environment variable name for the PostgreSQL user",
                    },
                ),
                "pass_env": (
                    "STRING",
                    {
                        "default": DEFAULT_PASS_ENV,
                        "tooltip": "Environment variable name for the PostgreSQL password",
                    },
                ),
                "port_env": (
                    "STRING",
                    {
                        "default": DEFAULT_PORT_ENV,
                        "tooltip": "Environment variable name for the PostgreSQL port",
                    },
                ),
                "name_env": (
                    "STRING",
                    {
                        "default": DEFAULT_NAME_ENV,
                        "tooltip": "Environment variable name for the PostgreSQL database name",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        user = self.getenv(kwargs.get("user_env", DEFAULT_USER_ENV))
        password = self.getenv(kwargs.get("pass_env", DEFAULT_PASS_ENV))
        host = self.getenv(kwargs.get("host_env", DEFAULT_HOST_ENV))
        port = self.getenv(kwargs.get("port_env", DEFAULT_PORT_ENV))
        name = self.getenv(kwargs.get("name_env", DEFAULT_NAME_ENV))
        table_name = kwargs.get("table_name", DEFAULT_TABLE_NAME)
        embedding_driver = kwargs.get("embedding_driver", None)

        params = {
            "connection_string": f"postgresql://{user}:{password}@{host}:{port}/{name}",
            "table_name": table_name,
        }
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)

        driver = PgVectorVectorStoreDriver(**params)
        return (driver,)
