starter_app = """
```python
from fasthtml.common import *

app = FastHTML()
rt = app.route


@rt('/')
def get():
    return Div('Hello, World!')

serve()
```
"""
