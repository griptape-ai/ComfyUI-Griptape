from __future__ import annotations

import schema
from attr import define
from duckduckgo_search import DDGS
from griptape.artifacts import ErrorArtifact, ListArtifact, TextArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Literal, Schema


@define
class DuckDuckGoTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to perform a text search on DuckDuckGo",
            "schema": Schema(
                {
                    Literal("keywords", description="The keywords to search for"): str,
                    schema.Optional(
                        "max_results",
                        default=None,
                        description="The maximum number of results to return",
                    ): int,
                    schema.Optional(
                        "region",
                        default="wt-wt",
                        description="The region to search in (wt-wt, us-en, uk-en, ru-ru, etc)",
                    ): str,
                    schema.Optional(
                        "safe_search",
                        default="moderate",
                        description="The safe search level to use (on, moderate, off)",
                    ): str,
                    schema.Optional(
                        "timelimit",
                        default=None,
                        description="The time limit for the search (d, w, m, y)",
                    ): str,
                    schema.Optional(
                        "backend",
                        default="api",
                        description="The backend to use for the search (api, html, lite)",
                    ): str,
                },
            ),
        }
    )
    def text(self, params: dict) -> ListArtifact | ErrorArtifact:
        keyword_value = params["values"].get("keywords")
        max_results = params["values"].get("max_results")
        region = params["values"].get("region")
        safe_search = params["values"].get("safe_search")
        timelimit = params["values"].get("timelimit")
        backend = params["values"].get("backend")

        # Initialize a dictionary with the keyword argument
        params = {}

        # Add parameters to the dictionary only if they are not None
        if max_results is not None:
            params["max_results"] = max_results
        if region is not None:
            params["region"] = region
        if safe_search is not None:
            params["safe_search"] = safe_search
        if timelimit is not None:
            params["timelimit"] = timelimit
        if backend is not None:
            params["backend"] = backend
        try:
            results = DDGS().text(keyword_value, **params)
            return ListArtifact([TextArtifact(result) for result in results])

        except Exception as e:
            return ErrorArtifact(str(e))

    @activity(
        config={
            "description": "Can be used to get instant answers from DuckDuckGo",
            "schema": Schema(
                {
                    Literal("keywords", description="The keywords to search for"): str,
                },
            ),
        }
    )
    def answers(self, params: dict) -> ListArtifact | ErrorArtifact:
        keyword_value = params["values"].get("keywords")

        try:
            results = DDGS().answers(keyword_value)
            return ListArtifact([TextArtifact(result) for result in results])

        except Exception as e:
            return ErrorArtifact(str(e))
