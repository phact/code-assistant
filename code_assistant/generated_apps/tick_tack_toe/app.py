from fasthtml.common import *

css = Style('''
    .grid {
        display: grid;
        grid-template-columns: repeat(3, 100px);
        gap: 5px;
    }
    .box {
        width: 100px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid black;
        font-size: 24px;
        background-color: lightblue; /* Added background color */
        color: darkblue; /* Changed text color */
    }
''')

app = FastHTML(hdrs=(css,))
#app = FastHTML()
rt = app.route

# Board settings
board = [' ' for _ in range(9)]
# Current player
current_player = 'X'

def check_winner():
    # Check rows, columns, and diagonals for a winner
    win_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                     (0, 3, 6), (1, 4, 7), (2, 5, 8),
                     (0, 4, 8), (2, 4, 6)]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != ' ':
            return board[pos[0]]
    if ' ' not in board:
        return 'Draw'
    return None

def reset_board():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'

@rt('/')
def get():
    msg = f'{current_player}\'s Turn.'

    if winner := check_winner():
        if winner == 'Draw':
            msg = 'Draw! Resetting board...'
        else:
            msg = f'Player {winner} wins! Resetting board...'
        reset_board()

    board_elements = [Div(board[i], cls='box', hx_post=f'/move/{i}', hx_swap="outerHTML", hx_target="#container") for i in range(9)]
    grid = Div(*board_elements, cls='grid')
    return Titled('Tic-Tac-Toe', Div(H1('Tic-Tac-Toe'),
                                     H2(msg),
                                     grid),
                  id="container"
                  )

@rt('/move/{index}')
def post(index: int):
    global current_player
    if board[index] == ' ':
        board[index] = current_player
        current_player = 'O' if current_player == 'X' else 'X'
    return get()


serve()