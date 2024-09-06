from fasthtml.common import *
import random

css = Style("""
    body {
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        background-color: #f0f0f0;
    }
    #game {
        text-align: center;
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .buttons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }
    button {
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
    }
    .result {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
""")

app = FastHTML(hdrs=[Script(src="https://unpkg.com/htmx.org@1.9.2"), css])
rt = app.route

choices = ['rock', 'paper', 'scissors']

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!"
    elif (
        (player_choice == 'rock' and computer_choice == 'scissors') or
        (player_choice == 'paper' and computer_choice == 'rock') or
        (player_choice == 'scissors' and computer_choice == 'paper')
    ):
        return "You win!"
    else:
        return "Computer wins!"

@rt('/')
def get():
    return Div(
        H1('Rock Paper Scissors'),
        Div(
            Button('Rock', hx_get='/play/rock', hx_target='#result'),
            Button('Paper', hx_get='/play/paper', hx_target='#result'),
            Button('Scissors', hx_get='/play/scissors', hx_target='#result'),
            className='buttons'
        ),
        Div(id='result'),
        id='game'
    )

@rt('/play/{choice}')
def play(choice):
    player_choice = choice.lower()
    computer_choice = random.choice(choices)
    result = determine_winner(player_choice, computer_choice)
    
    return Div(
        P(f"You chose: {player_choice.capitalize()}"),
        P(f"Computer chose: {computer_choice.capitalize()}"),
        P(f"Result: {result}"),
        className='result'
    )

serve()