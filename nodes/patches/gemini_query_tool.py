from __future__ import annotations

from attrs import define
from griptape.artifacts import ErrorArtifact, ListArtifact, TextArtifact
from griptape.engines.rag.rag_context import RagContext
from griptape.tools import QueryTool
from griptape.utils.decorators import activity
from schema import Literal, Schema


@define(kw_only=True)
class GeminiQueryTool(QueryTool):
    @activity(
        config={
            "description": "Can be used to search through textual content.",
            "schema": Schema(
                {
                    Literal(
                        "query", description="A natural language search query"
                    ): str,
                    Literal("content"): Schema(
                        {
                            "memory_name": str,
                            "artifact_namespace": str,
                        }
                    ),
                }
            ),
        },
    )
    def query(self, params: dict) -> ListArtifact | ErrorArtifact:
        query = params["values"]["query"]
        content = params["values"]["content"]

        if isinstance(content, str):
            text_artifacts = [TextArtifact(content)]
        else:
            memory = self.find_input_memory(content["memory_name"])
            artifact_namespace = content["artifact_namespace"]

            if memory is not None:
                artifacts = memory.load_artifacts(artifact_namespace)
            else:
                return ErrorArtifact("memory not found")

            text_artifacts = [
                artifact for artifact in artifacts if isinstance(artifact, TextArtifact)
            ]

        outputs = self._rag_engine.process(
            RagContext(query=query, text_chunks=text_artifacts)
        ).outputs

        if len(outputs) > 0:
            return ListArtifact(outputs)
        else:
            return ErrorArtifact("query output is empty")
