from code_assistant.assistants import ManagerFactory
from code_assistant.routes import home, chat_message, code, edit, file_rt, upload, context, preview, fix_errors
from fasthtml.common import *

from code_assistant.util.constants.scroll_script_src import scroll_script_src
from code_assistant.util.constants.css_text import css_text
from code_assistant.util.constants.post_message_listener_src import post_message_listener_src
from code_assistant.util.file_util import get_mount_from_file

css = Style(css_text)

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
plink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css")
scrollScript = Script(scroll_script_src)

app_routes = []

for root, dirs, files in os.walk('generated_apps'):
    for file in files:
        if file.endswith('.py'):
            mount = get_mount_from_file(file)
            app_routes.append(mount)

iframe_post_message_script = Script(post_message_listener_src)

app, rt = fast_app(hdrs=(tlink, dlink, css, scrollScript, plink, iframe_post_message_script), routes=app_routes)
#app, rt = fast_app(hdrs=(tlink, dlink, css, plink, scrollScript))

setup_toasts(app)

manager = ManagerFactory(app)

messages = []

app.state.manager = manager
app.state.messages = messages

app.get('/')(home.page)
app.get("/chat_message/{msg_idx}")(chat_message.page)
app.post("/code")(code.page)
app.post("/edit/{programid}")(edit.page)
app.get("/file")(file_rt.page)
app.post("/upload")(upload.page)
app.get("/context")(context.page)
app.post("/preview/{fileselect}")(preview.page)
app.post('/fix_errors')(fix_errors.page)

serve()