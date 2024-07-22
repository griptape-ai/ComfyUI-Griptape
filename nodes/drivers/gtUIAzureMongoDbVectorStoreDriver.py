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
                "host_env": ("STRING", {"default": DEFAULT_HOST_ENV}),
                "username_env": ("STRING", {"default": DEFAULT_USERNAME_ENV}),
                "password_env": ("STRING", {"default": DEFAULT_PASSWORD_ENV}),
                "database_name_env": ("STRING", {"default": DEFAULT_DATABASE_NAME_ENV}),
                "collection_name_env": (
                    "STRING",
                    {"default": DEFAULT_COLLECTION_NAME_ENV},
                ),
                "index_name_env": ("STRING", {"default": DEFAULT_INDEX_NAME_ENV}),
                "vector_path_env": ("STRING", {"default": DEFAULT_VECTOR_PATH_ENV}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        host_env = kwargs.get("host_env", DEFAULT_HOST_ENV)
        username_env = kwargs.get("username_env", DEFAULT_USERNAME_ENV)
        password_env = kwargs.get("password_env", DEFAULT_PASSWORD_ENV)
        database_name_env = kwargs.get("database_name_env", DEFAULT_DATABASE_NAME_ENV)
        collection_name_env = kwargs.get(
            "collection_name_env", DEFAULT_COLLECTION_NAME_ENV
        )
        index_name_env_var = kwargs.get("index_name_env", DEFAULT_INDEX_NAME_ENV)
        vector_path_env = kwargs.get("vector_path_env", DEFAULT_VECTOR_PATH_ENV)

        if username_env:
            username = self.getenv(username_env)
        if password_env:
            password = self.getenv(password_env)
        if host_env:
            host = self.getenv(host_env)
        if database_name_env:
            database_name = self.getenv(database_name_env)
        if collection_name_env:
            collection_name = self.getenv(collection_name_env)
        if vector_path_env:
            vector_path = self.getenv(vector_path_env)

        params = {}
        if username and password and host and database_name:
            params["connection_string"] = (
                f"mongodb+srv://{username}:{password}@{host}/{database_name}?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000",
            )
        if database_name:
            params["database_name"] = database_name
        if collection_name:
            params["collection_name"] = collection_name
        if vector_path:
            params["vector_path"] = vector_path
        if index_name_env_var:
            params["index_name"] = self.getenv(index_name_env_var)
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()
        driver = AzureMongoDbVectorStoreDriver(**params)
        return (driver,)
