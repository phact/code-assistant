from random import choice
from fasthtml import FastHTML
from fasthtml.common import Div, Form, P, Input, Button, serve, Style

# Define CSS to style the application
css = Style("""
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f9;
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    .riddle-question {
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    #riddle-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .submit-btn, .new-riddle-btn {
        background-color: #6200ea;
        color: #ffffff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .submit-btn:hover, .new-riddle-btn:hover {
        background-color: #3700b3;
    }
    #answer-response {
        margin-top: 10px;
        font-weight: bold;
    }
""")

app = FastHTML(hdrs=[css])
rt = app.route

# List of riddles and their answers
riddles = [
    {"question": "What has keys but can't open locks?", "answer": "Keyboard"},
    {"question": "What runs around a yard without moving?", "answer": "Fence"},
    {"question": "What can travel around the world while staying in a corner?", "answer": "Stamp"},
    {"question": "What has a heart that doesn’t beat?", "answer": "Artichoke"},
]

current_riddle = None

def init_riddle():
    global current_riddle
    if current_riddle is None:
        current_riddle = choice(riddles)

@rt('/')
def get():
    global current_riddle
    init_riddle()
    return Div(
        Div(
            Form(
                Div(
                    P(current_riddle["question"], cls='riddle-question'),
                    Input(type='text', id='user-answer', name='user_answer', placeholder='Your answer here'),
                    Button("Submit", type='submit', hx_post="/check-answer", hx_target="#answer-response", cls='submit-btn'),
                    id='riddle-section'
                ),
            ),
            Div(id='answer-response')
        ),
        title="Riddle Game"
    )

@app.post('/check-answer')
def check_answer(user_answer: str):
    if user_answer.strip().lower() == current_riddle["answer"].lower():
        response = "Correct! Great job."
    else:
        response = "Incorrect. Try again!"

    return Div(
        P(response, id='answer-response'),
        Button("Try Another Riddle", hx_post="/new-riddle", hx_target="#riddle-section", cls='new-riddle-btn')
    )

@app.post('/new-riddle')
def new_riddle():
    global current_riddle
    current_riddle = choice(riddles)
    return Div(
        P(current_riddle["question"], cls='riddle-question'),
        Input(type='text', id='user-answer', name='user_answer', placeholder='Your answer here'),
        Button("Submit", type='submit', hx_post="/check-answer", hx_target="#answer-response", cls='submit-btn')
    )

serve()