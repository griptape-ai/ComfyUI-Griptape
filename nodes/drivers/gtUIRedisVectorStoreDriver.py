from griptape.drivers import OpenAiEmbeddingDriver, RedisVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

DEFAULT_HOST_ENV = "REDIS_HOST"
DEFAULT_PORT_ENV = "REDIS_PORT"
DEFAULT_PASSWORD_ENV = "REDIS_PASSWORD"
DEFAULT_INDEX_ENV = "REDIS_INDEX"


class gtUIRedisVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Redis Atlas Vector Store Driver: https://redis.io/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "host_env": ("STRING", {"default": DEFAULT_HOST_ENV}),
                "port_env": ("STRING", {"default": DEFAULT_PORT_ENV}),
                "password_env": ("STRING", {"default": DEFAULT_PASSWORD_ENV}),
                "index_env": ("STRING", {"default": DEFAULT_INDEX_ENV}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        host_env = kwargs.get("host_env", DEFAULT_HOST_ENV)
        port_env = kwargs.get("port_env", DEFAULT_PORT_ENV)
        password_env = kwargs.get("password_env", DEFAULT_PASSWORD_ENV)
        index_env_var = kwargs.get("index_name_env", DEFAULT_INDEX_ENV)

        if password_env:
            password = self.getenv(password_env)
        if host_env:
            host = self.getenv(host_env)
        if port_env:
            port = self.getenv(port_env)
        if index_env_var:
            index = self.getenv(index_env_var)
        params = {}
        if password:
            params["password"] = password
        if host:
            params["host"] = host
        if port:
            params["port"] = port
        if index:
            params["index"] = index
        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = default_embedding_driver
        driver = RedisVectorStoreDriver(**params)
        return (driver,)
