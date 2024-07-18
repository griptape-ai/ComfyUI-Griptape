import os

from griptape.drivers import AzureMongoDbVectorStoreDriver, OpenAiEmbeddingDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

default_host_env = "AZURE_MONGODB_HOST"
default_username_env = "AZURE_MONGODB_USERNAME"
default_password_env = "AZURE_MONGODB_PASSWORD"
default_database_name_env = "AZURE_MONGODB_DATABASE_NAME"
default_collection_name_env = "AZURE_MONGODB_COLLECTION_NAME"
default_index_name_env = "AZURE_MONGODB_INDEX_NAME"
default_vector_path_env = "AZURE_MONGODB_VECTOR_PATH"


class gtUIAzureMongoDbVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Azure Mongodb Atlas Vector Store Driver: https://www.mongodb.com/products/platform/atlas-database"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "host_env": ("STRING", {"default": default_host_env}),
                "username_env": ("STRING", {"default": default_username_env}),
                "password_env": ("STRING", {"default": default_password_env}),
                "database_name_env": ("STRING", {"default": default_database_name_env}),
                "collection_name_env": (
                    "STRING",
                    {"default": default_collection_name_env},
                ),
                "index_name_env": ("STRING", {"default": default_index_name_env}),
                "vector_path_env": ("STRING", {"default": default_vector_path_env}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        host_env = kwargs.get("host_env", default_host_env)
        username_env = kwargs.get("username_env", default_username_env)
        password_env = kwargs.get("password_env", default_password_env)
        database_name_env = kwargs.get("database_name_env", default_database_name_env)
        collection_name_env = kwargs.get(
            "collection_name_env", default_collection_name_env
        )
        index_name_env_var = kwargs.get("index_name_env", default_index_name_env)
        vector_path_env = kwargs.get("vector_path_env", default_vector_path_env)

        if username_env:
            username = os.getenv(username_env)
        if password_env:
            password = os.getenv(password_env)
        if host_env:
            host = os.getenv(host_env)
        if database_name_env:
            database_name = os.getenv(database_name_env)
        if collection_name_env:
            collection_name = os.getenv(collection_name_env)
        if vector_path_env:
            vector_path = os.getenv(vector_path_env)

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
            params["index_name"] = os.getenv(index_name_env_var)
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver
        driver = AzureMongoDbVectorStoreDriver(**params)
        return (driver,)
