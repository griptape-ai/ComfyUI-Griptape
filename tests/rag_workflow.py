# use tempfile to create a temporary file

from dotenv import load_dotenv
from griptape.chunkers import TextChunker
from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver
from griptape.engines.rag import RagEngine
from griptape.engines.rag.modules import TextLoaderRetrievalRagModule
from griptape.engines.rag.stages import RetrievalRagStage
from griptape.loaders import TextLoader
from griptape.structures import Agent
from griptape.tools import QueryTool, RagTool

load_dotenv()

text = """
Wonderbread.ai is a fictitional company that specializes in creating balloon animals for the future.
They are often confused with the bread company, Wonder Bread, but they are not the same.
Some of the services that Wonderbread.ai offers include:
- Balloon animal creation
- Balloon animal delivery
- Balloon animal training
- Balloon animal parties
- Balloon animal events
- Balloon animal consulting
- Balloon animal workshops
- Balloon animal classes
- Balloon animal seminars
- Balloon animal webinars
- Balloon animal conferences

Wonderbread.ai is a leader in the balloon animal industry and has been in business for over 100 years.
They have a team of experts who are dedicated to creating the best balloon animals in the world.
If you are interested in learning more about Wonderbread.ai, please visit their website at www.wonderbread.ai/balloonanimals
"""

chunker = TextChunker()
chunks = chunker.chunk(text)
module = TextLoaderRetrievalRagModule(
    query_params={"namespace": "wonderbread"},
    vector_store_driver=LocalVectorStoreDriver(
        embedding_driver=OpenAiEmbeddingDriver()
    ),
    loader=TextLoader().parse(text),
)

retrieval_modules = [module]

rag_engine = RagEngine(
    retrieval_stage=RetrievalRagStage(retrieval_modules=retrieval_modules),
)

tool = RagTool(
    off_prompt=True, description="Contains info about a company", rag_engine=rag_engine
)

agent = Agent(tools=[tool, QueryTool()])

agent.run("What does the company Wonderbread.ai do?")
