import shutil

from code_assistant.assistants import ManagerFactory
from code_assistant.routes import home, chat_message, code, edit, file_rt, upload, context, preview, fix_errors
from fasthtml.common import *

from code_assistant.constants.scroll_script_src import scroll_script_src
from code_assistant.constants.css_text import css_text
from code_assistant.constants.post_message_listener_src import post_message_listener_src
from code_assistant.util.file_util import get_mount_from_file
from code_assistant.constants.config import GENERATED_APPS_DIR

from importlib.resources import files


css = Style(css_text)

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com")
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
plink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css")
scrollScript = Script(scroll_script_src)

app_routes = []

print(f"Generated apps dir: {GENERATED_APPS_DIR}")
if not os.path.exists(GENERATED_APPS_DIR):
    print(f"Creating: {GENERATED_APPS_DIR}")
    os.makedirs(GENERATED_APPS_DIR)

    generated_apps_dir = files('code_assistant').joinpath('generated_apps')
    print(f"Copying files to : {GENERATED_APPS_DIR}")
    for file in generated_apps_dir.iterdir():
        if file.is_file():
            shutil.copy(file, GENERATED_APPS_DIR)

for root, dirs, files in os.walk(GENERATED_APPS_DIR):
    for file in files:
        if file.endswith('.py'):
            mount = get_mount_from_file(file)
            app_routes.append(mount)

iframe_post_message_script = Script(post_message_listener_src, type="module")

app, rt = fast_app(hdrs=(tlink, dlink, css, scrollScript, plink, iframe_post_message_script), routes=app_routes)

#setup_toasts(app) work around toast bug until fasthtml 5.2 ships
app.hdrs += (Style(toast_css), Script(toast_js, type="module"))
app.after.append(toast_after)

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