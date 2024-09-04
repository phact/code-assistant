from code_assistant.app import *
from code_assistant.util.constants.htmx_context import starter_app
from astra_assistants.tools.structured_code.util import add_chunks_to_cache


async def page(request, msg: str):
    messages = request.app.state.messages
    manager = request.app.state.manager
    idx = len(messages)
    msg = (f"Here is an example FastHTML app: {starter_app}\nMake a new app per the following instructions:\n## "
           f"Description:\n{msg}")
    messages.append({"role": "user", "content": msg})

    print(f"New app message: {msg}")
    r = manager.code_manager.stream_thread(
        content=msg,
        tool_choice=manager.code_generator,
        additional_instructions="\n".join(manager.additional_instructions)
    )  # Send message to chat model (with streaming)

    messages.append({"role": "assistant", "generating": True, "content": ""})  # Response initially blank
    first_chunk = add_chunks_to_cache(r, manager.programs, get_response_factory(messages))
    output = first_chunk['output']
    programid = first_chunk['program_id']
    if output is not None:
        return (
            ChatMessage(messages, idx),
            ChatMessage(messages, idx + 1),
            FileOutput(output.to_string(False)),
            SelectFile(manager.code_generator.program_cache),
            ChatInput(),
            ChatControls(programid=programid),
            PreviewCheckbox(programid, False)
        )
    else:
        return (
            ChatMessage(messages, idx),
            ChatMessage(messages, idx + 1),
            ChatInput(),
            ChatControls()
        )
