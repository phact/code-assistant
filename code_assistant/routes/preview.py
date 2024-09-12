from code_assistant.app import *

async def page(request, preview: str = None, program_id: str = None):
    programs = request.app.state.manager.programs
    projects = request.app.state.manager.projects

    selected_index = 0
    i = 1
    for project in projects.projects:
        # Currently there is only one program per project
        for project_program_id in project.filename_to_program_id.values():
            if program_id == project_program_id:
                selected_index = i
            i += 1
    filename = projects.get_filename_by_program_id(program_id).replace('/app.py', '')
    if preview is not None and preview == "on":
        return (
            Div(
                Div(
                    Div(f"/{filename}/", cls="input"),
                    cls="mockup-browser-toolbar"),
                Iframe(src=f"/{filename}/", cls="bg-base-200 flex justify-center px-4 py-4 w-full h-full"),
                #Div("Hello!", cls="bg-base-200 flex justify-center px-4 py-16"),
                id="file-content", cls="file-content mockup-browser bg-base-300 border", hx_swap_oob='true',
            ),
            SelectFile(programs, projects, selected_index, True)
        )
    else:
        content = programs.get(program_id).program.to_string(False)
        #for project in projects.projects:
        #    # Currently there is only one program per project
        #    for filename, program_id in project.program_id_to_filename.items():
        #        if fileselect == filename:
        #            content = programs.get(program_id).program.to_string(False)
        return (
            FileOutput(content, linenumbers=True),
            SelectFile(programs, projects, selected_index, False)
        )
