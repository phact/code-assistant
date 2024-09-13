from fasthtml.common import *

app = FastHTML()
rt = app.route

@rt('/')
def get():
    return Html(
        Head(
            Title("Graphing Calculator"),
            Script(src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js"),
            Script(src="https://cdn.plot.ly/plotly-latest.min.js"),
            Style("""
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                input[type="text"] { width: 300px; }
            """)
        ),
        Body(
            H1("Graphing Calculator"),
            Form(
                Label("Enter a mathematical expression: ", For="expression"),
                Input(type="text", id="expression", name="expression", value="x^2"),
                Button("Graph", type="button", onclick="plotGraph()")
            ),
            Div(id="graph"),
            Script("""
                function plotGraph() {
                    const expression = document.getElementById('expression').value;
                    const xValues = [];
                    const yValues = [];

                    for (let x = -10; x <= 10; x += 0.1) {
                        xValues.push(x);
                        try {
                            const result = math.evaluate(expression, { x: x });
                            yValues.push(result);
                        } catch (error) {
                            console.error('Error evaluating expression:', error);
                            alert('Invalid expression. Please check and try again.');
                            return;
                        }
                    }

                    const data = [{
                        x: xValues,
                        y: yValues,
                        type: 'scatter',
                        mode: 'lines'
                    }];

                    const layout = {
                        title: 'Graph of ' + expression,
                        xaxis: { title: 'x' },
                        yaxis: { title: 'y' }
                    };

                    Plotly.newPlot('graph', data, layout);
                }
            """)
        )
    )

serve()