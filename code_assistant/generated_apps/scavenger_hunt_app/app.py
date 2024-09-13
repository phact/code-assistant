from fasthtml.common import *
from starlette.requests import Request

app = FastHTML()
rt = app.route

@rt('/')
def home():
    return Div(
        H1('Scavenger Hunt Challenge!', style="text-align:center; color: green;"),
        P('Welcome to the Scavenger Hunt! Find and upload photos of the following items:', style="text-align:center;"),
        Ul(
            Li('A red apple'),
            Li('A funny hat'),
            Li('A green leaf'),
            Li('A street sign'),
            Li('A blue car')
        ),
        Form(
            Input(type='file', name='photo', accept='image/*', style="display:block; margin:auto;"),
            Input(type='submit', value='Upload Photo', style="display:block; margin-top: 10px; margin:auto;"),
            enctype='multipart/form-data', method='post', action='/upload', hx_post="/upload", hx_target="#uploadResult", style="text-align:center;"
        ),
        Div(id='uploadResult', style="text-align:center; margin-top: 15px;"),
        style="max-width: 600px; margin: auto;"
    )

@rt('/upload', methods=['POST'])
async def upload(request: Request):
    form = await request.form()
    if 'photo' not in form:
        return Div(
            H1('Upload Error', style="text-align:center; color: red;"),
            P('Missing required field: uploadfile', style="text-align:center;"),
            hx_swap_oob=True
        )
    return Div(
        H1('Upload Successful!', style="text-align:center; color: green;"),
        P('Thank you for uploading your photo!', style="text-align:center;"),
        hx_swap_oob=True
    )

serve()