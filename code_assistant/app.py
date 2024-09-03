import json
import traceback
from uuid import uuid1

from astra_assistants.tools.structured_code.program_cache import StructuredProgram
from astra_assistants.tools.structured_code.util import add_chunks_to_cache
from fasthtml.common import *
from starlette.datastructures import UploadFile

from code_assistant.assistants import ManagerFactory
from code_assistant.util.constants import htmx_context
from code_assistant.util.constants.big_fasthtml_context import big_fasthtml_context
from code_assistant.util.constants.css_text import css_text
from code_assistant.util.constants.small_fasthtml_context import small_fasthtml_context
from code_assistant.util.file_util import get_mount_from_file
from code_assistant.util.constants.htmx_context import starter_app

css = Style(css_text)

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
plink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css")
scrollScript = Script('''
document.addEventListener('DOMContentLoaded', function() {
    // Function to auto-scroll chat to the bottom on new message
    function scrollToBottom() {
        const chatList = document.getElementById('chatlist');
        if (chatList) {
            chatList.scrollTop = chatList.scrollHeight;
        }
    }
    
    // Observe mutations in the chatlist to auto-scroll
    const chatListElement = document.getElementById('chatlist');
    if (chatListElement) {
        const observer = new MutationObserver(scrollToBottom);
        observer.observe(chatListElement, { childList: true });
    }
});
''')

app_routes = []

for root, dirs, files in os.walk('code_assistant/generated_apps'):
    for file in files:
        if file.endswith('.py'):
            mount = get_mount_from_file(file)
            app_routes.append(mount)

iframe_post_message_script = Script("""
        // Listen for messages from the iframe
        window.addEventListener('message', function(event) {
            if (event.data.type === 'showMessage') {
                let error_message = document.getElementById('error-message')
                error_message.style.display = 'block';
                let heal_data = document.getElementById('heal_data')
                content = JSON.stringify(event.data.content)
                heal_data.value = content
            }
        });
""")

app = FastHTML(hdrs=(tlink, dlink, css, scrollScript, plink, iframe_post_message_script), routes=app_routes)

setup_toasts(app)
rt = app.route

manager = ManagerFactory(app)

messages = []


def get_main_content():
    return Div(
        get_code_section(),
    )


heal_form = Form(
    Input(id="heal_data", name="heal_data", type="hidden", value=""),
    Button("Self Heal", cls="btn btn-primary", hx_post="/fix_errors", hx_disabled_elt=".btn",
           hx_target="#chatlist", hx_swap="beforeend", ),
    id="error-message",
    hx_swap_oob="true",
    style="display:none;",
    hx_trigger="errorOccurred from:body",
    cls="file-display flex-item",
)


