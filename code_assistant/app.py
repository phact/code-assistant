import traceback

from fasthtml.common import *

def get_main_content(manager, messages):
    return Div(
        get_code_section(manager, messages),
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


def get_code_section(manager, messages):
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
                Div(*[ChatMessage(messages, index) for index, message in enumerate(messages)],
                    id="chatlist", cls="chat-box overflow-y-auto code-output"),
                #Div(id="code-output", cls="code-output"),
                Span(id="code-spinner", cls="loading loading-spinner loading-sm spinner"),
                ChatControls(),
                PicoBusy(),
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


# Chat message component, polling if message is still being generated
def ChatMessage(messages, msg_idx):
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


def get_response_factory(messages):
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

    return get_response






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


