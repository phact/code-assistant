from code_assistant.app import *


async def page(request, program_id: str = None, linenumbers: bool = None):
    if program_id is None or program_id == "" or program_id == "Select a project":
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
                    hx_trigger="change",
                    hx_post=f"/preview/{program_id}",
                    cls="label cursor-pointer",
                    hx_swap="none",
                    for_="linenumbers"
                ),
                id="preview-toggle",
                cls="form-control",
                hx_swap_oob='true'
            ),
        )

    projects = request.app.state.manager.projects
    programs = request.app.state.manager.programs

    # Currently only one program per project
    output = programs.get(program_id).program

    return (
        FileOutput(output.to_string(with_line_numbers=False), linenumbers=linenumbers),
        ChatControls(program_id),
        PreviewCheckbox(program_id, False)
    )
