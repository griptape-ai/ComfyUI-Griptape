from griptape.engines.rag import RagEngine
from griptape.engines.rag.stages import (
    QueryRagStage,
    ResponseRagStage,
    RetrievalRagStage,
)


class gtUIRagEngine:
    DESCRIPTION = "Griptape Rag Tool"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "query_stage_modules": (
                    "MODULE_LIST",
                    {
                        "forceInput:": True,
                        "tooltip": "(Optional) Used for modifying user queries. For example, translating the query to another language.",
                    },
                ),
                "retrieval_stage_modules": (
                    "MODULE_LIST",
                    {
                        "forceInput": True,
                        "tooltip": "Modules Used for retrieving relevant documents and re-ranking results.",
                    },
                ),
                "rerank_module": (
                    "MODULE",
                    {
                        "forceInput": True,
                        "tooltip": "(Optional) Module used for re-ranking results. ",
                    },
                ),
                "response_stage_modules": (
                    "MODULE_LIST",
                    {
                        "forceInput": True,
                        "tooltip": "Modules used to append metadata, rulesets, generate responses, or adding footnotes.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("RAG_ENGINE",)
    RETURN_NAMES = ("RAG_ENGINE",)

    FUNCTION = "create"

    CATEGORY = "Griptape/RAG"

    def create(self, **kwargs):
        query_stage_modules = kwargs.get("query_stage_modules", [])
        retrieval_stage_modules = kwargs.get("retrieval_stage_modules", [])
        rerank_module = kwargs.get("rerank_module", None)
        response_stage_modules = kwargs.get("response_stage_modules", [])

        engine_params = {}

        if len(query_stage_modules) > 0:
            engine_params["query_stage"] = QueryRagStage(
                query_modules=query_stage_modules
            )
        if len(retrieval_stage_modules) > 0:
            retrieval_stage_params = {}
            if rerank_module:
                retrieval_stage_params["rerank_module"] = rerank_module
            retrieval_stage_params["retrieval_modules"] = retrieval_stage_modules
            engine_params["retrieval_stage"] = RetrievalRagStage(
                **retrieval_stage_params
            )
        if len(response_stage_modules) > 0:
            engine_params["response_stage"] = ResponseRagStage(
                response_modules=response_stage_modules
            )

        engine = RagEngine(**engine_params)
        return (engine,)
