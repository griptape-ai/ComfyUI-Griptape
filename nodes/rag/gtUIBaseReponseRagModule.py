from griptape.engines.rag.modules import BaseResponseRagModule

from .gtUIBaseRagModule import gtUIBaseRagModule


class gtUIBaseResponseRagModule(gtUIBaseRagModule):
    """
    Griptape Base Response Rag Module
    """

    def create(self, **kwargs):
        return ([BaseResponseRagModule()],)
