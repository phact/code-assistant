from code_assistant.app import *

async def page(request, preview: str = None, fileselect: str = None):
    manager = request.app.state.manager
    selected_index = 0
    i = 1
    for entry in manager.programs:
        if entry.program_id == fileselect:
            selected_index = i
        i += 1
    if preview is not None and preview == "on":
        for entry in manager.programs:
            if fileselect == entry.program_id:
                fileselect = entry.program.filename
        path = fileselect.split(".")[0]
        return (
            Div(
                Div(
                    Div(f"/{path}/", cls="input"),
                    cls="mockup-browser-toolbar"),
                Iframe(src=f"/{path}/", cls="bg-base-200 flex justify-center px-4 py-4 w-full h-full"),
                #Div("Hello!", cls="bg-base-200 flex justify-center px-4 py-16"),
                id="file-content", cls="file-content mockup-browser bg-base-300 border", hx_swap_oob='true',
            ),
            SelectFile(manager.programs, selected_index, True)
        )
    else:
        content = ""
        for program_entry in manager.programs:
            if program_entry.program_id == fileselect:
                content = program_entry.program.to_string(False)
        return (
            FileOutput(content, linenumbers=True),
            SelectFile(manager.programs, selected_index, False)
        )
