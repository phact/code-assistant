from fasthtml.common import *

app = FastHTML()

@app.route('/')
def get():
    form = Form(
        Input(id='expression', placeholder='Enter Calculation',
              style='border: 2px dashed pink; background-color: #fbe4ff; font-family: "Comic Sans MS", cursive; padding: 10px; margin-bottom: 10px;'),
        Div(
            Div(
                Button('1', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=1", hx_swap='outerHTML'),
                Button('2', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=2", hx_swap='outerHTML'),
                Button('3', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=3", hx_swap='outerHTML'),
                Button('+', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=%2B", hx_swap='outerHTML'),
                style='display: flex; justify-content: space-around; margin-bottom: 10px;'
            ),
            Div(
                Button('4', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=4", hx_swap='outerHTML'),
                Button('5', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=5", hx_swap='outerHTML'),
                Button('6', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=6", hx_swap='outerHTML'),
                Button('-', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=-", hx_swap='outerHTML'),
                style='display: flex; justify-content: space-around; margin-bottom: 10px;'
            ),
            Div(
                Button('7', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=7", hx_swap='outerHTML'),
                Button('8', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=8", hx_swap='outerHTML'),
                Button('9', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=9", hx_swap='outerHTML'),
                Button('*', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=*", hx_swap='outerHTML'),
                style='display: flex; justify-content: space-around; margin-bottom: 10px;'
            ),
            Div(
                Button('0', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=0", hx_swap='outerHTML'),
                Button('/', hx_trigger='click', hx_target='#expression', hx_post="/update_expression?value=/", hx_swap='outerHTML'),
                style='display: flex; justify-content: space-around; margin-bottom: 10px;'
            ),
            Button('Calculate', hx_post='/calculate', hx_target='#result', style='background-color: #ffc0cb; color: white; border-radius: 12px; padding: 10px 20px; font-size: 16px;'),
            Button('Clear', type='button', hx_post='/clear', hx_target='#expression', hx_swap='outerHTML', style='background-color: #ffc0cb; color: white; border-radius: 12px; padding: 10px 20px; font-size: 16px;'),
            style='background-color: #f0e6f7; border: 1px solid lavender; border-radius: 15px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);'
        )
    )
    result_container = Div('', id='result',
                           style='margin-top: 15px; color: #800080; font-size: 18px; text-shadow: 1px 1px #e5e5e5;')
    return Titled('Calculator - Magic Edition', form, result_container,
                  style='background-image: url("https://example.com/fairytale_background.jpg"); background-size: cover; padding: 40px; border-radius: 25px; text-align: center; width: 220px;')

@app.post('/update_expression')
def update_expression(value: str, expression: str = None):
    if expression is None:
        expression = ''
    expression += value
    return Input(id='expression', placeholder='Enter Calculation', value=expression,
          style='border: 2px dashed pink; background-color: #fbe4ff; font-family: "Comic Sans MS", cursive; padding: 10px; margin-bottom: 10px;'),

@app.post('/calculate')
def calculate(expression: str):
    try:
        result = str(eval(expression))
    except Exception as e:
        result = f'Error: {e}'
    return Div(f'Result: {result}')

@app.post('/clear')
def clear_expression():
    return Input(id='expression', placeholder='Enter Calculation', value='',
           style='border: 2px dashed pink; background-color: #fbe4ff; font-family: "Comic Sans MS", cursive; padding: 10px; margin-bottom: 10px;')

serve()