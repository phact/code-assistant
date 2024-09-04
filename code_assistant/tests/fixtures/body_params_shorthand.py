from fasthtml.common import *

app = FastHTML()

@app.post('/thing_id')
async def select_vehicle(id: str, name: str):
    return f'id: {id} name: {name}'


@app.get('/')
def home():
    return Form(
        Input(id='id', type='text'), Input(id='name', type='text'), Button('Submit'),
        hx_post='/thing_id'
    )

serve()