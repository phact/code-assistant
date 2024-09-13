from fasthtml.common import *

app = FastHTML()
rt = app.route

# A simple 9x9 grid example (partially filled)
initial_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

@rt('/')
def get():
    return Body(
        H1('Sudoku Game'),
        Form(
            Table(
                *[
                    Tr(
                        *[
                            Td(
                                Input(
                                    name=f'cell-{i}-{j}',
                                    value=(str(initial_grid[i][j]) if initial_grid[i][j] != 0 else ''),
                                    type='text',
                                    size=1,
                                    maxlength=1,
                                    cls='sudoku-cell ' + ('border-right ' if (j+1) % 3 == 0 else '') +
                                    ('border-bottom ' if (i+1) % 3 == 0 else ''),
                                    disabled=(True if initial_grid[i][j] != 0 else False)
                                ),
                            ) for j in range(9)
                        ]
                    ) for i in range(9)
                ],
                cls='sudoku-grid'
            ),
            Button('Check', type='submit', hx_post='/check', hx_trigger='click', hx_target='#result'),
            Div(id='result', style='margin-top:20px; font-size: 20px; color: #005500;')
        ),
        Style(
            '''
            .sudoku-grid {
                border-collapse: collapse;
            }
            .sudoku-cell {
                border: 1px solid #ccc;
                text-align: center;
            }
            .border-right {
                border-right: 3px solid #000;
            }
            .border-bottom {
                border-bottom: 3px solid #000;
            }
            '''
        )
    )

def is_valid_sudoku(grid):
    # Check each row
    for row in grid:
        if len(set(row) - {0}) != len([x for x in row if x != 0]):
            return False

    # Check each column
    for col in range(9):
        col_set = {grid[row][col] for row in range(9) if grid[row][col] != 0}
        if len(col_set) != len([grid[row][col] for row in range(9) if grid[row][col] != 0]):
            return False

    # Check each 3x3 subgrid
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_set = set()
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if grid[r][c] != 0:
                        if grid[r][c] in box_set:
                            return False
                        box_set.add(grid[r][c])

    return True

def is_complete(grid):
    for row in grid:
        if 0 in row:
            return False
    return True

@rt('/check')
async def post(request):
    form = await request.form()
    current_grid = [[initial_grid[i][j] for j in range(9)] for i in range(9)]

    for i in range(9):
        for j in range(9):
            value = form.get(f'cell-{i}-{j}', '')
            if value.isdigit():
                if initial_grid[i][j] == 0:  # Allow changes to editable cells
                    current_grid[i][j] = int(value)
            elif value:
                return Div(P("Invalid input detected!", id='result'))

    if not is_valid_sudoku(current_grid):
        result_text = "The solution is incorrect. Try again!"
    elif is_complete(current_grid):
        result_text = "Congratulations! The solution is correct."
    else:
        result_text = "The solution is correct so far, keep going!"

    return Div(P(result_text, id='result'))

serve()