def get_code_section():
    return Section(
        Header(H1("Code Assistant")),

        Div(
            Div(
                Div(
                    Button("Context", id="modal", onclick="context_modal.showModal()", cls="btn"),
                    Dialog(
                        Div(
                            Form(
                                Button("✕", cls="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"),
                                method="dialog",
                            ),
                            P("Context", cls="text-lg font-bold"),
                            Form(
                                Div(
                                    Label(
                                        "FastHTML Context (large)",
                                        Input(
                                            id="big_fasthtml",
                                            name="big_fasthtml",
                                            type="checkbox",
                                            cls="toggle",
                                            checked=False
                                        ),
                                        for_="big_fasthtml"
                                    ),
                                    Label(
                                        "FastHTML Context (small)",
                                        Input(
                                            id="small_fasthtml",
                                            name="small_fasthtml",
                                            type="checkbox",
                                            cls="toggle",
                                            checked=True
                                        ),
                                        for_="small_fasthtml"
                                    ),
                                    Label(
                                        "HTMX Context",
                                        Input(
                                            id="htmx",
                                            name="htmx",
                                            type="checkbox",
                                            cls="toggle",
                                            checked=False
                                        ),
                                        for_="fasthtml"
                                    ),
                                    cls="form-control",
                                ),
                                hx_trigger="change", hx_encoding='multipart/form-data', hx_get='/context',
                                hx_swap="none", cls="label cursor-pointer",
                                #, hx_vals='{"fasthtml": fasthtml}',
                            ),
                            cls="modal-box w-[70vw]"
                        ),
                        id="context_modal", cls="modal"
                    ),
                ),
                Div(*[ChatMessage(index) for index, message in enumerate(messages)],
                    id="chatlist", cls="chat-box overflow-y-auto code-output"),
                #Div(id="code-output", cls="code-output"),
                Span(id="code-spinner", cls="loading loading-spinner loading-sm spinner"),
                ChatControls(),
                cls="flex-item"
            ),
            Div(cls="divider divider-horizontal"),
            Div(
                Form(
                    Div(
                        SelectFile(manager.programs, 0),

                        Div(
                            Label(
                                "Line Numbers",
                                Input(
                                    id="linenumbers",
                                    name="linenumbers",
                                    type="checkbox",
                                    cls="toggle",
                                    checked=True
                                ),
                                cls="label cursor-pointer",
                                for_="linenumbers"
                            ),
                            cls="form-control"
                        ),
                        cls="flex-container"
                    ),
                    FileOutput(),
                    cls="file-list",
                    hx_swap="innerHTML", hx_trigger="change", hx_get="/file", hx_params="*", hx_target="#file-output",
                ),
                Div(
                    Form(
                        Div(
                            Label(
                                "Preview",
                                Input(
                                    id="preview",
                                    name="preview",
                                    type="checkbox",
                                    cls="toggle disabled",
                                    checked=False,
                                    disabled=True
                                ),
                                hx_trigger="change", hx_post="/preview", cls="label cursor-pointer", hx_swap="none",
                                for_="linenumbers"
                            ),
                            id="preview-toggle",
                            cls="form-control"
                        ),
                    ),
                    heal_form,
                    cls="flex-container"
                ),
                Form(
                    Input(name='uploadfile', type='file', cls='file-input file-input-bordered w-full max-w-xs'),
                    Button("Upload", cls='btn'),
                    Progress(id='progress', value='0', max='100'),
                    id='form', hx_encoding='multipart/form-data', hx_post='/upload', hx_target="#file-output"
                ),
                Script("""
htmx.on('#form', 'htmx:xhr:progress', function(evt) {
    htmx.find('#progress').setAttribute('value', evt.detail.loaded/evt.detail.total * 100)
});
"""),
                cls="file-display flex-item"
            ),
            cls="flex-container"
        ),
    )


@rt('/')
async def get(session):
    message_objects = []
    #message_objects= client.beta.threads.messages.list(thread_id="thread_94kTIBLZI918vFI6OLzpnOFqmiH9SI7L", order="asc").data

    for message_object in message_objects:
        msg = message_object.content[0].text.value
        if message_object.role == "user":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})
    return Body(
        Div(
            #get_sidebar(),
            get_main_content(),
            cls="container"
        )
    )


# Chat message component, polling if message is still being generated
def ChatMessage(msg_idx):
    msg = messages[msg_idx]
    text = "..." if msg['content'] == "" else msg['content']
    bubble_class = "chat-bubble" if msg['role'] == 'user' else 'chat-bubble'
    chat_class = "chat-end" if msg['role'] == 'user' else 'chat-start'
    generating = 'generating' in messages[msg_idx] and messages[msg_idx]['generating']
    editable = "true" if msg['role'] == 'user' else 'false'
    stream_args = {"hx_trigger": "every 0.1s", "hx_swap": "outerHTML", "hx_get": f"/chat_message/{msg_idx}"}
    return Div(Div(msg['role'], cls="chat-header"),
               Div(text, cls=f"chat-bubble {bubble_class} whitespace-pre-wrap", contenteditable=editable),
               cls=f"chat {chat_class}", id=f"chat-message-{msg_idx}",
               **stream_args if generating else {})


