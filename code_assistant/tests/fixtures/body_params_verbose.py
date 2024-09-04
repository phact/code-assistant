from fasthtml.common import *

app = FastHTML()

@app.post('/thing_id')
async def select_vehicle(request):
    form_obj = await request.form()
    return f'id: {form_obj["id"]} name: {form_obj["name"]}'


@app.get('/')
def home():
    return Form(
        Input(id='id', type='text'), Input(id='name', type='text'), Button('Submit'),
        hx_post='/thing_id'
    )

serve()