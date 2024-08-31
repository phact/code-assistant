import json

from fasthtml.common import *

plink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css")


def get_error_app(filename: str, error: str, trace: str, program_id: str, JS):
    script = Script(JS)
    app = FastHTML(hdrs=(plink, script))
    rt = app.route

    content = json.dumps({"error_message": error, "filename": filename, "program_id": program_id})

    @rt('/')
    def get():
        return Div(
            H1(f"Error loading app {filename}", id="error-title"),
            P(f"Error loading app {filename}: {error}"),
            P(f"trace: {trace}"),
        )


    return app

