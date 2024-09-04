from code_assistant.app import *
from astra_assistants.tools.structured_code.util import add_chunks_to_cache


async def page(request, session, msg: str, programid: str = None, tool_choice: str = None):
    messages = request.app.state.messages
    manager = request.app.state.manager

    try:
        idx = len(messages)
        program_string = None
        for program_entry in manager.programs:
            if program_entry.program_id == programid:
                program_string = program_entry.program.to_string()
                break

        messages.append({"role": "user", "content": msg})

        message_text = f"## Context:\nMake an edit for the program and describe your changes\n" + \
                       f"the current content of the program (with line numbers) is:\n{program_string}\n" + \
                       f"## Request:\nPerform the following changes to the program using the edit tools: \n{msg}"
        if program_string is None:
            return {"error": f"Program id {programid} not found"}
        manager.set_program_ids(programid)

        if tool_choice is None:
            tool_choice = "required"

        r = manager.code_manager.stream_thread(
            content=message_text,
            additional_instructions="\n".join(manager.additional_instructions),
            tool_choice=tool_choice
        )

        messages.append({"role": "assistant", "generating": True, "content": ""})  # Response initially blank
        first_chunk = add_chunks_to_cache(r, manager.programs, get_response_factory(messages))
        output = first_chunk['output']
        programid = first_chunk['program_id']

        selected_index = 0
        i = 1
        for program_entry in manager.programs:
            if program_entry.program_id == programid:
                selected_index = i
            i += 1

        if output is not None:
            if hasattr(output, 'to_string'):
                code = output.to_string(False)
            else:
                assert isinstance(output, str)
                code = output
            return (
                ChatMessage(messages, idx),
                Div(Div("Tool", cls="chat-header"),
                    Div(f"{type(manager.code_manager.tool_call_arguments).__name__} {manager.code_manager.tool_call_arguments}",
                        cls=f"whitespace-pre-wrap"),
                    ),
                ChatMessage(messages, idx + 1),
                FileOutput(code),
                SelectFile(manager.code_generator.program_cache, selected_index),
                ChatInput(),
                PreviewCheckbox(programid, False)
            )
        else:
            return (
                ChatMessage(messages, idx),
                ChatMessage(messages, idx + 1),
                ChatInput(),
            )
    except Exception as e:
        trace = traceback.format_exc()
        print(f"e: {e} trace: {trace}")
        messages[idx]["content"] += f"e: {e} trace: {trace}"
        messages[idx]["generating"] = False
        add_toast(session, f"error try again", "error")
        return (
            ChatMessage(messages, idx),
            ChatMessage(messages, idx + 1),
            ChatInput(),
        )
