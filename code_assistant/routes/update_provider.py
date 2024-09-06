from astra_assistants.utils import get_env_vars_for_provider
from code_assistant.constants.config import MODEL
from code_assistant.routes.home import key_modal_page
from litellm import utils


async def page(provider: str):
    env_vars = get_env_vars_for_provider(provider)
    model_provider = utils.get_llm_provider(MODEL)[1]
    model = ""
    if provider == model_provider:
        model = MODEL
    return key_modal_page(provider, env_vars, model)