from griptape.drivers.vector.redis import RedisVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_HOST_ENV = "REDIS_HOST"
DEFAULT_PORT_ENV = "REDIS_PORT"
DEFAULT_PASSWORD_ENV = "REDIS_PASSWORD"
DEFAULT_INDEX_ENV = "REDIS_INDEX"


class gtUIRedisVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Redis Atlas Vector Store Driver: https://redis.io/"

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
                        "tooltip": "Environment variable name for the Redis host",
                    },
                ),
                "port_env": (
                    "STRING",
                    {
                        "default": DEFAULT_PORT_ENV,
                        "tooltip": "Environment variable name for the Redis port",
                    },
                ),
                "password_env": (
                    "STRING",
                    {
                        "default": DEFAULT_PASSWORD_ENV,
                        "tooltip": "Environment variable name for the Redis password. Do not include the actual password here.",
                    },
                ),
                "index_env": (
                    "STRING",
                    {
                        "default": DEFAULT_INDEX_ENV,
                        "tooltip": "Environment variable name for the Redis index",
                    },
                ),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        host_env = kwargs.get("host_env", DEFAULT_HOST_ENV)
        port_env = kwargs.get("port_env", DEFAULT_PORT_ENV)
        password_env = kwargs.get("password_env", DEFAULT_PASSWORD_ENV)
        index_env_var = kwargs.get("index_name_env", DEFAULT_INDEX_ENV)

        password = None
        host = None
        port = None
        index = None

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
            params["embedding_driver"] = self.get_default_embedding_driver()
        driver = RedisVectorStoreDriver(**params)
        return (driver,)
