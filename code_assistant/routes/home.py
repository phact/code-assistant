from code_assistant.app import get_main_content
from code_assistant.main import *
from fasthtml.common import *


async def page(request):
    message_objects = []
    #message_objects= client.beta.threads.messages.list(thread_id="thread_94kTIBLZI918vFI6OLzpnOFqmiH9SI7L", order="asc").data

    for message_object in message_objects:
        msg = message_object.content[0].text.value
        if message_object.role == "user":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})
    return Div(
        #get_sidebar(),
        get_main_content(request.app.state.manager, request.app.state.messages),
        cls="container"
    )