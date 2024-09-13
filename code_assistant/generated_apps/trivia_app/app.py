from fasthtml.common import *
import random

style = Style("""
    body {
        background-color: #f4f1ea;
        font-family: 'Arial', sans-serif;
        color: #4a3f35;
    }
    form {
        background-color: #d8c3a5;
        border: 2px solid #8e8d8a;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: auto;
        margin-top: 50px;
    }
    div {
        padding: 10px 0;
    }
    input[type="submit"] {
        background-color: #8e8d8a;
        color: #f4f1ea;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
        border-radius: 5px;
    }
    input[type="submit"]:hover {
        background-color: #4a3f35;
    }
    a {
        color: #4a3f35;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    .success {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        margin-top: 20px;
    }
    .error {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        margin-top: 20px;
    }
""")

app = FastHTML(hdrs=style)

# Sample trivia data
questions_data = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Lyon", "Marseille", "Nice"],
        "correct_answer": "Paris"
    },
    {
        "question": "What is the capital of Spain?",
        "options": ["Madrid", "Barcelona", "Seville", "Valencia"],
        "correct_answer": "Madrid"
    },
    {
        "question": "What is the capital of Italy?",
        "options": ["Rome", "Milan", "Naples", "Turin"],
        "correct_answer": "Rome"
    },
    {
        "question": "What is the capital of Germany?",
        "options": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
        "correct_answer": "Berlin"
    }
]

current_correct_answer = None

# Route for displaying the trivia question
@app.route('/')
def get():
    global current_correct_answer

    # Select a random question
    selected_question = random.choice(questions_data)
    question = selected_question["question"]
    options = selected_question["options"]
    current_correct_answer = selected_question["correct_answer"]

    random.shuffle(options)

    form_elements = [
        Div(question),
        *[Div(Input(type='radio', name='answer', value=option), option) for option in options],
        Div(Input(type='submit', value='Submit'))
    ]
    return Form(*form_elements, method='post')

# Route for handling the answer submission
@app.post('/')
def post(answer: str):
    global current_correct_answer

    if answer == current_correct_answer:
        return Div(Div(f'Correct! The capital is indeed {current_correct_answer}.', _class='success'), A('Try Again?', href='/'))
    else:
        return Div(Div('Incorrect. Try Again.', _class='error'), A('Back', href='/'))

# Start the FastHTML app
serve()