import os

from griptape.drivers import OpenAiEmbeddingDriver, RedisVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

default_embedding_driver = OpenAiEmbeddingDriver()

default_host_env = "REDIS_HOST"
default_port_env = "REDIS_PORT"
default_password_env = "REDIS_PASSWORD"
default_index_env = "REDIS_INDEX"


class gtUIRedisVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Redis Atlas Vector Store Driver: https://redis.io/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update()
        inputs["optional"].update(
            {
                "host_env": ("STRING", {"default": default_host_env}),
                "port_env": ("STRING", {"default": default_port_env}),
                "password_env": ("STRING", {"default": default_password_env}),
                "index_env": ("STRING", {"default": default_index_env}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", default_embedding_driver)
        host_env = kwargs.get("host_env", default_host_env)
        port_env = kwargs.get("port_env", default_port_env)
        password_env = kwargs.get("password_env", default_password_env)
        index_env_var = kwargs.get("index_name_env", default_index_env)

        if password_env:
            password = os.getenv(password_env)
        if host_env:
            host = os.getenv(host_env)
        if port_env:
            port = os.getenv(port_env)
        if index_env_var:
            index = os.getenv(index_env_var)
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
