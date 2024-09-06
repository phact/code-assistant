from code_assistant.app import get_main_content
from code_assistant.constants.config import MODEL
from code_assistant.main import *
from fasthtml.common import *
from litellm import utils
from astra_assistants.utils import env_var_is_missing, get_env_vars_for_provider, provider_env_var_map


async def page(request):
    message_objects = []
    #message_objects= client.beta.threads.messages.list(thread_id="thread_94kTIBLZI918vFI6OLzpnOFqmiH9SI7L", order="asc").data

    if not hasattr(request.app.state, 'model'):
        request.app.state.model = MODEL
    model = request.app.state.model
    provider = utils.get_llm_provider(model)[1]
    env_vars = get_env_vars_for_provider(provider)
    if request.app.state._manager is None and env_var_is_missing(provider, env_vars):
        return key_modal_page(provider, env_vars, model)
    programs = request.app.state.manager.programs
    messages = request.app.state.messages
    for message_object in message_objects:
        msg = message_object.content[0].text.value
        if message_object.role == "user":
            request.app.state.messages.append({"role": "user", "content": msg})
        else:
            request.app.state.messages.append({"role": "assistant", "content": msg})
    return Div(
        get_main_content(programs, messages),
        cls="container",
    )

def get_key_modal(provider, inputs):
    provider_list = []
    for this_provider in provider_env_var_map.keys():
        if provider == this_provider:
            provider_list.append(Option(this_provider, selected=True))
        else:
            provider_list.append(Option(this_provider))

    return Dialog(
        Div(
            H1("Code Assistant"),
            H2("☝️Please provide a valid API key(s) to use the assistant."),
            H2("❕ Set these values as env vars to avoid manual entry."),
            Form(
                Label("LLM provider ",
                    Select(
                        Summary("LLM provider", cls="btn m-1"),
                        *provider_list,
                        hx_post="/provider",
                        hx_trigger="change",
                        hx_target="#container",
                        hx_swap="outerHTML",
                        cls="select w-full max-w-xs",
                        id="provider"
                    ),
                    for_="provider"
                )
            ),
            Form(

                *inputs,
                Button("Submit", hx_post="/keys", hx_swap="outerHTML", hx_target="#key_modal")
            ),
            cls="modal-box w-[70vw] space-y-4"
        ),
        cls="modal",
        id="key_modal"
    )


def key_modal_page(provider, env_vars, model):
    form_inputs = []
    for key_name, env_var in env_vars.items():
        form_inputs.append(
            Label(
                env_var,
                Input(placeholder=key_name, id=env_var, type="password"),
            )
        )
    form_inputs.append(
        Label(
            "Model",
            Input(placeholder="Model", id="model", type="text", value=model),
        )
    )
    key_modal = get_key_modal(provider, form_inputs)
    modal_open_script = Script("key_modal.showModal()")
    return Div(
        key_modal,
        modal_open_script,
        cls="container",
        id="container"
    )