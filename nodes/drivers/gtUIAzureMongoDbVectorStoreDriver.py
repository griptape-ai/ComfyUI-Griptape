from griptape.drivers import (
    AzureMongoDbVectorStoreDriver,
)

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_HOST_ENV = "AZURE_MONGODB_HOST"
DEFAULT_USERNAME_ENV = "AZURE_MONGODB_USERNAME"
DEFAULT_PASSWORD_ENV = "AZURE_MONGODB_PASSWORD"
DEFAULT_DATABASE_NAME_ENV = "AZURE_MONGODB_DATABASE_NAME"
DEFAULT_COLLECTION_NAME_ENV = "AZURE_MONGODB_COLLECTION_NAME"
DEFAULT_INDEX_NAME_ENV = "AZURE_MONGODB_INDEX_NAME"
DEFAULT_VECTOR_PATH_ENV = "AZURE_MONGODB_VECTOR_PATH"


class gtUIAzureMongoDbVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Azure Mongodb Atlas Vector Store Driver: https://www.mongodb.com/products/platform/atlas-database"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "host_env": (
                    "STRING",
                    {
                        "default": DEFAULT_HOST_ENV,
                        "tooltip": "Enter the name of the environment variable for AZURE_MONGODB_HOST, not the actual host.",
                    },
                ),
                "username_env": (
                    "STRING",
                    {
                        "default": DEFAULT_USERNAME_ENV,
                        "tooltip": "Enter the name of the environment variable for AZURE_MONGODB_USERNAME, not the actual username.",
                    },
                ),
                "password_env": (
                    "STRING",
                    {
                        "default": DEFAULT_PASSWORD_ENV,
                        "tooltip": "Enter the name of the environment variable for AZURE_MONGODB_PASSWORD, not the actual password.",
                    },
                ),
                "database_name_env": (
                    "STRING",
                    {
                        "default": DEFAULT_DATABASE_NAME_ENV,
                        "tooltip": "Enter the name of the environment variable for AZURE_MONGODB_DATABASE_NAME, not the actual database name.",
                    },
                ),
                "collection_name_env": (
                    "STRING",
                    {
                        "default": DEFAULT_COLLECTION_NAME_ENV,
                        "tooltip": "Enter the name of the environment variable for AZURE_MONGODB_COLLECTION_NAME, not the actual collection name.",
                    },
                ),
                "index_name_env": (
                    "STRING",
                    {
                        "default": DEFAULT_INDEX_NAME_ENV,
                        "tooltip": "Enter the name of the environment variable for AZURE_MONGODB_INDEX_NAME, not the actual index name.",
                    },
                ),
                "vector_path_env": (
                    "STRING",
                    {
                        "default": DEFAULT_VECTOR_PATH_ENV,
                        "tooltip": "Enter the name of the environment variable for AZURE_MONGODB_VECTOR_PATH, not the actual vector path.",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        host_env = self.getenv(kwargs.get("host_env", DEFAULT_HOST_ENV))
        username_env = self.getenv(kwargs.get("username_env", DEFAULT_USERNAME_ENV))
        password_env = self.getenv(kwargs.get("password_env", DEFAULT_PASSWORD_ENV))
        database_name_env = self.getenv(
            kwargs.get("database_name_env", DEFAULT_DATABASE_NAME_ENV)
        )
        collection_name_env = self.getenv(
            kwargs.get("collection_name_env", DEFAULT_COLLECTION_NAME_ENV)
        )
        index_name_env_var = self.getenv(
            kwargs.get("index_name_env", DEFAULT_INDEX_NAME_ENV)
        )
        vector_path_env = self.getenv(
            kwargs.get("vector_path_env", DEFAULT_VECTOR_PATH_ENV)
        )

        params = {}
        if host_env and username_env and password_env and database_name_env:
            params["connection_string"] = (
                f"mongodb+srv://{username_env}:{password_env}@{host_env}/{database_name_env}?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000",
            )
        if database_name_env:
            params["database_name"] = database_name_env
        if collection_name_env:
            params["collection_name"] = collection_name_env
        if vector_path_env:
            params["vector_path"] = vector_path_env
        if index_name_env_var:
            params["index_name"] = index_name_env_var
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = AzureMongoDbVectorStoreDriver(**params)
        return (driver,)
