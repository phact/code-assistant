import json

from code_assistant.app import *
from code_assistant.routes import edit


async def page(request, session, heal_data: str):
    manager = request.app.state.manager
    data = json.loads(heal_data)
    error_message = data['error_message']
    filename = data['filename']
    program_id = None
    if 'program_id' in data:
        program_id = data['program_id']
    else:
        program_id = manager.programs.cache.get(filename.replace('.py', '')).program_id
    assert program_id is not None, f"Program not found in cache for filename {filename}"

    message = "Please rewrite the app to fix the following error: " + error_message
    print(f"healing message {message}")
    output = await edit.page(request, session, message, program_id, manager.code_rewriter)

    return output + (heal_form,)