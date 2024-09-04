from fasthtml.common import *

app = FastHTML()

@app.post('/thing_id')
def select_vehicle(id: str): # NOTICE the type hint for id, this is required or the variable will be set to None
    return id


@app.get('/')
def home():
    return Form(Input(id='id', type='text'), Button('Submit'), action='/thing_id', method='post')

serve()