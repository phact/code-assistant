from code_assistant.app import *

async def page(request, fileselect: str = None, linenumbers: bool = None):
    if fileselect is None or fileselect == "" or fileselect == "Select a file":
        return (
            FileOutput(),
            ChatControls(programid=None),
            #Button("Preview", cls="btn btn-disabled", id="preview-toggle", hx_swap_oob='true')
            Div(
                Label(
                    "Preview",
                    Input(
                        id="preview",
                        name="preview",
                        type="checkbox",
                        cls="toggle disabled",
                        checked=False,
                        disabled=True,
                    ),
                    hx_trigger="change", hx_post=f"/preview/{fileselect}", cls="label cursor-pointer", hx_swap="none",
                    for_="linenumbers"
                ),
                id="preview-toggle",
                cls="form-control",
                hx_swap_oob='true'
            ),
        )

    cache = request.app.state.manager.programs

    output = None
    for program_entry in cache:
        if program_entry.program_id == fileselect:
            output = program_entry.program
            break

    return (
        FileOutput(output.to_string(with_line_numbers=False), linenumbers=linenumbers),
        ChatControls(fileselect),
        PreviewCheckbox(fileselect, False)
    )

