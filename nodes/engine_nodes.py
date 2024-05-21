from griptape.engines import CsvExtractionEngine, JsonExtractionEngine

from .base_engine import gtUIBaseExtractionEngine


class gtUICsvExtractionEngine(gtUIBaseExtractionEngine):
    """
    Griptape CSV Extraction Engine
    """

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver")
        max_token_multiplier = kwargs.get("max_token_multiplier")
        chunk_joiner = kwargs.get("chunk_joiner")

        engine = CsvExtractionEngine(
            driver=prompt_driver,
            max_token_multiplier=max_token_multiplier,
            chunk_joiner=chunk_joiner,
        )

        return (engine,)


class gtUIJsonExtractionEngine(gtUIBaseExtractionEngine):
    """
    Griptape Json Extraction Engine
    """

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver")
        max_token_multiplier = kwargs.get("max_token_multiplier")
        chunk_joiner = kwargs.get("chunk_joiner")

        engine = JsonExtractionEngine(
            driver=prompt_driver,
            max_token_multiplier=max_token_multiplier,
            chunk_joiner=chunk_joiner,
        )

        return (engine,)
