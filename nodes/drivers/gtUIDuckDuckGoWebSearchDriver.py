from griptape.drivers.web_search.duck_duck_go import DuckDuckGoWebSearchDriver

from .gtUIBaseWebSearchDriver import gtUIBaseWebSearchDriver


class gtUIDuckDuckGoWebSearchDriver(gtUIBaseWebSearchDriver):
    DESCRIPTION = "DuckDuckGo Web Search Driver"

    def create(self, **kwargs):
        driver = DuckDuckGoWebSearchDriver()
        return (driver,)
