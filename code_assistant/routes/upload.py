from uuid import uuid1
from code_assistant.app import *

from astra_assistants.tools.structured_code.program_cache import StructuredProgram


async def page(request, uploadfile: UploadFile):
    manager = request.app.state.manager
    text = (await uploadfile.read()).decode()
    filename = uploadfile.filename
    programid = str(uuid1())
    manager.programs.append(
        {
            "program_id": programid,
            "output": StructuredProgram(
                lines=text.split("\n"),
                filename=filename,
                language=filename.split(".")[1]
            )
        }
    )
    return (
        FileOutput(text, linenumbers=True),
        SelectFile(manager.programs),
        ChatControls(programid=programid)
    )