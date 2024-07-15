from griptape.drivers import DuckDuckGoWebSearchDriver

from .BaseWebSearchDriver import gtUIBaseWebSearchDriver


class gtUIDuckDuckGoWebSearchDriver(gtUIBaseWebSearchDriver):
    DESCRIPTION = "DuckDuckGo Web Search Driver"

    def create(
        self,
    ):
        driver = DuckDuckGoWebSearchDriver()
        return (driver,)
