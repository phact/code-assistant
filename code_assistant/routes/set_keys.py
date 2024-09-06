import os
from fasthtml.common import Script
from code_assistant.constants import config


async def page(request):
    form = await request.form()
    for key, value in form.items():
        if key == "model":
            request.app.state.model = value
        else:
            os.environ[key.upper()] = value
    return Script("window.location.href = '/';")
