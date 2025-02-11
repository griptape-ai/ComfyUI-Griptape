from griptape.drivers.vector.mongodb_atlas import MongoDbAtlasVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_HOST_ENV = "MONGODB_HOST"
DEFAULT_USERNAME_ENV = "MONGODB_USERNAME"
DEFAULT_PASSWORD_ENV = "MONGODB_PASSWORD"
DEFAULT_DATABASE_NAME_ENV = "MONGODB_DATABASE_NAME"
DEFAULT_COLLECTION_NAME_ENV = "MONGODB_COLLECTION_NAME"
DEFAULT_INDEX_NAME_ENV = "MONGODB_INDEX_NAME"
DEFAULT_VECTOR_PATH_ENV = "MONGODB_VECTOR_PATH"


class gtUIMongoDbAtlasVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Mongodb Atlas Vector Store Driver: https://www.mongodb.com/products/platform/atlas-database"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "host_env": (
                    "STRING",
                    {
                        "default": DEFAULT_HOST_ENV,
                        "tooltip": "Environment variable for MongoDB host",
                    },
                ),
                "username_env": (
                    "STRING",
                    {
                        "default": DEFAULT_USERNAME_ENV,
                        "tooltip": "Environment variable for MongoDB username",
                    },
                ),
                "password_env": (
                    "STRING",
                    {
                        "default": DEFAULT_PASSWORD_ENV,
                        "tooltip": "Environment variable for MongoDB password",
                    },
                ),
                "database_name_env": (
                    "STRING",
                    {
                        "default": DEFAULT_DATABASE_NAME_ENV,
                        "tooltip": "Environment variable for MongoDB database name",
                    },
                ),
                "collection_name_env": (
                    "STRING",
                    {
                        "default": DEFAULT_COLLECTION_NAME_ENV,
                        "tooltip": "Environment variable for MongoDB collection name",
                    },
                ),
                "index_name_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_INDEX_NAME_ENV,
                        "tooltip": "Environment variable for MongoDB index name",
                    },
                ),
                "vector_path_env": (
                    "STRING",
                    {
                        "default": DEFAULT_VECTOR_PATH_ENV,
                        "tooltip": "Environment variable for MongoDB vector path",
                    },
                ),
            }
        )

        return inputs

    def build_params(self, **kwargs):
        username = self.getenv(kwargs.get("username_env", DEFAULT_USERNAME_ENV))
        password = self.getenv(kwargs.get("password_env", DEFAULT_PASSWORD_ENV))
        host = self.getenv(kwargs.get("host_env", DEFAULT_HOST_ENV))
        database_name = self.getenv(
            kwargs.get("database_name_env", DEFAULT_DATABASE_NAME_ENV)
        )
        collection_name = self.getenv(
            kwargs.get("collection_name_env", DEFAULT_COLLECTION_NAME_ENV)
        )
        index_name = self.getenv(
            kwargs.get("index_name_env_var", DEFAULT_INDEX_NAME_ENV)
        )
        vector_path = self.getenv(
            kwargs.get("vector_path_env", DEFAULT_VECTOR_PATH_ENV)
        )
        embedding_driver = kwargs.get("embedding_driver", None)
        params = {
            "database_name": database_name,
            "collection_name": collection_name,
            "vector_path": vector_path,
            "index_name": index_name,
        }
        params["connection_string"] = (
            f"mongodb+srv://{username}:{password}@{host}/{database_name}"
        )

        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()

        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = MongoDbAtlasVectorStoreDriver(**params)  # type: ignore[reportArgumentType]
        return (driver,)