# Route that gets polled while streaming
@app.get("/chat_message/{msg_idx}")
async def get_chat_message(msg_idx: int):
    if msg_idx >= len(messages): return ""
    return ChatMessage(msg_idx)


# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Textarea(type="text", name='msg', id='msg-input',
                    placeholder="Type a message",
                    cls="textarea textarea-bordered textarea-lg w-full max-w-xs", hx_swap_oob='true',
                    onkeypress="if(event.key === 'Enter' && !event.shiftKey){document.getElementById('chat-send-button').click(); event.preventDefault(); this.value = '';}"
                    )


def FileOutput(content: str = None, linenumbers: bool = True):
    children = []
    if content is None:
        return Div(Div(id="file-output"), id="file-content", cls="file-content whitespace-pre-wrap", hx_swap_oob='true')

    if linenumbers:
        for i, line in enumerate(content.split("\n")):
            children.append(Pre(Code(line), data_prefix=i + 1))
    else:
        children.append(Pre(content, contenteditable="true"))
    file_output = Div(
        Div(id="file-output", *children),
        id="file-content", cls="file-content mockup-code", hx_swap_oob='true'
    )
    return file_output


def SelectFile(program_cache=None, selected_index=None, disabled=False):
    if program_cache is None:
        return Select(id="fileselect", hx_swap_oob='true')

    if selected_index is None:
        selected_index = len(program_cache)

    options = [Option("Select a file", value="")]
    if selected_index == 0:
        options = [Option("Select a file", value="", selected=True)]

    file_list = []
    i = 1
    for program_entry in program_cache:
        structured_program = program_entry.program
        option = None
        if i == selected_index:
            option = Option(structured_program.filename, value=program_entry.program_id, selected=True)
        else:
            option = Option(structured_program.filename, value=program_entry.program_id)
        found_option = False
        for each_option in options.copy():
            if option.children[0] == each_option.children[0]:
                options.remove(each_option)
                options.append(option)
                found_option = True
        if not found_option:
            options.append(option)
        i += 1

    return (
        Select(
            *options,
            id="fileselect",
            hx_swap_oob='true',
            cls="select select-bordered w-full max-w-xs",
            disabled=disabled
        ),
    )


def ChatControls(programid: str = None):
    if programid is None:
        return Div(
            Form(
                Div(
                    ChatInput(),
                    Button("Send", id="chat-send-button", cls="btn", hx_disabled_elt=".btn")
                ),
                hx_post="/code", hx_target="#chatlist", hx_swap="beforeend",
                cls="flex space-x-2 mt-2",
            ),
            id="chat-controls",
            hx_swap_oob='true'
        )
    return Div(
        Form(
            Div(
                ChatInput(),
                Button("Send", id="chat-send-button", cls="btn btn-primary", hx_disabled_elt=".btn")
            ),
            id="chat-controls",
            hx_post=f"/edit/{programid}", hx_target="#chatlist", hx_swap="beforeend",
            cls="flex space-x-2 mt-2",
        ),
        id="chat-controls",
        hx_swap_oob='true'
    )


# Run the chat model in a separate thread
@threaded
def get_response(r, optional_text=None):
    try:
        idx = len(messages) - 1
        if optional_text is None or not isinstance(optional_text, str):
            optional_text = ""
        messages[idx]["content"] = optional_text
        for chunk in r:
            messages[idx]["content"] += chunk
        if messages[idx]["content"] == "":
            messages[idx]["content"] = "Done."
        messages[idx]["generating"] = False
    except Exception as e:
        trace = traceback.format_exc()
        print(f"e: {e} trace: {trace}")
        messages[idx]["content"] += f"e: {e} trace: {trace}"
        messages[idx]["generating"] = False


