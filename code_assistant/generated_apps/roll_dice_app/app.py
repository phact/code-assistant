from fasthtml.common import FastHTML, Style, Div, Button, Script, serve

styles = '''
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 100vh;
        margin: 0;
        background-color: #f0f8ff;
        font-family: Arial, sans-serif;
    }
    
    #dice-result {
        font-size: 2.5em;
        margin-top: 20px;
        color: #333;
        text-align: center;
        min-width: 220px; /* Consistent width to avoid shifts */
        transition: color 0.3s ease;
    }
    
    button {
        padding: 12px 24px;
        font-size: 1.1em;
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
    }
'''

app = FastHTML()
rt = app.route

@rt('/')
def get():
    return Div(
        Style(styles),
        Button('Roll the Dice 🎲', onclick='rollDice()'),
        Div(id='dice-result')
    ) + Script('''
        function rollDice() {
            const resultElem = document.getElementById('dice-result');
            resultElem.innerText = '🎲';
            let rollInterval = setInterval(() => {
                resultElem.innerText = Math.floor(Math.random() * 6) + 1;
            }, 100);
        
            setTimeout(() => {
                clearInterval(rollInterval);
                resultElem.innerText = 'You rolled: ' + (Math.floor(Math.random() * 6) + 1);
                resultElem.style.color = '#28a745';
            }, 2000);
        }
    ''')

serve()