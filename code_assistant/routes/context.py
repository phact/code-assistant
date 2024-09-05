from code_assistant.constants.htmx_context import htmx_context
from code_assistant.constants.big_fasthtml_context import big_fasthtml_context
from code_assistant.constants.small_fasthtml_context import small_fasthtml_context


async def page(request, fasthtml: str = None, small_fasthtml: str = None, htmx: str = None):
    manager = request.app.state.manager
    if fasthtml == 'on':
        if not big_fasthtml_context in manager.additional_instructions:
            manager.additional_instructions.append(big_fasthtml_context)
    else:
        if big_fasthtml_context in manager.additional_instructions:
            manager.additional_instructions.remove(big_fasthtml_context)

    if small_fasthtml == 'on':
        if not small_fasthtml_context in manager.additional_instructions:
            manager.additional_instructions.append(small_fasthtml_context)
    else:
        if small_fasthtml_context in manager.additional_instructions:
            manager.additional_instructions.remove(small_fasthtml_context)

    if htmx == 'on':
        if not htmx_context in manager.additional_instructions:
            manager.additional_instructions.append(htmx_context)
    else:
        if htmx_context in manager.additional_instructions:
            manager.additional_instructions.remove(htmx_context)