@rt("/code")
async def post(session, msg: str):
    idx = len(messages)
    msg = f"Here is an example FastHTML app: {starter_app}\nMake a new app per the following instructions:\n## Description:\n{msg}"
    messages.append({"role": "user", "content": msg})

    print(f"New app message: {msg}")
    r = manager.code_manager.stream_thread(
        content=msg,
        tool_choice=manager.code_generator,
        additional_instructions="\n".join(manager.additional_instructions)
    )  # Send message to chat model (with streaming)

    messages.append({"role": "assistant", "generating": True, "content": ""})  # Response initially blank
    first_chunk = add_chunks_to_cache(r, manager.programs, get_response)
    output = first_chunk['output']
    programid = first_chunk['program_id']
    if output is not None:
        return (
            ChatMessage(idx),
            ChatMessage(idx + 1),
            FileOutput(output.to_string(False)),
            SelectFile(manager.code_generator.program_cache),
            ChatInput(),
            ChatControls(programid=programid),
            PreviewCheckbox(programid, False)
        )
    else:
        return (
            ChatMessage(idx),
            ChatMessage(idx + 1),
            ChatInput(),
            ChatControls()
        )


@app.post("/edit/{programid}")
async def edit_program(session, msg: str, programid: str = None, tool_choice: str = None):
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
        first_chunk = add_chunks_to_cache(r, manager.programs, get_response)
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
                ChatMessage(idx),
                Div(Div("Tool", cls="chat-header"),
                    Div(f"{type(manager.code_manager.tool_call_arguments).__name__} {manager.code_manager.tool_call_arguments}",
                        cls=f"whitespace-pre-wrap"),
                    ),
                ChatMessage(idx + 1),
                FileOutput(code),
                SelectFile(manager.code_generator.program_cache, selected_index),
                ChatInput(),
                PreviewCheckbox(programid, False)
            )
        else:
            return (
                ChatMessage(idx),
                ChatMessage(idx + 1),
                ChatInput(),
            )
    except Exception as e:
        trace = traceback.format_exc()
        print(f"e: {e} trace: {trace}")
        messages[idx]["content"] += f"e: {e} trace: {trace}"
        messages[idx]["generating"] = False
        add_toast(session, f"error try again", "error")
        return (
            ChatMessage(idx),
            ChatMessage(idx + 1),
            ChatInput(),
        )


def PreviewCheckbox(fileselect: str, checked: bool = False):
    return Div(
        Label(
            "Preview",
            Input(
                id="preview",
                name="preview",
                type="checkbox",
                cls="toggle disabled",
                checked=False,
            ),
            hx_trigger="change", hx_post=f"/preview/{fileselect}", cls="label cursor-pointer", hx_swap="none",
            for_="linenumbers"
        ),
        id="preview-toggle",
        cls="form-control",
        hx_swap_oob='true'
    )


@rt("/file")
async def get(session, fileselect: str = None, linenumbers: bool = None):
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

    cache = manager.programs

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


@rt("/upload")
async def post(session, uploadfile: UploadFile):
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


@rt("/context")
async def get(session, fasthtml: str = None, small_fasthtml: str = None, htmx: str = None):
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


@rt("/preview/{fileselect}")
async def post(session, preview: str = None, fileselect: str = None):
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


@rt('/fix_errors')
async def post(session, heal_data: str):
    data = json.loads(heal_data)
    error_message = data['error_message']
    filename = data['filename']
    program_id = None
    if 'program_id' in data:
        program_id = data['program_id']
    else:
        for program_entry in manager.programs:
            if program_entry.program.filename == filename:
                program_id = program_entry.program_id
                break

    assert program_id is not None, f"Program not found in cache for filename {filename}"
    message = "Please rewrite the app to fix the following error: " + error_message
    print(f"healing message {message}")
    output = await edit_program(session, message, program_id, manager.code_rewriter)

    return output + (heal_form,)
