from ...py.griptape_config import get_config
from .base_task import gtUIBaseTask

default_prompt = "{{ input_string }}"
OPENAI_API_KEY = get_config("env.OPENAI_API_KEY")


class gtUIPromptTask(gtUIBaseTask): ...