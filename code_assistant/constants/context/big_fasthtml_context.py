big_fasthtml_context = """
<project title="FastHTML" summary='FastHTML is a python library which brings together Starlette, Uvicorn, HTMX, and fastcore&#39;s `FT` "FastTags" into a library for creating server-rendered hypermedia applications. The `FastHTML` class itself inherits from `Starlette`, and adds decorator-based routing with many additions, Beforeware, automatic `FT` to HTML rendering, and much more. Although parts of its API are inspired by FastAPI, it is *not* compatible with FastAPI syntax and is not targeted at creating API services. FastHTML includes support for Pico CSS and the fastlite sqlite library, although using both are optional; sqlite can be used directly or via the fastsql library, and any CSS framework can be used. FastHTML is compatible with web components and any vanilla JS library, but not with React, Vue, or Svelte. Support for the Surreal and css-scope-inline libraries are also included, but both are optional.'>
  <docs>
    <doc title="FastHTML quick start" info="A brief overview of many FastHTML features"># Web Devs Quickstart



&lt;div&gt;

&gt; **Note**
&gt;
&gt; We’re going to be adding more to this document, so check back
&gt; frequently for updates.

&lt;/div&gt;

## Installation

``` bash
pip install python-fasthtml
```

## A Minimal Application

A minimal FastHTML application looks something like this:

&lt;div class=&quot;code-with-filename&quot;&gt;

**main.py**

``` python
from fasthtml.common import *

app, rt = fast_app()

@rt(&quot;/&quot;)
def get():
    return Titled(&quot;FastHTML&quot;, P(&quot;Let&#x27;s do this!&quot;))

serve()
```

&lt;/div&gt;

Line 1  
We import what we need for rapid development! A carefully-curated set of
FastHTML functions and other Python objects is brought into our global
namespace for convenience.

Line 3  
We instantiate a FastHTML app with the `fast_app()` utility function.
This provides a number of really useful defaults that we’ll take
advantage of later in the tutorial.

Line 5  
We use the `rt()` decorator to tell FastHTML what to return when a user
visits `/` in their browser.

Line 6  
We connect this route to HTTP GET requests by defining a view function
called `get()`.

Line 7  
A tree of Python function calls that return all the HTML required to
write a properly formed web page. You’ll soon see the power of this
approach.

Line 9  
The `serve()` utility configures and runs FastHTML using a library
called `uvicorn`.

Run the code:

``` bash
python main.py
```

The terminal will look like this:

``` bash
INFO:     Uvicorn running on http://0.0.0.0:5001 (Press CTRL+C to quit)
INFO:     Started reloader process [58058] using WatchFiles
INFO:     Started server process [58060]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Confirm FastHTML is running by opening your web browser to
[127.0.0.1:5001](http://127.0.0.1:5001). You should see something like
the image below:

![](quickstart-web-dev/quickstart-fasthtml.png)

&lt;div&gt;

&gt; **Note**
&gt;
&gt; While some linters and developers will complain about the wildcard
&gt; import, it is by design here and perfectly safe. FastHTML is very
&gt; deliberate about the objects it exports in `fasthtml.common`. If it
&gt; bothers you, you can import the objects you need individually, though
&gt; it will make the code more verbose and less readable.
&gt;
&gt; If you want to learn more about how FastHTML handles imports, we cover
&gt; that [here](https://docs.fastht.ml/explains/faq.html#why-use-import).

&lt;/div&gt;

## A Minimal Charting Application

The
[`Script`](https://AnswerDotAI.github.io/fasthtml/api/xtend.html#script)
function allows you to include JavaScript. You can use Python to
generate parts of your JS or JSON like this:

``` python
import json
from fasthtml.common import * 

app, rt = fast_app(hdrs=(Script(src=&quot;https://cdn.plot.ly/plotly-2.32.0.min.js&quot;),))

data = json.dumps({
    &quot;data&quot;: [{&quot;x&quot;: [1, 2, 3, 4],&quot;type&quot;: &quot;scatter&quot;},
            {&quot;x&quot;: [1, 2, 3, 4],&quot;y&quot;: [16, 5, 11, 9],&quot;type&quot;: &quot;scatter&quot;}],
    &quot;title&quot;: &quot;Plotly chart in FastHTML &quot;,
    &quot;description&quot;: &quot;This is a demo dashboard&quot;,
    &quot;type&quot;: &quot;scatter&quot;
})


@rt(&quot;/&quot;)
def get():
  return Titled(&quot;Chart Demo&quot;, Div(id=&quot;myDiv&quot;),
    Script(f&quot;var data = {data}; Plotly.newPlot(&#x27;myDiv&#x27;, data);&quot;))

serve()
```

## Debug Mode

When we can’t figure out a bug in FastHTML, we can run it in `DEBUG`
mode. When an error is thrown, the error screen is displayed in the
browser. This error setting should never be used in a deployed app.

``` python
from fasthtml.common import *

app, rt = fast_app(debug=True)

@rt(&quot;/&quot;)
def get():
    1/0
    return Titled(&quot;FastHTML Error!&quot;, P(&quot;Let&#x27;s error!&quot;))

serve()
```

Line 3  
`debug=True` sets debug mode on.

Line 7  
Python throws an error when it tries to divide an integer by zero.

## Routing

FastHTML builds upon FastAPI’s friendly decorator pattern for specifying
URLs, with extra features:

&lt;div class=&quot;code-with-filename&quot;&gt;

**main.py**

``` python
from fasthtml.common import * 

app, rt = fast_app()

@rt(&quot;/&quot;)
def get():
  return Titled(&quot;FastHTML&quot;, P(&quot;Let&#x27;s do this!&quot;))

@rt(&quot;/hello&quot;)
def get():
  return Titled(&quot;Hello, world!&quot;)

serve()
```

&lt;/div&gt;

Line 5  
The “/” URL on line 5 is the home of a project. This would be accessed
at [127.0.0.1:5001](http://127.0.0.1:5001).

Line 9  
“/hello” URL on line 9 will be found by the project if the user visits
[127.0.0.1:5001/hello](http://127.0.0.1:5001/hello).

&lt;div&gt;

&gt; **Tip**
&gt;
&gt; It looks like `get()` is being defined twice, but that’s not the case.
&gt; Each function decorated with `rt` is totally separate, and is injected
&gt; into the router. We’re not calling them in the module’s namespace
&gt; (`locals()`). Rather, we’re loading them into the routing mechanism
&gt; using the `rt` decorator.

&lt;/div&gt;

You can do more! Read on to learn what we can do to make parts of the
URL dynamic.

## Variables in URLs

You can add variable sections to a URL by marking them with
`{variable_name}`. Your function then receives the `{variable_name}` as
a keyword argument, but only if it is the correct type. Here’s an
example:

&lt;div class=&quot;code-with-filename&quot;&gt;

**main.py**

``` python
from fasthtml.common import * 

app, rt = fast_app()

@rt(&quot;/{name}/{age}&quot;)
def get(name: str, age: int):
  return Titled(f&quot;Hello {name.title()}, age {age}&quot;)

serve()
```

&lt;/div&gt;

Line 5  
We specify two variable names, `name` and `age`.

Line 6  
We define two function arguments named identically to the variables. You
will note that we specify the Python types to be passed.

Line 7  
We use these functions in our project.

Try it out by going to this address:
[127.0.0.1:5001/uma/5](http://127.0.0.1:5001/uma/5). You should get a
page that says,

&gt; “Hello Uma, age 5”.

### What happens if we enter incorrect data?

The [127.0.0.1:5001/uma/5](http://127.0.0.1:5001/uma/5) URL works
because `5` is an integer. If we enter something that is not, such as
[127.0.0.1:5001/uma/five](http://127.0.0.1:5001/uma/five), then FastHTML
will return an error instead of a web page.

&lt;div&gt;

&gt; **FastHTML URL routing supports more complex types**
&gt;
&gt; The two examples we provide here use Python’s built-in `str` and `int`
&gt; types, but you can use your own types, including more complex ones
&gt; such as those defined by libraries like
&gt; [attrs](https://pypi.org/project/attrs/),
&gt; [pydantic](https://pypi.org/project/pydantic/), and even
&gt; [sqlmodel](https://pypi.org/project/sqlmodel/).

&lt;/div&gt;

## HTTP Methods

FastHTML matches function names to HTTP methods. So far the URL routes
we’ve defined have been for HTTP GET methods, the most common method for
web pages.

Form submissions often are sent as HTTP POST. When dealing with more
dynamic web page designs, also known as Single Page Apps (SPA for
short), the need can arise for other methods such as HTTP PUT and HTTP
DELETE. The way FastHTML handles this is by changing the function name.

&lt;div class=&quot;code-with-filename&quot;&gt;

**main.py**

``` python
from fasthtml.common import * 

app, rt = fast_app()

@rt(&quot;/&quot;)  
def get():
  return Titled(&quot;HTTP GET&quot;, P(&quot;Handle GET&quot;))

@rt(&quot;/&quot;)  
def post():
  return Titled(&quot;HTTP POST&quot;, P(&quot;Handle POST&quot;))

serve()
```

&lt;/div&gt;

Line 6  
On line 6 because the `get()` function name is used, this will handle
HTTP GETs going to the `/` URI.

Line 10  
On line 10 because the `post()` function name is used, this will handle
HTTP POSTs going to the `/` URI.

## CSS Files and Inline Styles

Here we modify default headers to demonstrate how to use the [Sakura CSS
microframework](https://github.com/oxalorg/sakura) instead of FastHTML’s
default of Pico CSS.

&lt;div class=&quot;code-with-filename&quot;&gt;

**main.py**

``` python
from fasthtml.common import * 

app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel=&#x27;stylesheet&#x27;, href=&#x27;assets/normalize.min.css&#x27;, type=&#x27;text/css&#x27;),
        Link(rel=&#x27;stylesheet&#x27;, href=&#x27;assets/sakura.css&#x27;, type=&#x27;text/css&#x27;),
        Style(&quot;p {color: red;}&quot;)
))

@app.get(&quot;/&quot;)
def home():
    return Titled(&quot;FastHTML&quot;,
        P(&quot;Let&#x27;s do this!&quot;),
    )

serve()
```

&lt;/div&gt;

Line 4  
By setting `pico` to `False`, FastHTML will not include `pico.min.css`.

Line 7  
This will generate an HTML `&lt;link&gt;` tag for sourcing the css for Sakura.

Line 8  
If you want an inline styles, the `Style()` function will put the result
into the HTML.

## Other Static Media File Locations

As you saw,
[`Script`](https://AnswerDotAI.github.io/fasthtml/api/xtend.html#script)
and `Link` are specific to the most common static media use cases in web
apps: including JavaScript, CSS, and images. But it also works with
videos and other static media files. The default behavior is to look for
these files in the root directory - typically we don’t do anything
special to include them.

FastHTML also allows us to define a route that uses `FileResponse` to
serve the file at a specified path. This is useful for serving images,
videos, and other media files from a different directory without having
to change the paths of many files. So if we move the directory
containing the media files, we only need to change the path in one
place. In the example below, we call images from a directory called
`public`.

``` python
@rt(&quot;/{fname:path}.{ext:static}&quot;)
async def get(fname:str, ext:str): 
    return FileResponse(f&#x27;public/{fname}.{ext}&#x27;)
```

## Rendering Markdown

``` python
from fasthtml.common import *

hdrs = (MarkdownJS(), HighlightJS(langs=[&#x27;python&#x27;, &#x27;javascript&#x27;, &#x27;html&#x27;, &#x27;css&#x27;]), )

app, rt = fast_app(hdrs=hdrs)

content = &quot;&quot;&quot;
Here are some _markdown_ elements.

- This is a list item
- This is another list item
- And this is a third list item

**Fenced code blocks work here.**
&quot;&quot;&quot;

@rt(&#x27;/&#x27;)
def get(req):
    return Titled(&quot;Markdown rendering example&quot;, Div(content,cls=&quot;marked&quot;))

serve()
```

## Code highlighting

Here’s how to highlight code without any markdown configuration.

``` python
from fasthtml.common import *

# Add the HighlightJS built-in header
hdrs = (HighlightJS(langs=[&#x27;python&#x27;, &#x27;javascript&#x27;, &#x27;html&#x27;, &#x27;css&#x27;]),)

app, rt = fast_app(hdrs=hdrs)

code_example = &quot;&quot;&quot;
import datetime
import time

for i in range(10):
    print(f&quot;{datetime.datetime.now()}&quot;)
    time.sleep(1)
&quot;&quot;&quot;

@rt(&#x27;/&#x27;)
def get(req):
    return Titled(&quot;Markdown rendering example&quot;,
        Div(
            # The code example needs to be surrounded by
            # Pre &amp; Code elements
            Pre(Code(code_example))
    ))

serve()
```

## Defining new `ft` components

We can build our own `ft` components and combine them with other
components. The simplest method is defining them as a function.

``` python
def hero(title, statement):
    return Div(H1(title),P(statement), cls=&quot;hero&quot;)

# usage example
Main(
    hero(&quot;Hello World&quot;, &quot;This is a hero statement&quot;)
)
```

``` html
&lt;main&gt;
  &lt;div class=&quot;hero&quot;&gt;
    &lt;h1&gt;Hello World&lt;/h1&gt;
    &lt;p&gt;This is a hero statement&lt;/p&gt;
  &lt;/div&gt;
&lt;/main&gt;
```

### Pass through components

For when we need to define a new component that allows zero-to-many
components to be nested within them, we lean on Python’s `*args` and
`**kwargs` mechanism. Useful for creating page layout controls.

``` python
def layout(*args, **kwargs):
    &quot;&quot;&quot;Dashboard layout for all our dashboard views&quot;&quot;&quot;
    return Main(
        H1(&quot;Dashboard&quot;),
        Div(*args, **kwargs),
        cls=&quot;dashboard&quot;,
    )

# usage example
layout(
    Ul(*[Li(o) for o in range(3)]),
    P(&quot;Some content&quot;, cls=&quot;description&quot;),
)
```

``` html
&lt;main class=&quot;dashboard&quot;&gt;
  &lt;h1&gt;Dashboard&lt;/h1&gt;
  &lt;div&gt;
    &lt;ul&gt;
      &lt;li&gt;0&lt;/li&gt;
      &lt;li&gt;1&lt;/li&gt;
      &lt;li&gt;2&lt;/li&gt;
    &lt;/ul&gt;
    &lt;p class=&quot;description&quot;&gt;Some content&lt;/p&gt;
  &lt;/div&gt;
&lt;/main&gt;
```

### Dataclasses as ft components

While functions are easy to read, for more complex components some might
find it easier to use a dataclass.

``` python
from dataclasses import dataclass

@dataclass
class Hero:
    title: str
    statement: str
    
    def __ft__(self):
        &quot;&quot;&quot; The __ft__ method renders the dataclass at runtime.&quot;&quot;&quot;
        return Div(H1(self.title),P(self.statement), cls=&quot;hero&quot;)
    
# usage example
Main(
    Hero(&quot;Hello World&quot;, &quot;This is a hero statement&quot;)
)
```

``` html
&lt;main&gt;
  &lt;div class=&quot;hero&quot;&gt;
    &lt;h1&gt;Hello World&lt;/h1&gt;
    &lt;p&gt;This is a hero statement&lt;/p&gt;
  &lt;/div&gt;
&lt;/main&gt;
```

## Testing views in notebooks

Because of the ASGI event loop it is currently impossible to run
FastHTML inside a notebook. However, we can still test the output of our
views. To do this, we leverage Starlette, an ASGI toolkit that FastHTML
uses.

``` python
# First we instantiate our app, in this case we remove the
# default headers to reduce the size of the output.
app, rt = fast_app(default_hdrs=False)

# Setting up the Starlette test client
from starlette.testclient import TestClient
client = TestClient(app)

# Usage example
@rt(&quot;/&quot;)
def get():
    return Titled(&quot;FastHTML is awesome&quot;, 
        P(&quot;The fastest way to create web apps in Python&quot;))

print(client.get(&quot;/&quot;).text)
```

    &lt;!doctype html&gt;

    &lt;html&gt;
      &lt;head&gt;
        &lt;title&gt;FastHTML is awesome&lt;/title&gt;
      &lt;/head&gt;
      &lt;body&gt;
    &lt;main class=&quot;container&quot;&gt;
      &lt;h1&gt;FastHTML is awesome&lt;/h1&gt;
      &lt;p&gt;The fastest way to create web apps in Python&lt;/p&gt;
    &lt;/main&gt;
      &lt;/body&gt;
    &lt;/html&gt;

## Strings and conversion order

The general rules for rendering are: - `__ft__` method will be called
(for default components like `P`, `H2`, etc. or if you define your own
components) - If you pass a string, it will be escaped - On other python
objects, `str()` will be called

As a consequence, if you want to include plain HTML tags directly into
e.g. a `Div()` they will get escaped by default (as a security measure
to avoid code injections). This can be avoided by using `NotStr()`, a
convenient way to reuse python code that returns already HTML. If you
use pandas, you can use `pandas.DataFrame.to_html()` to get a nice
table. To include the output a FastHTML, wrap it in `NotStr()`, like
`Div(NotStr(df.to_html()))`.

Above we saw how a dataclass behaves with the `__ft__` method defined.
On a plain dataclass, `str()` will be called (but not escaped).

``` python
from dataclasses import dataclass

@dataclass
class Hero:
    title: str
    statement: str
        
# rendering the dataclass with the default method
Main(
    Hero(&quot;&lt;h1&gt;Hello World&lt;/h1&gt;&quot;, &quot;This is a hero statement&quot;)
)
```

``` html
&lt;main&gt;Hero(title=&#x27;&lt;h1&gt;Hello World&lt;/h1&gt;&#x27;, statement=&#x27;This is a hero statement&#x27;)&lt;/main&gt;
```

``` python
# This will display the HTML as text on your page
Div(&quot;Let&#x27;s include some HTML here: &lt;div&gt;Some HTML&lt;/div&gt;&quot;)
```

``` html
&lt;div&gt;Let&amp;#x27;s include some HTML here: &amp;lt;div&amp;gt;Some HTML&amp;lt;/div&amp;gt;&lt;/div&gt;
```

``` python
# Keep the string untouched, will be rendered on the page
Div(NotStr(&quot;&lt;div&gt;&lt;h1&gt;Some HTML&lt;/h1&gt;&lt;/div&gt;&quot;))
```

``` html
&lt;div&gt;&lt;div&gt;&lt;h1&gt;Some HTML&lt;/h1&gt;&lt;/div&gt;&lt;/div&gt;
```

## Custom exception handlers

FastHTML allows customization of exception handlers, but does so
gracefully. What this means is by default it includes all the `&lt;html&gt;`
tags needed to display attractive content. Try it out!

``` python
from fasthtml.common import *

def not_found(req, exc): return Titled(&quot;404: I don&#x27;t exist!&quot;)

exception_handlers = {404: not_found}

app, rt = fast_app(exception_handlers=exception_handlers)

@rt(&#x27;/&#x27;)
def get():
    return (Titled(&quot;Home page&quot;, P(A(href=&quot;/oops&quot;)(&quot;Click to generate 404 error&quot;))))

serve()
```

We can also use lambda to make things more terse:

``` python
from fasthtml.common import *

exception_handlers={
    404: lambda req, exc: Titled(&quot;404: I don&#x27;t exist!&quot;),
    418: lambda req, exc: Titled(&quot;418: I&#x27;m a teapot!&quot;)
}

app, rt = fast_app(exception_handlers=exception_handlers)

@rt(&#x27;/&#x27;)
def get():
    return (Titled(&quot;Home page&quot;, P(A(href=&quot;/oops&quot;)(&quot;Click to generate 404 error&quot;))))

serve()
```

## Cookies

We can set cookies using the `cookie()` function. In our example, we’ll
create a `timestamp` cookie.

``` python
from datetime import datetime
from IPython.display import HTML
```

``` python
@rt(&quot;/settimestamp&quot;)
def get(req):
    now = datetime.now()
    return P(f&#x27;Set to {now}&#x27;), cookie(&#x27;now&#x27;, datetime.now())

HTML(client.get(&#x27;/settimestamp&#x27;).text)
```

&lt;!doctype html&gt;
&amp;#10;&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;FastHTML page&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
Set to 2024-08-07 09:07:47.535449
  &lt;/body&gt;
&lt;/html&gt;

Now let’s get it back using the same name for our parameter as the
cookie name.

``` python
@rt(&#x27;/gettimestamp&#x27;)
def get(now:date): return f&#x27;Cookie was set at time {now.time()}&#x27;

client.get(&#x27;/gettimestamp&#x27;).text
```

    &#x27;Cookie was set at time 09:07:47.535456&#x27;

## Sessions

For convenience and security, FastHTML has a mechanism for storing small
amounts of data in the user’s browser. We can do this by adding a
`session` argument to routes. FastHTML sessions are Python dictionaries,
and we can leverage to our benefit. The example below shows how to
concisely set and get sessions.

``` python
@rt(&#x27;/adder/{num}&#x27;)
def get(session, num: int):
    session.setdefault(&#x27;sum&#x27;, 0)
    session[&#x27;sum&#x27;] = session.get(&#x27;sum&#x27;) + num
    return Response(f&#x27;The sum is {session[&quot;sum&quot;]}.&#x27;)
```

## Toasts (also known as Messages)

Toasts, sometimes called “Messages” are small notifications usually in
colored boxes used to notify users that something has happened. Toasts
can be of four types:

- info
- success
- warning
- error

Examples toasts might include:

- “Payment accepted”
- “Data submitted”
- “Request approved”

Toasts require the use of the `setup_toasts()` function plus every view
needs these two features:

- The session argument
- Must return FT components

``` python
setup_toasts(app)

@rt(&#x27;/toasting&#x27;)
def get(session):
    # Normally one toast is enough, this allows us to see
    # different toast types in action.
    add_toast(session, f&quot;Toast is being cooked&quot;, &quot;info&quot;)
    add_toast(session, f&quot;Toast is ready&quot;, &quot;success&quot;)
    add_toast(session, f&quot;Toast is getting a bit crispy&quot;, &quot;warning&quot;)
    add_toast(session, f&quot;Toast is burning!&quot;, &quot;error&quot;)
    return Titled(&quot;I like toast&quot;)
```

Line 1  
`setup_toasts` is a helper function that adds toast dependencies.
Usually this would be declared right after `fast_app()`

Line 4  
Toasts require sessions

Line 11  
Views with Toasts must return FT components.

## Authentication and authorization

In FastHTML the tasks of authentication and authorization are handled
with Beforeware. Beforeware are functions that run before the route
handler is called. They are useful for global tasks like ensuring users
are authenticated or have permissions to access a view.

First, we write a function that accepts a request and session arguments:

``` python
# Status code 303 is a redirect that can change POST to GET,
# so it&#x27;s appropriate for a login page.
login_redir = RedirectResponse(&#x27;/login&#x27;, status_code=303)

def user_auth_before(req, sess):
    # The `auth` key in the request scope is automatically provided
    # to any handler which requests it, and can not be injected
    # by the user using query params, cookies, etc, so it should
    # be secure to use.    
    auth = req.scope[&#x27;auth&#x27;] = sess.get(&#x27;auth&#x27;, None)
    # If the session key is not there, it redirects to the login page.
    if not auth: return login_redir
```

Now we pass our `user_auth_before` function as the first argument into a
[`Beforeware`](https://AnswerDotAI.github.io/fasthtml/api/core.html#beforeware)
class. We also pass a list of regular expressions to the `skip`
argument, designed to allow users to still get to the home and login
pages.

``` python
beforeware = Beforeware(
    user_auth_before,
    skip=[r&#x27;/favicon\.ico&#x27;, r&#x27;/static/.*&#x27;, r&#x27;.*\.css&#x27;, r&#x27;.*\.js&#x27;, &#x27;/login&#x27;, &#x27;/&#x27;]
)

app, rt = fast_app(before=beforeware)
```

## Unwritten quickstart sections

- Forms
- Websockets
- Tables</doc>
    <doc title="Surreal" info="Tiny jQuery alternative for plain Javascript with inline Locality of Behavior, providing `me` and `any` functions"># 🗿 Surreal
### Tiny jQuery alternative for plain Javascript with inline [Locality of Behavior](https://htmx.org/essays/locality-of-behaviour/)!

![cover](https://user-images.githubusercontent.com/24665/171092805-b41286b2-be4a-4aab-9ee6-d604699cc507.png)
(Art by [shahabalizadeh](https://www.deviantart.com/shahabalizadeh))
&lt;!--
&lt;a href=&quot;https://github.com/gnat/surreal/archive/refs/heads/main.zip&quot;&gt;&lt;img src=&quot;https://img.shields.io/badge/Download%20.zip-ff9800?style=for-the-badge&amp;color=%234400e5&quot; alt=&quot;Download badge&quot; /&gt;&lt;/a&gt;

&lt;a href=&quot;https://github.com/gnat/surreal&quot;&gt;&lt;img src=&quot;https://img.shields.io/github/workflow/status/gnat/surreal/ci?label=ci&amp;style=for-the-badge&amp;color=%237d91ce&quot; alt=&quot;CI build badge&quot; /&gt;&lt;/a&gt;
&lt;a href=&quot;https://github.com/gnat/surreal/releases&quot;&gt;&lt;img src=&quot;https://img.shields.io/github/workflow/status/gnat/surreal/release?label=Mini&amp;style=for-the-badge&amp;color=%237d91ce&quot; alt=&quot;Mini build badge&quot; /&gt;&lt;/a&gt;
&lt;a href=&quot;https://github.com/gnat/surreal/blob/main/LICENSE&quot;&gt;&lt;img src=&quot;https://img.shields.io/github/license/gnat/surreal?style=for-the-badge&amp;color=%234400e5&quot; alt=&quot;License badge&quot; /&gt;&lt;/a&gt;--&gt;

## Why does this exist?

For devs who love ergonomics! You may appreciate Surreal if:

* You want to stay as close as possible to Vanilla JS.
* Hate typing `document.querySelector` over.. and over..
* Hate typing `addEventListener` over.. and over..
* Really wish `document.querySelectorAll` had Array functions..
* Really wish `this` would work in any inline `&lt;script&gt;` tag
* Enjoyed using jQuery selector syntax.
* [Animations, timelines, tweens](#-quick-start) with no extra libraries.
* Only 320 lines. No build step. No dependencies.
* Pairs well with [htmx](https://htmx.org)
* Want fewer layers, less complexity. Are aware of the cargo cult. ✈️

## ✨ What does it add to Javascript?

* ⚡️ [Locality of Behavior (LoB)](https://htmx.org/essays/locality-of-behaviour/) Use `me()` inside `&lt;script&gt;`
  * No **.class** or **#id** needed! Get an element without creating a unique name.
  * `this` but much more flexible!
  * Want `me` in your CSS `&lt;style&gt;` tags, too? See our [companion script](https://github.com/gnat/css-scope-inline)
* 🔗 Call chaining, jQuery style.
* ♻️ Functions work seamlessly on 1 element or arrays of elements!
  * All functions can use: `me()`, `any()`, `NodeList`, `HTMLElement` (..or arrays of these!)
  * Get 1 element: `me()`
  * ..or many elements: `any()`
  * `me()` or `any()` can chain with any Surreal function.
    * `me()` can be used directly as a single element (like `querySelector()` or `$()`)
    * `any()` can use: `for` / `forEach` / `filter` / `map` (like `querySelectorAll()` or `$()`)
* 🌗 No forced style. Use: `classAdd` or `class_add` or `addClass` or `add_class`
  * Use `camelCase` (Javascript) or `snake_case` (Python, Rust, PHP, Ruby, SQL, CSS).

### 🤔 Why use `me()` / `any()` instead of `$()`
* 💡 Solves the classic jQuery bloat problem: Am I getting 1 element or an array of elements?
  * `me()` is guaranteed to return 1 element (or first found, or null).
  * `any()` is guaranteed to return an array (or empty array).
  * No more checks = write less code. Bonus: Reads more like self-documenting english.

## 👁️ How does it look?

Do surreal things with [Locality of Behavior](https://htmx.org/essays/locality-of-behaviour/) like:
```html
&lt;label for=&quot;file-input&quot; &gt;
  &lt;div class=&quot;uploader&quot;&gt;&lt;/div&gt;
  &lt;script&gt;
    me().on(&quot;dragover&quot;, ev =&gt; { halt(ev); me(ev).classAdd(&#x27;.hover&#x27;); console.log(&quot;Files in drop zone.&quot;) })
    me().on(&quot;dragleave&quot;, ev =&gt; { halt(ev); me(ev).classRemove(&#x27;.hover&#x27;); console.log(&quot;Files left drop zone.&quot;) })
    me().on(&quot;drop&quot;, ev =&gt; { halt(ev); me(ev).classRemove(&#x27;.hover&#x27;).classAdd(&#x27;.loading&#x27;); me(&#x27;#file-input&#x27;).attribute(&#x27;files&#x27;, ev.dataTransfer.files); me(&#x27;#form&#x27;).send(&#x27;change&#x27;) })
  &lt;/script&gt;
&lt;/label&gt;
```

See the [Live Example](https://gnat.github.io/surreal/example.html)! Then [view source](https://github.com/gnat/surreal/blob/main/example.html).

## 🎁 Install

Surreal is only 320 lines. No build step. No dependencies.

[📥 Download](https://raw.githubusercontent.com/gnat/surreal/main/surreal.js) into your project, and add `&lt;script src=&quot;/surreal.js&quot;&gt;&lt;/script&gt;` in your `&lt;head&gt;`

Or, 🌐 via CDN: `&lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/surreal/1.3.2/surreal.js&quot;&gt;&lt;/script&gt;`

## ⚡ Usage

### &lt;a name=&quot;selectors&quot;&gt;&lt;/a&gt;🔍️ DOM Selection

* Select **one** element: `me(...)`
  * Can be any of:
    * CSS selector: `&quot;.button&quot;`, `&quot;#header&quot;`, `&quot;h1&quot;`, `&quot;body &gt; .block&quot;`
    * Variables: `body`, `e`, `some_element`
    * Events: `event.currentTarget` will be used.
    * Surreal selectors: `me()`,`any()`
    * Choose the start location in the DOM with the 2nd arg. (Default: `document`)
      * 🔥 `any(&#x27;button&#x27;, me(&#x27;#header&#x27;)).classAdd(&#x27;red&#x27;)`
        * Add `.red` to any `&lt;button&gt;` inside of `#header`
  * `me()` ⭐ Get parent element of `&lt;script&gt;` without a **.class** or **#id** !
  * `me(&quot;body&quot;)` Gets `&lt;body&gt;`
  * `me(&quot;.button&quot;)` Gets the first `&lt;div class=&quot;button&quot;&gt;...&lt;/div&gt;`. To get all of them use `any()`
* Select **one or more** elements as an array: `any(...)`
  * Like `me()` but guaranteed to return an array (or empty array). 
  * `any(&quot;.foo&quot;)` ⭐ Get all matching elements.
  * Convert between arrays of elements and single elements: `any(me())`, `me(any(&quot;.something&quot;))`
 
### 🔥 DOM Functions

* ♻️ All functions work on single elements or arrays of elements.
* 🔗 Start a chain using `me()` and `any()`
  * 🟢 Style A `me().classAdd(&#x27;red&#x27;)` ⭐ Chain style. Recommended!
  * 🟠 Style B: `classAdd(me(), &#x27;red&#x27;)`
* 🌐 Global conveniences help you write less code.
  * `globalsAdd()` will automatically warn you of any clobbering issues!
  * 💀🩸 If you want no conveniences, or are a masochist, delete `globalsAdd()`
    * 🟢 `me().classAdd(&#x27;red&#x27;)` becomes `surreal.me().classAdd(&#x27;red&#x27;)`
    * 🟠 `classAdd(me(), &#x27;red&#x27;)` becomes `surreal.classAdd(surreal.me(), &#x27;red&#x27;)`

See: [Quick Start](#quick-start) and [Reference](#reference) and [No Surreal Needed](#no-surreal)

## &lt;a name=&quot;quick-start&quot;&gt;&lt;/a&gt;⚡ Quick Start

* Add a class
  * `me().classAdd(&#x27;red&#x27;)`
  * `any(&quot;button&quot;).classAdd(&#x27;red&#x27;)`
* Events
  * `me().on(&quot;click&quot;, ev =&gt; me(ev).fadeOut() )`
  * `any(&#x27;button&#x27;).on(&#x27;click&#x27;, ev =&gt; { me(ev).styles(&#x27;color: red&#x27;) })`
* Run functions over elements.
  * `any(&#x27;button&#x27;).run(_ =&gt; { alert(_) })`
* Styles / CSS
  * `me().styles(&#x27;color: red&#x27;)`
  * `me().styles({ &#x27;color&#x27;:&#x27;red&#x27;, &#x27;background&#x27;:&#x27;blue&#x27; })`
* Attributes
  * `me().attribute(&#x27;active&#x27;, true)`

&lt;a name=&quot;timelines&quot;&gt;&lt;/a&gt;
#### Timeline animations without any libraries.
```html
&lt;div&gt;I change color every second.
  &lt;script&gt;
    // On click, animate something new every second.
    me().on(&quot;click&quot;, async ev =&gt; {
      let el = me(ev) // Save target because async will lose it.
      me(el).styles({ &quot;transition&quot;: &quot;background 1s&quot; })
      await sleep(1000)
      me(el).styles({ &quot;background&quot;: &quot;red&quot; })
      await sleep(1000)
      me(el).styles({ &quot;background&quot;: &quot;green&quot; })
      await sleep(1000)
      me(el).styles({ &quot;background&quot;: &quot;blue&quot; })
      await sleep(1000)
      me(el).styles({ &quot;background&quot;: &quot;none&quot; })
      await sleep(1000)
      me(el).remove()
    })
  &lt;/script&gt;
&lt;/div&gt;
```
```html
&lt;div&gt;I fade out and remove myself.
  &lt;script&gt;me().on(&quot;click&quot;, ev =&gt; { me(ev).fadeOut() })&lt;/script&gt;
&lt;/div&gt;
```
```html
&lt;div&gt;Change color every second.
  &lt;script&gt;
    // Run immediately.
    (async (e = me()) =&gt; {
      me(e).styles({ &quot;transition&quot;: &quot;background 1s&quot; })
      await sleep(1000)
      me(e).styles({ &quot;background&quot;: &quot;red&quot; })
      await sleep(1000)
      me(e).styles({ &quot;background&quot;: &quot;green&quot; })
      await sleep(1000)
      me(e).styles({ &quot;background&quot;: &quot;blue&quot; })
      await sleep(1000)
      me(e).styles({ &quot;background&quot;: &quot;none&quot; })
      await sleep(1000)
      me(e).remove()
    })()
  &lt;/script&gt;
&lt;/div&gt;
```
```html
&lt;script&gt;
  // Run immediately, for every &lt;button&gt; globally!
  (async () =&gt; {
    any(&quot;button&quot;).fadeOut()
  })()
&lt;/script&gt;
```
#### Array methods
```js
any(&#x27;button&#x27;)?.forEach(...)
any(&#x27;button&#x27;)?.map(...)
```

## &lt;a name=&quot;reference&quot;&gt;&lt;/a&gt;👁️ Functions
Looking for [DOM Selectors](#selectors)?
Looking for stuff [we recommend doing in vanilla JS](#no-surreal)?
### 🧭 Legend
* 🔗 Chainable off `me()` and `any()`
* 🌐 Global shortcut.
* 🔥 Runnable example.
* 🔌 Built-in Plugin
### 👁️ At a glance

* 🔗 `run`
  * It&#x27;s `forEach` but less wordy and works on single elements, too!
  * 🔥 `me().run(e =&gt; { alert(e) })`
  * 🔥 `any(&#x27;button&#x27;).run(e =&gt; { alert(e) })`
* 🔗 `remove`
  * 🔥 `me().remove()`
  * 🔥 `any(&#x27;button&#x27;).remove()`
* 🔗 `classAdd` 🌗 `class_add` 🌗 `addClass` 🌗 `add_class`
  * 🔥 `me().classAdd(&#x27;active&#x27;)`
  * Leading `.` is **optional**
    * Same thing: `me().classAdd(&#x27;active&#x27;)` 🌗 `me().classAdd(&#x27;.active&#x27;)`
* 🔗 `classRemove` 🌗 `class_remove` 🌗 `removeClass` 🌗 `remove_class`
  * 🔥 `me().classRemove(&#x27;active&#x27;)`
* 🔗 `classToggle` 🌗 `class_toggle` 🌗 `toggleClass` 🌗 `toggle_class`
  * 🔥 `me().classToggle(&#x27;active&#x27;)`
* 🔗 `styles`
  * 🔥 `me().styles(&#x27;color: red&#x27;)` Add style.
  * 🔥 `me().styles({ &#x27;color&#x27;:&#x27;red&#x27;, &#x27;background&#x27;:&#x27;blue&#x27; })` Add multiple styles.
  * 🔥 `me().styles({ &#x27;background&#x27;:null })` Remove style.
* 🔗 `attribute` 🌗 `attributes` 🌗 `attr`
  * Get: 🔥 `me().attribute(&#x27;data-x&#x27;)`
    * For single elements.
    * For many elements, wrap it in: `any(...).run(...)` or `any(...).forEach(...)`
  * Set: 🔥`me().attribute(&#x27;data-x&#x27;, true)`
  * Set multiple: 🔥 `me().attribute({ &#x27;data-x&#x27;:&#x27;yes&#x27;, &#x27;data-y&#x27;:&#x27;no&#x27; })`
  * Remove: 🔥 `me().attribute(&#x27;data-x&#x27;, null)`
  * Remove multiple: 🔥 `me().attribute({ &#x27;data-x&#x27;: null, &#x27;data-y&#x27;:null })`
* 🔗 `send` 🌗 `trigger`
  * 🔥 `me().send(&#x27;change&#x27;)`
  * 🔥 `me().send(&#x27;change&#x27;, {&#x27;data&#x27;:&#x27;thing&#x27;})`
  * Wraps `dispatchEvent`
* 🔗 `on`
  * 🔥 `me().on(&#x27;click&#x27;, ev =&gt; { me(ev).styles(&#x27;background&#x27;, &#x27;red&#x27;) })`
  * Wraps `addEventListener`
* 🔗 `off`
  * 🔥 `me().off(&#x27;click&#x27;, fn)`
  * Wraps `removeEventListener`
* 🔗 `offAll`
  * 🔥 `me().offAll()`
* 🔗 `disable`
  * 🔥 `me().disable()`
  * Easy alternative to `off()`. Disables click, key, submit events.
* 🔗 `enable`
  * 🔥 `me().enable()`
  * Opposite of `disable()`
* 🌐 `sleep`
  * 🔥 `await sleep(1000, ev =&gt; { alert(ev) })`
  * `async` version of `setTimeout`
  * Wonderful for animation timelines.
* 🌐 `tick`
  * 🔥 `await tick()`
  * `await` version of `rAF` / `requestAnimationFrame`.
  * Animation tick. Waits 1 frame.
  * Great if you need to wait for events to propagate.
* 🌐 `rAF`
  * 🔥 `rAF(e =&gt; { return e })`
  * Animation tick.  Fires when 1 frame has passed. Alias of [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame)
  * Great if you need to wait for events to propagate.
* 🌐 `rIC`
  * 🔥 `rIC(e =&gt; { return e })`
  * Great time to compute. Fires function when JS is idle. Alias of [requestIdleCallback](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback)
* 🌐 `halt`
  * 🔥 `halt(event)`
  * Prevent default browser behaviors.
  * Wrapper for [preventDefault](https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault)
* 🌐 `createElement` 🌗 `create_element`
  * 🔥 `e_new = createElement(&quot;div&quot;); me().prepend(e_new)`
  * Alias of vanilla `document.createElement`
* 🌐 `onloadAdd` 🌗 `onload_add` 🌗 `addOnload` 🌗 `add_onload`
  * 🔥 `onloadAdd(_ =&gt; { alert(&quot;loaded!&quot;); })`
  * 🔥 `&lt;script&gt;let e = me(); onloadAdd(_ =&gt; { me(e).on(&quot;click&quot;, ev =&gt; { alert(&quot;clicked&quot;) }) })&lt;/script&gt;`
  * Execute after the DOM is ready. Similar to jquery `ready()`
  * Add to `window.onload` while preventing overwrites of `window.onload` and predictable loading!
  * Alternatives:
    * Skip missing elements using `?.` example: `me(&quot;video&quot;)?.requestFullscreen()`
    * Place `&lt;script&gt;` after the loaded element.
      * See `me(&#x27;-&#x27;)` / `me(&#x27;prev&#x27;)`
* 🔌 `fadeOut`
  * See below
* 🔌 `fadeIn`
  * See below

### &lt;a name=&quot;plugin-included&quot;&gt;&lt;/a&gt;🔌 Built-in Plugins

### Effects
Build effects with `me().styles({...})` with timelines using [CSS transitioned `await` or callbacks](#timelines).

Common effects included:

* 🔗 `fadeOut` 🌗 `fade_out`
  * Fade out and remove element.
  * Keep element with `remove=false`.
  * 🔥 `me().fadeOut()`
  * 🔥 `me().fadeOut(ev =&gt; { alert(&quot;Faded out!&quot;) }, 3000)` Over 3 seconds then call function.

* 🔗 `fadeIn` 🌗 `fade_in`
  * Fade in existing element which has `opacity: 0`
  * 🔥 `me().fadeIn()`
  * 🔥 `me().fadeIn(ev =&gt; { alert(&quot;Faded in!&quot;) }, 3000)` Over 3 seconds then call function.


## &lt;a name=&quot;no-surreal&quot;&gt;&lt;/a&gt;⚪ No Surreal Needed

More often than not, Vanilla JS is the easiest way!

Logging
* 🔥 `console.log()` `console.warn()` `console.error()`
* Event logging: 🔥 `monitorEvents(me())` See: [Chrome Blog](https://developer.chrome.com/blog/quickly-monitor-events-from-the-console-panel-2/)

Benchmarking / Time It!
* 🔥 `console.time(&#x27;name&#x27;)`
* 🔥 `console.timeEnd(&#x27;name&#x27;)`

Text / HTML Content
* 🔥 `me().textContent = &quot;hello world&quot;`
  * XSS Safe! See: [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)
* 🔥 `me().innerHTML = &quot;&lt;p&gt;hello world&lt;/p&gt;&quot;`
* 🔥 `me().innerText = &quot;hello world&quot;`

Children
* 🔥 `me().children`
* 🔥 `me().children.hidden = true`

Append / Prepend elements.
* 🔥 `me().prepend(new_element)`
* 🔥 `me().appendChild(new_element)`
* 🔥 `me().insertBefore(element, other_element.firstChild)`
* 🔥 `me().insertAdjacentHTML(&quot;beforebegin&quot;, new_element)`

AJAX (replace jQuery `ajax()`)
* Use [htmx](https://htmx.org/) or [htmz](https://leanrada.com/htmz/) or [fetch()](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) or [XMLHttpRequest()](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) directly.
* Using `fetch()`
```js
me().on(&quot;click&quot;, async event =&gt; {
  let e = me(event)
  // EXAMPLE 1: Hit an endpoint.
  if((await fetch(&quot;/webhook&quot;)).ok) console.log(&quot;Did the thing.&quot;)
  // EXAMPLE 2: Get content and replace me()
  try {
    let response = await fetch(&#x27;/endpoint&#x27;)
    if (response.ok) e.innerHTML = await response.text()
    else console.warn(&#x27;fetch(): Bad response&#x27;)
  }
  catch (error) { console.warn(`fetch(): ${error}`) }
})
```
* Using `XMLHttpRequest()`
```js
me().on(&quot;click&quot;, async event =&gt; {
  let e = me(event)
  // EXAMPLE 1: Hit an endpoint.
  var xhr = new XMLHttpRequest()
  xhr.open(&quot;GET&quot;, &quot;/webhook&quot;)
  xhr.send()
  // EXAMPLE 2: Get content and replace me()
  var xhr = new XMLHttpRequest()
  xhr.open(&quot;GET&quot;, &quot;/endpoint&quot;)
  xhr.onreadystatechange = () =&gt; {
    if (xhr.readyState == 4 &amp;&amp; xhr.status &gt;= 200 &amp;&amp; xhr.status &lt; 300) e.innerHTML = xhr.responseText
  }
  xhr.send()
})
```

 ## 💎 Conventions &amp; Tips

* Many ideas can be done in HTML / CSS (ex: dropdowns)
* `_` = for temporary or unused variables. Keep it short and sweet!
* `e`, `el`, `elt` = element
* `e`, `ev`, `evt` = event
* `f`, `fn` = function

#### Scope functions inside `&lt;script&gt;`
  * ⭐ On `me()`
    *  `me().hey = (text) =&gt; { alert(text) }`
    *  `me().on(&#x27;click&#x27;, (ev) =&gt; { me(ev).hey(&quot;hi&quot;) })`
  * ⭐ Use a block: `{ function hey(text) { alert(text) }; me().on(&#x27;click&#x27;, ev =&gt; { hey(&quot;hi&quot;) }) }`
  * ⭐ Use an event: `me().on(&#x27;click&#x27;, ev =&gt; { /* add and call function here */ })`
  * Use an inline module: `&lt;script type=&quot;module&quot;&gt;`
    * Note: `me()` will no longer see `parentElement` so explicit selectors are required: `me(&quot;.mybutton&quot;)`

#### Select a void element like `&lt;input type=&quot;text&quot; /&gt;`
* Use: `me(&#x27;-&#x27;)` or `me(&#x27;prev&#x27;)` or `me(&#x27;previous&#x27;)`
  * 🔥 `&lt;input type=&quot;text&quot; /&gt; &lt;script&gt;me(&#x27;-&#x27;).value = &quot;hello&quot;&lt;/script&gt;`
  * Inspired by the CSS &quot;next sibling&quot; combinator `+` but in reverse `-`
* Or, use a relative start.
  * 🔥 `&lt;form&gt; &lt;input type=&quot;text&quot; n1 /&gt; &lt;script&gt;me(&#x27;[n1]&#x27;, me()).value = &quot;hello&quot;&lt;/script&gt; &lt;/form&gt;`

#### Ignore call chain when element is missing.
* 🔥 `me(&quot;#i_dont_exist&quot;)?.classAdd(&#x27;active&#x27;)`
* No warnings: 🔥 `me(&quot;#i_dont_exist&quot;, document, false)?.classAdd(&#x27;active&#x27;)`

## &lt;a name=&quot;plugins&quot;&gt;&lt;/a&gt;🔌 Your own plugin

Feel free to edit Surreal directly- but if you prefer, you can use plugins to effortlessly merge with new versions.

```javascript
function pluginHello(e) {
  function hello(e, name=&quot;World&quot;) {
    console.log(`Hello ${name} from ${e}`)
    return e // Make chainable.
  }
  // Add sugar
  e.hello = (name) =&gt; { return hello(e, name) }
}

surreal.plugins.push(pluginHello)
```

Now use your function like: `me().hello(&quot;Internet&quot;)`

* See the included `pluginEffects` for a more comprehensive example.
* Your functions are added globally by `globalsAdd()` If you do not want this, add it to the `restricted` list.
* Refer to an existing function to see how to make yours work with 1 or many elements.

Make an [issue](https://github.com/gnat/surreal/issues) or [pull request](https://github.com/gnat/surreal/pulls) if you think people would like to use it! If it&#x27;s useful enough we&#x27;ll want it in core.

### ⭐ Awesome Surreal examples, plugins, and resources: [awesome-surreal](https://github.com/gnat/awesome-surreal) !

## 📚️ Inspired by

* [jQuery](https://jquery.com/) for the chainable syntax we all love.
* [BlingBling.js](https://github.com/argyleink/blingblingjs) for modern minimalism.
* [Bliss.js](https://blissfuljs.com/) for a focus on single elements and extensibility.
* [Hyperscript](https://hyperscript.org) for Locality of Behavior and awesome ergonomics.
* Shout out to [Umbrella](https://umbrellajs.com/), [Cash](https://github.com/fabiospampinato/cash), [Zepto](https://zeptojs.com/)- Not quite as ergonomic. Requires build step to extend.

## 🌘 Future
* Always more `example.html` goodies!
* Automated browser testing perhaps with:
  * [Fava](https://github.com/fabiospampinato/fava). See: https://github.com/avajs/ava/issues/24#issuecomment-885949036
  * [Ava](https://github.com/avajs/ava/blob/main/docs/recipes/browser-testing.md)
  * [jsdom](https://github.com/jsdom/jsdom)
    * [jsdom notes](https://github.com/jsdom/jsdom#executing-scripts)</doc>
    <doc title="CSS Scope Inline" info="A JS library which allow `me` to be used in CSS selectors, by using a `MutationObserver` to monitor the DOM"># 🌘 CSS Scope Inline

![cover](https://github.com/gnat/css-scope-inline/assets/24665/c4935c1b-34e3-4220-9d42-11f064999a57)
(Art by [shahabalizadeh](https://www.artstation.com/artwork/zDgdd))

## Why does this exist?

* You want an easy inline vanilla CSS experience without Tailwind CSS.
* Hate creating unique class names over.. and over.. to use once.
* You want to co-locate your styles for ⚡️ [Locality of Behavior (LoB)](https://htmx.org/essays/locality-of-behaviour/)
* You wish `this` would work in `&lt;style&gt;` tags.
* Want all CSS features: [Nesting](https://caniuse.com/css-nesting), animations. Get scoped [`@keyframes`](https://github.com/gnat/css-scope-inline/blob/main/example.html#L86)!
* You wish `@media` queries were shorter for [responsive design](https://tailwindcss.com/docs/responsive-design).
* Only 16 lines. No build step. No dependencies.
* Pairs well with [htmx](https://htmx.org) and [Surreal](https://github.com/gnat/surreal)
* Want fewer layers, less complexity. Are aware of the cargo cult. ✈️

✨ Want to also scope your `&lt;script&gt;` tags? See our companion project [Surreal](https://github.com/gnat/surreal)

## 👁️ How does it look?
```html
&lt;div&gt;
    &lt;style&gt;
        me { background: red; } /* ✨ this &amp; self also work! */
        me button { background: blue; } /* style child elements inline! */
    &lt;/style&gt;
    &lt;button&gt;I&#x27;m blue&lt;/button&gt;
&lt;/div&gt;
```
See the [Live Example](https://gnat.github.io/css-scope-inline/example.html)! Then [view source](https://github.com/gnat/css-scope-inline/blob/main/example.html).

## 🌘 How does it work?

This uses `MutationObserver` to monitor the DOM, and the moment a `&lt;style&gt;` tag is seen, it scopes the styles to whatever the parent element is. No flashing or popping. 

This method also leaves your existing styles untouched, allowing you to mix and match at your leisure.

## 🎁 Install

✂️ copy + 📋 paste the snippet into `&lt;script&gt;` in your `&lt;head&gt;`

Or, [📥 download](https://raw.githubusercontent.com/gnat/css-scope-inline/main/script.js) into your project, and add `&lt;script src=&quot;script.js&quot;&gt;&lt;/script&gt;` in your `&lt;head&gt;`

Or, 🌐 CDN: `&lt;script src=&quot;https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js&quot;&gt;&lt;/script&gt;`

## 🤔 Why consider this over Tailwind CSS?

Use whatever you&#x27;d like, but there&#x27;s a few advantages with this approach over Tailwind, Twind, UnoCSS:

* No more [repeating styles](https://tailwindcss.com/docs/reusing-styles) on child elements (..no [@apply](https://tailwindcss.com/docs/reusing-styles#extracting-classes-with-apply), no `[&amp;&gt;thing]` per style). It&#x27;s just CSS!
* No endless visual noise on every `&lt;div&gt;`. Use a local `&lt;style&gt;` per group.
* No high risk of eventually requiring a build step.
* No chance of [deprecations](https://windicss.org/posts/sunsetting.html). 16 lines is infinitely maintainable.
* Get the ultra-fast &quot;inspect, play with styles, paste&quot; workflow back.
* No suffering from FOUC (a flash of unstyled content).
* Zero friction movement of styles between inline and `.css` files. Just replace `me`
* No special tooling or plugins to install. Universal vanilla CSS. 

## ⚡ Workflow Tips

* Flat, 1 selector per line can be very short like Tailwind. See the examples.
* Use just plain CSS variables in your design system.
* Use the short `@media` queries for responsive design.
  * Mobile First (flow: **above** breakpoint): **🟢 None** `sm` `md` `lg` `xl` `xx` 🏁
  * Desktop First (flow: **below** breakpoint): 🏁 `xs-` `sm-` `md-` `lg-` `xl-` **🟢 None**
  * 🟢 = No breakpoint. Default. See the [Live Example](https://gnat.github.io/css-scope-inline/example.html)!
  * Based on [Tailwind](https://tailwindcss.com/docs/responsive-design) breakpoints. We use `xx` not `2xl` to not break CSS highlighters.
  * Unlike Tailwind, you can [nest your @media styles](https://developer.chrome.com/articles/css-nesting/#nesting-media)!
* Positional selectors may be easier using `div[n1]` for `&lt;div n1&gt;` instead of `div:nth-child(1)`
* Try tools like- Auto complete styles: [VSCode](https://code.visualstudio.com/) or [Sublime](https://packagecontrol.io/packages/Emmet)

## 👁️ CSS Scope Inline vs Tailwind CSS Showdowns
### Basics
Tailwind verbosity goes up with more child elements.
```html
&lt;div&gt;
    &lt;style&gt;
        me { background: red; }
        me div { background: green; }
        me div[n1] { background: yellow; }
        me div[n2] { background: blue; }
    &lt;/style&gt;
    red
    &lt;div&gt;green&lt;/div&gt;
    &lt;div&gt;green&lt;/div&gt;
    &lt;div&gt;green&lt;/div&gt;
    &lt;div n1&gt;yellow&lt;/div&gt;
    &lt;div n2&gt;blue&lt;/div&gt;
    &lt;div&gt;green&lt;/div&gt;
    &lt;div&gt;green&lt;/div&gt;
&lt;/div&gt;

&lt;div class=&quot;bg-[red]&quot;&gt;
    red
    &lt;div class=&quot;bg-[green]&quot;&gt;green&lt;/div&gt;
    &lt;div class=&quot;bg-[green]&quot;&gt;green&lt;/div&gt;
    &lt;div class=&quot;bg-[green]&quot;&gt;green&lt;/div&gt;
    &lt;div class=&quot;bg-[yellow]&quot;&gt;yellow&lt;/div&gt;
    &lt;div class=&quot;bg-[blue]&quot;&gt;blue&lt;/div&gt;
    &lt;div class=&quot;bg-[green]&quot;&gt;green&lt;/div&gt;
    &lt;div class=&quot;bg-[green]&quot;&gt;green&lt;/div&gt;
&lt;/div&gt;
```
### CSS variables and child styling
```html
&lt;!doctype html&gt;
&lt;html&gt;
    &lt;head&gt;
        &lt;style&gt;
            :root {
                --color-1: hsl(0 0% 88%);
                --color-1-active: hsl(214 20% 70%);
            }
        &lt;/style&gt;
        &lt;script src=&quot;https://cdn.tailwindcss.com&quot;&gt;&lt;/script&gt;
        &lt;script src=&quot;https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js&quot;&gt;&lt;/script&gt;
    &lt;/head&gt;
    &lt;body&gt;
        &lt;!-- CSS Scope Inline --&gt;
        &lt;div&gt;
            &lt;style&gt;
               me { margin:8px 6px; }
               me div a { display:block; padding:8px 12px; margin:10px 0; background:var(--color-1); border-radius:10px; text-align:center; }
               me div a:hover { background:var(--color-1-active); color:white; }
            &lt;/style&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Home&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Team&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Profile&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Settings&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Log Out&lt;/a&gt;&lt;/div&gt;
        &lt;/div&gt;

        &lt;!-- Tailwind Example 1 --&gt;
        &lt;div class=&quot;mx-2 my-4&quot;&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot; class=&quot;block py-2 px-3 my-2 bg-[--color-1] rounded-lg text-center hover:bg-[--color-1-active] hover:text-white&quot;&gt;Home&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot; class=&quot;block py-2 px-3 my-2 bg-[--color-1] rounded-lg text-center hover:bg-[--color-1-active] hover:text-white&quot;&gt;Team&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot; class=&quot;block py-2 px-3 my-2 bg-[--color-1] rounded-lg text-center hover:bg-[--color-1-active] hover:text-white&quot;&gt;Profile&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot; class=&quot;block py-2 px-3 my-2 bg-[--color-1] rounded-lg text-center hover:bg-[--color-1-active] hover:text-white&quot;&gt;Settings&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot; class=&quot;block py-2 px-3 my-2 bg-[--color-1] rounded-lg text-center hover:bg-[--color-1-active] hover:text-white&quot;&gt;Log Out&lt;/a&gt;&lt;/div&gt;
        &lt;/div&gt;

        &lt;!-- Tailwind Example 2 --&gt;
        &lt;div class=&quot;mx-2 my-4
            [&amp;_div_a]:block [&amp;_div_a]:py-2 [&amp;_div_a]:px-3 [&amp;_div_a]:my-2 [&amp;_div_a]:bg-[--color-1] [&amp;_div_a]:rounded-lg [&amp;_div_a]:text-center
            [&amp;_div_a:hover]:bg-[--color-1-active] [&amp;_div_a:hover]:text-white&quot;&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Home&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Team&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Profile&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Settings&lt;/a&gt;&lt;/div&gt;
            &lt;div&gt;&lt;a href=&quot;#&quot;&gt;Log Out&lt;/a&gt;&lt;/div&gt;
        &lt;/div&gt;
    &lt;/body&gt;
&lt;/html&gt;
```
## 🔎 Technical FAQ
* Why do you use `querySelectorAll()` and not just process the `MutationObserver` results directly?
  * This was indeed the original design; it will work well up until you begin recieving subtrees (ex: DOM swaps with [htmx](https://htmx.org), ajax, jquery, etc.) which requires walking all subtree elements to ensure we do not miss a `&lt;style&gt;`. This unfortunately involves re-scanning thousands of repeated elements. This is why `querySelectorAll()` ends up the performance (and simplicity) winner.</doc>
    <doc title="HTMX reference" info="Brief description of all HTMX attributes, CSS classes, headers, events, extensions, js lib methods, and config options">+++
title = &quot;Reference&quot;
+++

## Contents

* [htmx Core Attributes](#attributes)
* [htmx Additional Attributes](#attributes-additional)
* [htmx CSS Classes](#classes)
* [htmx Request Headers](#request_headers)
* [htmx Response Headers](#response_headers)
* [htmx Events](#events)
* [htmx Extensions](https://extensions.htmx.org)
* [JavaScript API](#api)
* [Configuration Options](#config)

## Core Attribute Reference {#attributes}

The most common attributes when using htmx.

&lt;div class=&quot;info-table&quot;&gt;

| Attribute                                        | Description                                                                                                        |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| [`hx-get`](@/attributes/hx-get.md)               | issues a `GET` to the specified URL                                                                                |
| [`hx-post`](@/attributes/hx-post.md)             | issues a `POST` to the specified URL                                                                               |
| [`hx-on*`](@/attributes/hx-on.md)                | handle events with inline scripts on elements                                                                      |
| [`hx-push-url`](@/attributes/hx-push-url.md)     | push a URL into the browser location bar to create history                                                         |
| [`hx-select`](@/attributes/hx-select.md)         | select content to swap in from a response                                                                          |
| [`hx-select-oob`](@/attributes/hx-select-oob.md) | select content to swap in from a response, somewhere other than the target (out of band)                           |
| [`hx-swap`](@/attributes/hx-swap.md)             | controls how content will swap in (`outerHTML`, `beforeend`, `afterend`, ...)                                      |
| [`hx-swap-oob`](@/attributes/hx-swap-oob.md)     | mark element to swap in from a response (out of band)                                                              |
| [`hx-target`](@/attributes/hx-target.md)         | specifies the target element to be swapped                                                                         |
| [`hx-trigger`](@/attributes/hx-trigger.md)       | specifies the event that triggers the request                                                                      |
| [`hx-vals`](@/attributes/hx-vals.md)             | add values to submit with the request (JSON format)                                                                |

&lt;/div&gt;

## Additional Attribute Reference {#attributes-additional}

All other attributes available in htmx.

&lt;div class=&quot;info-table&quot;&gt;

| Attribute                                            | Description                                                                                                                        |
|------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| [`hx-boost`](@/attributes/hx-boost.md)               | add [progressive enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement) for links and forms                           |
| [`hx-confirm`](@/attributes/hx-confirm.md)           | shows a `confirm()` dialog before issuing a request                                                                                |
| [`hx-delete`](@/attributes/hx-delete.md)             | issues a `DELETE` to the specified URL                                                                                             |
| [`hx-disable`](@/attributes/hx-disable.md)           | disables htmx processing for the given node and any children nodes                                                                 |
| [`hx-disabled-elt`](@/attributes/hx-disabled-elt.md) | adds the `disabled` attribute to the specified elements while a request is in flight                                               |
| [`hx-disinherit`](@/attributes/hx-disinherit.md)     | control and disable automatic attribute inheritance for child nodes                                                                |
| [`hx-encoding`](@/attributes/hx-encoding.md)         | changes the request encoding type                                                                                                  |
| [`hx-ext`](@/attributes/hx-ext.md)                   | extensions to use for this element                                                                                                 |
| [`hx-headers`](@/attributes/hx-headers.md)           | adds to the headers that will be submitted with the request                                                                        |
| [`hx-history`](@/attributes/hx-history.md)           | prevent sensitive data being saved to the history cache                                                                            |
| [`hx-history-elt`](@/attributes/hx-history-elt.md)   | the element to snapshot and restore during history navigation                                                                      |
| [`hx-include`](@/attributes/hx-include.md)           | include additional data in requests                                                                                                |
| [`hx-indicator`](@/attributes/hx-indicator.md)       | the element to put the `htmx-request` class on during the request                                                                  |
| [`hx-inherit`](@/attributes/hx-inherit.md)           | control and enable automatic attribute inheritance for child nodes if it has been disabled by default                            |
| [`hx-params`](@/attributes/hx-params.md)             | filters the parameters that will be submitted with a request                                                                       |
| [`hx-patch`](@/attributes/hx-patch.md)               | issues a `PATCH` to the specified URL                                                                                              |
| [`hx-preserve`](@/attributes/hx-preserve.md)         | specifies elements to keep unchanged between requests                                                                              |
| [`hx-prompt`](@/attributes/hx-prompt.md)             | shows a `prompt()` before submitting a request                                                                                     |
| [`hx-put`](@/attributes/hx-put.md)                   | issues a `PUT` to the specified URL                                                                                                |
| [`hx-replace-url`](@/attributes/hx-replace-url.md)   | replace the URL in the browser location bar                                                                                        |
| [`hx-request`](@/attributes/hx-request.md)           | configures various aspects of the request                                                                                          |
| [`hx-sync`](@/attributes/hx-sync.md)                 | control how requests made by different elements are synchronized                                                                   |
| [`hx-validate`](@/attributes/hx-validate.md)         | force elements to validate themselves before a request                                                                             |
| [`hx-vars`](@/attributes/hx-vars.md)                 | adds values dynamically to the parameters to submit with the request (deprecated, please use [`hx-vals`](@/attributes/hx-vals.md)) |

&lt;/div&gt;

## CSS Class Reference {#classes}

&lt;div class=&quot;info-table&quot;&gt;

| Class | Description |
|-----------|-------------|
| `htmx-added` | Applied to a new piece of content before it is swapped, removed after it is settled.
| `htmx-indicator` | A dynamically generated class that will toggle visible (opacity:1) when a `htmx-request` class is present
| `htmx-request` | Applied to either the element or the element specified with [`hx-indicator`](@/attributes/hx-indicator.md) while a request is ongoing
| `htmx-settling` | Applied to a target after content is swapped, removed after it is settled. The duration can be modified via [`hx-swap`](@/attributes/hx-swap.md).
| `htmx-swapping` | Applied to a target before any content is swapped, removed after it is swapped. The duration can be modified via [`hx-swap`](@/attributes/hx-swap.md).

&lt;/div&gt;

## HTTP Header Reference {#headers}

### Request Headers Reference {#request_headers}

&lt;div class=&quot;info-table&quot;&gt;

| Header | Description |
|--------|-------------|
| `HX-Boosted` | indicates that the request is via an element using [hx-boost](@/attributes/hx-boost.md)
| `HX-Current-URL` | the current URL of the browser
| `HX-History-Restore-Request` | &quot;true&quot; if the request is for history restoration after a miss in the local history cache
| `HX-Prompt` | the user response to an [hx-prompt](@/attributes/hx-prompt.md)
| `HX-Request` | always &quot;true&quot;
| `HX-Target` | the `id` of the target element if it exists
| `HX-Trigger-Name` | the `name` of the triggered element if it exists
| `HX-Trigger` | the `id` of the triggered element if it exists

&lt;/div&gt;

### Response Headers Reference {#response_headers}

&lt;div class=&quot;info-table&quot;&gt;

| Header                                               | Description |
|------------------------------------------------------|-------------|
| [`HX-Location`](@/headers/hx-location.md)            | allows you to do a client-side redirect that does not do a full page reload
| [`HX-Push-Url`](@/headers/hx-push-url.md)            | pushes a new url into the history stack
| `HX-Redirect`                                        | can be used to do a client-side redirect to a new location
| `HX-Refresh`                                         | if set to &quot;true&quot; the client-side will do a full refresh of the page
| [`HX-Replace-Url`](@/headers/hx-replace-url.md)      | replaces the current URL in the location bar
| `HX-Reswap`                                          | allows you to specify how the response will be swapped. See [hx-swap](@/attributes/hx-swap.md) for possible values
| `HX-Retarget`                                        | a CSS selector that updates the target of the content update to a different element on the page
| `HX-Reselect`                                        | a CSS selector that allows you to choose which part of the response is used to be swapped in. Overrides an existing [`hx-select`](@/attributes/hx-select.md) on the triggering element
| [`HX-Trigger`](@/headers/hx-trigger.md)              | allows you to trigger client-side events
| [`HX-Trigger-After-Settle`](@/headers/hx-trigger.md) | allows you to trigger client-side events after the settle step
| [`HX-Trigger-After-Swap`](@/headers/hx-trigger.md)   | allows you to trigger client-side events after the swap step

&lt;/div&gt;

## Event Reference {#events}

&lt;div class=&quot;info-table&quot;&gt;

| Event | Description |
|-------|-------------|
| [`htmx:abort`](@/events.md#htmx:abort) | send this event to an element to abort a request
| [`htmx:afterOnLoad`](@/events.md#htmx:afterOnLoad) | triggered after an AJAX request has completed processing a successful response
| [`htmx:afterProcessNode`](@/events.md#htmx:afterProcessNode) | triggered after htmx has initialized a node
| [`htmx:afterRequest`](@/events.md#htmx:afterRequest)  | triggered after an AJAX request has completed
| [`htmx:afterSettle`](@/events.md#htmx:afterSettle)  | triggered after the DOM has settled
| [`htmx:afterSwap`](@/events.md#htmx:afterSwap)  | triggered after new content has been swapped in
| [`htmx:beforeCleanupElement`](@/events.md#htmx:beforeCleanupElement)  | triggered before htmx [disables](@/attributes/hx-disable.md) an element or removes it from the DOM
| [`htmx:beforeOnLoad`](@/events.md#htmx:beforeOnLoad)  | triggered before any response processing occurs
| [`htmx:beforeProcessNode`](@/events.md#htmx:beforeProcessNode) | triggered before htmx initializes a node
| [`htmx:beforeRequest`](@/events.md#htmx:beforeRequest)  | triggered before an AJAX request is made
| [`htmx:beforeSwap`](@/events.md#htmx:beforeSwap)  | triggered before a swap is done, allows you to configure the swap
| [`htmx:beforeSend`](@/events.md#htmx:beforeSend)  | triggered just before an ajax request is sent
| [`htmx:configRequest`](@/events.md#htmx:configRequest)  | triggered before the request, allows you to customize parameters, headers
| [`htmx:confirm`](@/events.md#htmx:confirm)  | triggered after a trigger occurs on an element, allows you to cancel (or delay) issuing the AJAX request
| [`htmx:historyCacheError`](@/events.md#htmx:historyCacheError)  | triggered on an error during cache writing
| [`htmx:historyCacheMiss`](@/events.md#htmx:historyCacheMiss)  | triggered on a cache miss in the history subsystem
| [`htmx:historyCacheMissError`](@/events.md#htmx:historyCacheMissError)  | triggered on a unsuccessful remote retrieval
| [`htmx:historyCacheMissLoad`](@/events.md#htmx:historyCacheMissLoad)  | triggered on a successful remote retrieval
| [`htmx:historyRestore`](@/events.md#htmx:historyRestore)  | triggered when htmx handles a history restoration action
| [`htmx:beforeHistorySave`](@/events.md#htmx:beforeHistorySave)  | triggered before content is saved to the history cache
| [`htmx:load`](@/events.md#htmx:load)  | triggered when new content is added to the DOM
| [`htmx:noSSESourceError`](@/events.md#htmx:noSSESourceError)  | triggered when an element refers to a SSE event in its trigger, but no parent SSE source has been defined
| [`htmx:onLoadError`](@/events.md#htmx:onLoadError)  | triggered when an exception occurs during the onLoad handling in htmx
| [`htmx:oobAfterSwap`](@/events.md#htmx:oobAfterSwap)  | triggered after an out of band element as been swapped in
| [`htmx:oobBeforeSwap`](@/events.md#htmx:oobBeforeSwap)  | triggered before an out of band element swap is done, allows you to configure the swap
| [`htmx:oobErrorNoTarget`](@/events.md#htmx:oobErrorNoTarget)  | triggered when an out of band element does not have a matching ID in the current DOM
| [`htmx:prompt`](@/events.md#htmx:prompt)  | triggered after a prompt is shown
| [`htmx:pushedIntoHistory`](@/events.md#htmx:pushedIntoHistory)  | triggered after an url is pushed into history
| [`htmx:responseError`](@/events.md#htmx:responseError)  | triggered when an HTTP response error (non-`200` or `300` response code) occurs
| [`htmx:sendError`](@/events.md#htmx:sendError)  | triggered when a network error prevents an HTTP request from happening
| [`htmx:sseError`](@/events.md#htmx:sseError)  | triggered when an error occurs with a SSE source
| [`htmx:sseOpen`](/events#htmx:sseOpen)  | triggered when a SSE source is opened
| [`htmx:swapError`](@/events.md#htmx:swapError)  | triggered when an error occurs during the swap phase
| [`htmx:targetError`](@/events.md#htmx:targetError)  | triggered when an invalid target is specified
| [`htmx:timeout`](@/events.md#htmx:timeout)  | triggered when a request timeout occurs
| [`htmx:validation:validate`](@/events.md#htmx:validation:validate)  | triggered before an element is validated
| [`htmx:validation:failed`](@/events.md#htmx:validation:failed)  | triggered when an element fails validation
| [`htmx:validation:halted`](@/events.md#htmx:validation:halted)  | triggered when a request is halted due to validation errors
| [`htmx:xhr:abort`](@/events.md#htmx:xhr:abort)  | triggered when an ajax request aborts
| [`htmx:xhr:loadend`](@/events.md#htmx:xhr:loadend)  | triggered when an ajax request ends
| [`htmx:xhr:loadstart`](@/events.md#htmx:xhr:loadstart)  | triggered when an ajax request starts
| [`htmx:xhr:progress`](@/events.md#htmx:xhr:progress)  | triggered periodically during an ajax request that supports progress events

&lt;/div&gt;

## JavaScript API Reference {#api}

&lt;div class=&quot;info-table&quot;&gt;

| Method | Description |
|-------|-------------|
| [`htmx.addClass()`](@/api.md#addClass)  | Adds a class to the given element
| [`htmx.ajax()`](@/api.md#ajax)  | Issues an htmx-style ajax request
| [`htmx.closest()`](@/api.md#closest)  | Finds the closest parent to the given element matching the selector
| [`htmx.config`](@/api.md#config)  | A property that holds the current htmx config object
| [`htmx.createEventSource`](@/api.md#createEventSource)  | A property holding the function to create SSE EventSource objects for htmx
| [`htmx.createWebSocket`](@/api.md#createWebSocket)  | A property holding the function to create WebSocket objects for htmx
| [`htmx.defineExtension()`](@/api.md#defineExtension)  | Defines an htmx [extension](https://extensions.htmx.org)
| [`htmx.find()`](@/api.md#find)  | Finds a single element matching the selector
| [`htmx.findAll()` `htmx.findAll(elt, selector)`](@/api.md#find)  | Finds all elements matching a given selector
| [`htmx.logAll()`](@/api.md#logAll)  | Installs a logger that will log all htmx events
| [`htmx.logger`](@/api.md#logger)  | A property set to the current logger (default is `null`)
| [`htmx.off()`](@/api.md#off)  | Removes an event listener from the given element
| [`htmx.on()`](@/api.md#on)  | Creates an event listener on the given element, returning it
| [`htmx.onLoad()`](@/api.md#onLoad)  | Adds a callback handler for the `htmx:load` event
| [`htmx.parseInterval()`](@/api.md#parseInterval)  | Parses an interval declaration into a millisecond value
| [`htmx.process()`](@/api.md#process)  | Processes the given element and its children, hooking up any htmx behavior
| [`htmx.remove()`](@/api.md#remove)  | Removes the given element
| [`htmx.removeClass()`](@/api.md#removeClass)  | Removes a class from the given element
| [`htmx.removeExtension()`](@/api.md#removeExtension)  | Removes an htmx [extension](https://extensions.htmx.org)
| [`htmx.swap()`](@/api.md#swap)  | Performs swapping (and settling) of HTML content
| [`htmx.takeClass()`](@/api.md#takeClass)  | Takes a class from other elements for the given element
| [`htmx.toggleClass()`](@/api.md#toggleClass)  | Toggles a class from the given element
| [`htmx.trigger()`](@/api.md#trigger)  | Triggers an event on an element
| [`htmx.values()`](@/api.md#values)  | Returns the input values associated with the given element

&lt;/div&gt;


## Configuration Reference {#config}

Htmx has some configuration options that can be accessed either programmatically or declaratively.  They are
listed below:

&lt;div class=&quot;info-table&quot;&gt;

| Config Variable                       | Info                                                                                                                                                                       |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `htmx.config.historyEnabled`          | defaults to `true`, really only useful for testing                                                                                                                         |
| `htmx.config.historyCacheSize`        | defaults to 10                                                                                                                                                             |
| `htmx.config.refreshOnHistoryMiss`    | defaults to `false`, if set to `true` htmx will issue a full page refresh on history misses rather than use an AJAX request                                                |
| `htmx.config.defaultSwapStyle`        | defaults to `innerHTML`                                                                                                                                                    |
| `htmx.config.defaultSwapDelay`        | defaults to 0                                                                                                                                                              |
| `htmx.config.defaultSettleDelay`      | defaults to 20                                                                                                                                                             |
| `htmx.config.includeIndicatorStyles`  | defaults to `true` (determines if the indicator styles are loaded)                                                                                                         |
| `htmx.config.indicatorClass`          | defaults to `htmx-indicator`                                                                                                                                               |
| `htmx.config.requestClass`            | defaults to `htmx-request`                                                                                                                                                 |
| `htmx.config.addedClass`              | defaults to `htmx-added`                                                                                                                                                   |
| `htmx.config.settlingClass`           | defaults to `htmx-settling`                                                                                                                                                |
| `htmx.config.swappingClass`           | defaults to `htmx-swapping`                                                                                                                                                |
| `htmx.config.allowEval`               | defaults to `true`, can be used to disable htmx&#x27;s use of eval for certain features (e.g. trigger filters)                                                                  |
| `htmx.config.allowScriptTags`         | defaults to `true`, determines if htmx will process script tags found in new content                                                                                       |
| `htmx.config.inlineScriptNonce`       | defaults to `&#x27;&#x27;`, meaning that no nonce will be added to inline scripts                                                                                                    |
| `htmx.config.inlineStyleNonce`        | defaults to `&#x27;&#x27;`, meaning that no nonce will be added to inline styles                                                                                                     |
| `htmx.config.attributesToSettle`      | defaults to `[&quot;class&quot;, &quot;style&quot;, &quot;width&quot;, &quot;height&quot;]`, the attributes to settle during the settling phase                                                                    |
| `htmx.config.wsReconnectDelay`        | defaults to `full-jitter`                                                                                                                                                  |
| `htmx.config.wsBinaryType`            | defaults to `blob`, the [the type of binary data](https://developer.mozilla.org/docs/Web/API/WebSocket/binaryType) being received over the WebSocket connection            |
| `htmx.config.disableSelector`         | defaults to `[hx-disable], [data-hx-disable]`, htmx will not process elements with this attribute on it or a parent                                                        |
| `htmx.config.withCredentials`         | defaults to `false`, allow cross-site Access-Control requests using credentials such as cookies, authorization headers or TLS client certificates                          |
| `htmx.config.timeout`                 | defaults to 0, the number of milliseconds a request can take before automatically being terminated                                                                         |
| `htmx.config.scrollBehavior`          | defaults to &#x27;instant&#x27;, the behavior for a boosted link on page transitions. The allowed values are `auto`, `instant` and `smooth`. Instant will scroll instantly in a single jump, smooth will scroll smoothly, while auto will behave like a vanilla link. |
| `htmx.config.defaultFocusScroll`      | if the focused element should be scrolled into view, defaults to false and can be overridden using the [focus-scroll](@/attributes/hx-swap.md#focus-scroll) swap modifier. |
| `htmx.config.getCacheBusterParam`     | defaults to false, if set to true htmx will append the target element to the `GET` request in the format `org.htmx.cache-buster=targetElementId`                           |
| `htmx.config.globalViewTransitions`   | if set to `true`, htmx will use the [View Transition](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API) API when swapping in new content.             |
| `htmx.config.methodsThatUseUrlParams` | defaults to `[&quot;get&quot;]`, htmx will format requests with these methods by encoding their parameters in the URL, not the request body                                          |
| `htmx.config.selfRequestsOnly`        | defaults to `true`, whether to only allow AJAX requests to the same domain as the current document                                                             |
| `htmx.config.ignoreTitle`             | defaults to `false`, if set to `true` htmx will not update the title of the document when a `title` tag is found in new content                                            |
| `htmx.config.scrollIntoViewOnBoost`   | defaults to `true`, whether or not the target of a boosted element is scrolled into the viewport. If `hx-target` is omitted on a boosted element, the target defaults to `body`, causing the page to scroll to the top. |
| `htmx.config.triggerSpecsCache`       | defaults to `null`, the cache to store evaluated trigger specifications into, improving parsing performance at the cost of more memory usage. You may define a simple object to use a never-clearing cache, or implement your own system using a [proxy object](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Proxy) |
| `htmx.config.allowNestedOobSwaps`     | defaults to `true`, whether to process OOB swaps on elements that are nested within the main response element. See [Nested OOB Swaps](@/attributes/hx-swap-oob.md#nested-oob-swaps). |

&lt;/div&gt;

You can set them directly in javascript, or you can use a `meta` tag:

```html
&lt;meta name=&quot;htmx-config&quot; content=&#x27;{&quot;defaultSwapStyle&quot;:&quot;outerHTML&quot;}&#x27;&gt;
```</doc>
  </docs>
  <examples>
    <doc title="Websockets application">from asyncio import sleep
from fasthtml.common import *

app = FastHTML(ws_hdr=True)
rt = app.route

def mk_inp(): return Input(id=&#x27;msg&#x27;)
nid = &#x27;notifications&#x27;

@rt(&#x27;/&#x27;)
async def get():
    cts = Div(
        Div(id=nid),
        Form(mk_inp(), id=&#x27;form&#x27;, ws_send=True),
        hx_ext=&#x27;ws&#x27;, ws_connect=&#x27;/ws&#x27;)
    return Titled(&#x27;Websocket Test&#x27;, cts)

async def on_connect(send): await send(Div(&#x27;Hello, you have connected&#x27;, id=nid))
async def on_disconnect( ): print(&#x27;Disconnected!&#x27;)

@app.ws(&#x27;/ws&#x27;, conn=on_connect, disconn=on_disconnect)
async def ws(msg:str, send):
    await send(Div(&#x27;Hello &#x27; + msg, id=nid))
    await sleep(2)
    return Div(&#x27;Goodbye &#x27; + msg, id=nid), mk_inp()

serve()
</doc>
    <doc title="Todo list application">###
# Walkthrough of an idiomatic fasthtml app
###

# This fasthtml app includes functionality from fastcore, starlette, fastlite, and fasthtml itself.
# Run with: `python adv_app.py`
# Importing from `fasthtml.common` brings the key parts of all of these together.
# For simplicity, you can just `from fasthtml.common import *`:
from fasthtml.common import *
# ...or you can import everything into a namespace:
# from fasthtml import common as fh
# ...or you can import each symbol explicitly (which we&#x27;re commenting out here but including for completeness):
&quot;&quot;&quot;
from fasthtml.common import (
    # These are the HTML components we use in this app
    A, AX, Button, Card, CheckboxX, Container, Div, Form, Grid, Group, H1, H2, Hidden, Input, Li, Main, Script, Style, Textarea, Title, Titled, Ul,
    # These are FastHTML symbols we&#x27;ll use
    Beforeware, FastHTML, fast_app, SortableJS, fill_form, picolink, serve,
    # These are from Starlette, Fastlite, fastcore, and the Python stdlib
    FileResponse, NotFoundError, RedirectResponse, database, patch, dataclass
)
&quot;&quot;&quot;

from hmac import compare_digest

# You can use any database you want; it&#x27;ll be easier if you pick a lib that supports the MiniDataAPI spec.
# Here we are using SQLite, with the FastLite library, which supports the MiniDataAPI spec.
db = database(&#x27;data/utodos.db&#x27;)
# The `t` attribute is the table collection. The `todos` and `users` tables are not created if they don&#x27;t exist.
# Instead, you can use the `create` method to create them if needed.
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    # You can pass a dict, or kwargs, to most MiniDataAPI methods.
    users.create(dict(name=str, pwd=str), pk=&#x27;name&#x27;)
    todos.create(id=int, title=str, done=bool, name=str, details=str, priority=int, pk=&#x27;id&#x27;)
# Although you can just use dicts, it can be helpful to have types for your DB objects.
# The `dataclass` method creates that type, and stores it in the object, so it will use it for any returned items.
Todo,User = todos.dataclass(),users.dataclass()

# Any Starlette response class can be returned by a FastHTML route handler.
# In that case, FastHTML won&#x27;t change it at all.
# Status code 303 is a redirect that can change POST to GET, so it&#x27;s appropriate for a login page.
login_redir = RedirectResponse(&#x27;/login&#x27;, status_code=303)

# The `before` function is a *Beforeware* function. These are functions that run before a route handler is called.
def before(req, sess):
    # This sets the `auth` attribute in the request scope, and gets it from the session.
    # The session is a Starlette session, which is a dict-like object which is cryptographically signed,
    # so it can&#x27;t be tampered with.
    # The `auth` key in the scope is automatically provided to any handler which requests it, and can not
    # be injected by the user using query params, cookies, etc, so it should be secure to use.
    auth = req.scope[&#x27;auth&#x27;] = sess.get(&#x27;auth&#x27;, None)
    # If the session key is not there, it redirects to the login page.
    if not auth: return login_redir
    # `xtra` is part of the MiniDataAPI spec. It adds a filter to queries and DDL statements,
    # to ensure that the user can only see/edit their own todos.
    todos.xtra(name=auth)

markdown_js = &quot;&quot;&quot;
import { marked } from &quot;https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js&quot;;
import { proc_htmx} from &quot;https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js/fasthtml.js&quot;;
proc_htmx(&#x27;.markdown&#x27;, e =&gt; e.innerHTML = marked.parse(e.textContent));
&quot;&quot;&quot;

# We will use this in our `exception_handlers` dict
def _not_found(req, exc): return Titled(&#x27;Oh no!&#x27;, Div(&#x27;We could not find that page :(&#x27;))

# To create a Beforeware object, we pass the function itself, and optionally a list of regexes to skip.
bware = Beforeware(before, skip=[r&#x27;/favicon\.ico&#x27;, r&#x27;/static/.*&#x27;, r&#x27;.*\.css&#x27;, &#x27;/login&#x27;])
# The `FastHTML` class is a subclass of `Starlette`, so you can use any parameters that `Starlette` accepts.
# In addition, you can add your Beforeware here, and any headers you want included in HTML responses.
# FastHTML includes the &quot;HTMX&quot; and &quot;Surreal&quot; libraries in headers, unless you pass `default_hdrs=False`.
app = FastHTML(before=bware,
               # These are the same as Starlette exception_handlers, except they also support `FT` results
               exception_handlers={404: _not_found},
               # PicoCSS is a particularly simple CSS framework, with some basic integration built in to FastHTML.
               # `picolink` is pre-defined with the header for the PicoCSS stylesheet.
               # You can use any CSS framework you want, or none at all.
               hdrs=(picolink,
                     # `Style` is an `FT` object, which are 3-element lists consisting of:
                     # (tag_name, children_list, attrs_dict).
                     # FastHTML composes them from trees and auto-converts them to HTML when needed.
                     # You can also use plain HTML strings in handlers and headers,
                     # which will be auto-escaped, unless you use `NotStr(...string...)`.
                     Style(&#x27;:root { --pico-font-size: 100%; }&#x27;),
                     # Have a look at fasthtml/js.py to see how these Javascript libraries are added to FastHTML.
                     # They are only 5-10 lines of code each, and you can add your own too.
                     SortableJS(&#x27;.sortable&#x27;),
                     # MarkdownJS is actually provided as part of FastHTML, but we&#x27;ve included the js code here
                     # so that you can see how it works.
                     Script(markdown_js, type=&#x27;module&#x27;))
                )
# We add `rt` as a shortcut for `app.route`, which is what we&#x27;ll use to decorate our route handlers.
# When using `app.route` (or this shortcut), the only required argument is the path.
# The name of the decorated function (eg `get`, `post`, etc) is used as the HTTP verb for the handler.
rt = app.route

# For instance, this function handles GET requests to the `/login` path.
@rt(&quot;/login&quot;)
def get():
    # This creates a form with two input fields, and a submit button.
    # All of these components are `FT` objects. All HTML tags are provided in this form by FastHTML.
    # If you want other custom tags (e.g. `MyTag`), they can be auto-generated by e.g
    # `from fasthtml.components import MyTag`.
    # Alternatively, manually call e.g `ft(tag_name, *children, **attrs)`.
    frm = Form(
        # Tags with a `name` attr will have `name` auto-set to the same as `id` if not provided
        Input(id=&#x27;name&#x27;, placeholder=&#x27;Name&#x27;),
        Input(id=&#x27;pwd&#x27;, type=&#x27;password&#x27;, placeholder=&#x27;Password&#x27;),
        Button(&#x27;login&#x27;),
        action=&#x27;/login&#x27;, method=&#x27;post&#x27;)
    # If a user visits the URL directly, FastHTML auto-generates a full HTML page.
    # However, if the URL is accessed by HTMX, then one HTML partial is created for each element of the tuple.
    # To avoid this auto-generation of a full page, return a `HTML` object, or a Starlette `Response`.
    # `Titled` returns a tuple of a `Title` with the first arg and a `Container` with the rest.
    # See the comments for `Title` later for details.
    return Titled(&quot;Login&quot;, frm)

# Handlers are passed whatever information they &quot;request&quot; in the URL, as keyword arguments.
# Dataclasses, dicts, namedtuples, TypedDicts, and custom classes are automatically instantiated
# from form data.
# In this case, the `Login` class is a dataclass, so the handler will be passed `name` and `pwd`.
@dataclass
class Login: name:str; pwd:str

# This handler is called when a POST request is made to the `/login` path.
# The `login` argument is an instance of the `Login` class, which has been auto-instantiated from the form data.
# There are a number of special parameter names, which will be passed useful information about the request:
# `session`: the Starlette session; `request`: the Starlette request; `auth`: the value of `scope[&#x27;auth&#x27;]`,
# `htmx`: the HTMX headers, if any; `app`: the FastHTML app object.
# You can also pass any string prefix of `request` or `session`.
@rt(&quot;/login&quot;)
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    # Indexing into a MiniDataAPI table queries by primary key, which is `name` here.
    # It returns a dataclass object, if `dataclass()` has been called at some point, or a dict otherwise.
    try: u = users[login.name]
    # If the primary key does not exist, the method raises a `NotFoundError`.
    # Here we use this to just generate a user -- in practice you&#x27;d probably to redirect to a signup page.
    except NotFoundError: u = users.insert(login)
    # This compares the passwords using a constant time string comparison
    # https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python
    if not compare_digest(u.pwd.encode(&quot;utf-8&quot;), login.pwd.encode(&quot;utf-8&quot;)): return login_redir
    # Because the session is signed, we can securely add information to it. It&#x27;s stored in the browser cookies.
    # If you don&#x27;t pass a secret signing key to `FastHTML`, it will auto-generate one and store it in a file `./sesskey`.
    sess[&#x27;auth&#x27;] = u.name
    return RedirectResponse(&#x27;/&#x27;, status_code=303)

# Instead of using `app.route` (or the `rt` shortcut), you can also use `app.get`, `app.post`, etc.
# In this case, the function name is not used to determine the HTTP verb.
@app.get(&quot;/logout&quot;)
def logout(sess):
    del sess[&#x27;auth&#x27;]
    return login_redir

# FastHTML uses Starlette&#x27;s path syntax, and adds a `static` type which matches standard static file extensions.
# You can define your own regex path specifiers -- for instance this is how `static` is defined in FastHTML
# `reg_re_param(&quot;static&quot;, &quot;ico|gif|jpg|jpeg|webm|css|js|woff|png|svg|mp4|webp|ttf|otf|eot|woff2|txt|xml|html&quot;)`
# In this app, we only actually have one static file, which is `favicon.ico`. But it would also be needed if
# we were referencing images, CSS/JS files, etc.
# Note, this function is unnecessary, as the `fast_app()` call already includes this functionality.
# However, it&#x27;s included here to show how you can define your own static file handler.
@rt(&quot;/{fname:path}.{ext:static}&quot;)
async def get(fname:str, ext:str): return FileResponse(f&#x27;{fname}.{ext}&#x27;)

# The `patch` decorator, which is defined in `fastcore`, adds a method to an existing class.
# Here we are adding a method to the `Todo` class, which is returned by the `todos` table.
# The `__ft__` method is a special method that FastHTML uses to convert the object into an `FT` object,
# so that it can be composed into an FT tree, and later rendered into HTML.
@patch
def __ft__(self:Todo):
    # Some FastHTML tags have an &#x27;X&#x27; suffix, which means they&#x27;re &quot;extended&quot; in some way.
    # For instance, here `AX` is an extended `A` tag, which takes 3 positional arguments:
    # `(text, hx_get, target_id)`.
    # All underscores in FT attrs are replaced with hyphens, so this will create an `hx-get` attr,
    # which HTMX uses to trigger a GET request.
    # Generally, most of your route handlers in practice (as in this demo app) are likely to be HTMX handlers.
    # For instance, for this demo, we only have two full-page handlers: the &#x27;/login&#x27; and &#x27;/&#x27; GET handlers.
    show = AX(self.title, f&#x27;/todos/{self.id}&#x27;, &#x27;current-todo&#x27;)
    edit = AX(&#x27;edit&#x27;,     f&#x27;/edit/{self.id}&#x27; , &#x27;current-todo&#x27;)
    dt = &#x27;✅ &#x27; if self.done else &#x27;&#x27;
    # FastHTML provides some shortcuts. For instance, `Hidden` is defined as simply:
    # `return Input(type=&quot;hidden&quot;, value=value, **kwargs)`
    cts = (dt, show, &#x27; | &#x27;, edit, Hidden(id=&quot;id&quot;, value=self.id), Hidden(id=&quot;priority&quot;, value=&quot;0&quot;))
    # Any FT object can take a list of children as positional args, and a dict of attrs as keyword args.
    return Li(*cts, id=f&#x27;todo-{self.id}&#x27;)

# This is the handler for the main todo list application.
# By including the `auth` parameter, it gets passed the current username, for displaying in the title.
@rt(&quot;/&quot;)
def get(auth):
    title = f&quot;{auth}&#x27;s Todo list&quot;
    top = Grid(H1(title), Div(A(&#x27;logout&#x27;, href=&#x27;/logout&#x27;), style=&#x27;text-align: right&#x27;))
    # We don&#x27;t normally need separate &quot;screens&quot; for adding or editing data. Here for instance,
    # we&#x27;re using an `hx-post` to add a new todo, which is added to the start of the list (using &#x27;afterbegin&#x27;).
    new_inp = Input(id=&quot;new-title&quot;, name=&quot;title&quot;, placeholder=&quot;New Todo&quot;)
    add = Form(Group(new_inp, Button(&quot;Add&quot;)),
               hx_post=&quot;/&quot;, target_id=&#x27;todo-list&#x27;, hx_swap=&quot;afterbegin&quot;)
    # In the MiniDataAPI spec, treating a table as a callable (i.e with `todos(...)` here) queries the table.
    # Because we called `xtra` in our Beforeware, this queries the todos for the current user only.
    # We can include the todo objects directly as children of the `Form`, because the `Todo` class has `__ft__` defined.
    # This is automatically called by FastHTML to convert the `Todo` objects into `FT` objects when needed.
    # The reason we put the todo list inside a form is so that we can use the &#x27;sortable&#x27; js library to reorder them.
    # That library calls the js `end` event when dragging is complete, so our trigger here causes our `/reorder`
    # handler to be called.
    frm = Form(*todos(order_by=&#x27;priority&#x27;),
               id=&#x27;todo-list&#x27;, cls=&#x27;sortable&#x27;, hx_post=&quot;/reorder&quot;, hx_trigger=&quot;end&quot;)
    # We create an empty &#x27;current-todo&#x27; Div at the bottom of our page, as a target for the details and editing views.
    card = Card(Ul(frm), header=add, footer=Div(id=&#x27;current-todo&#x27;))
    # PicoCSS uses `&lt;Main class=&#x27;container&#x27;&gt;` page content; `Container` is a tiny function that generates that.
    # A handler can return either a single `FT` object or string, or a tuple of them.
    # In the case of a tuple, the stringified objects are concatenated and returned to the browser.
    # The `Title` tag has a special purpose: it sets the title of the page.
    return Title(title), Container(top, card)

# This is the handler for the reordering of todos.
# It&#x27;s a POST request, which is used by the &#x27;sortable&#x27; js library.
# Because the todo list form created earlier included hidden inputs with the todo IDs,
# they are passed as form data. By using a parameter called (e.g) &quot;id&quot;, FastHTML will try to find
# something suitable in the request with this name. In order, it searches as follows:
# path; query; cookies; headers; session keys; form data.
# Although all these are provided in the request as strings, FastHTML will use your parameter&#x27;s type
# annotation to try to cast the value to the requested type.
# In the case of form data, there can be multiple values with the same key. So in this case,
# the parameter is a list of ints.
@rt(&quot;/reorder&quot;)
def post(id:list[int]):
    for i,id_ in enumerate(id): todos.update({&#x27;priority&#x27;:i}, id_)
    # HTMX by default replaces the inner HTML of the calling element, which in this case is the todo list form.
    # Therefore, we return the list of todos, now in the correct order, which will be auto-converted to FT for us.
    # In this case, it&#x27;s not strictly necessary, because sortable.js has already reorder the DOM elements.
    # However, by returning the updated data, we can be assured that there aren&#x27;t sync issues between the DOM
    # and the server.
    return tuple(todos(order_by=&#x27;priority&#x27;))

# Refactoring components in FastHTML is as simple as creating Python functions.
# The `clr_details` function creates a Div with specific HTMX attributes.
# `hx_swap_oob=&#x27;innerHTML&#x27;` tells HTMX to swap the inner HTML of the target element out-of-band,
# meaning it will update this element regardless of where the HTMX request originated from.
def clr_details(): return Div(hx_swap_oob=&#x27;innerHTML&#x27;, id=&#x27;current-todo&#x27;)

# This route handler uses a path parameter `{id}` which is automatically parsed and passed as an int.
@rt(&quot;/todos/{id}&quot;)
def delete(id:int):
    # The `delete` method is part of the MiniDataAPI spec, removing the item with the given primary key.
    todos.delete(id)
    # Returning `clr_details()` ensures the details view is cleared after deletion,
    # leveraging HTMX&#x27;s out-of-band swap feature.
    # Note that we are not returning *any* FT component that doesn&#x27;t have an &quot;OOB&quot; swap, so the target element
    # inner HTML is simply deleted. That&#x27;s why the deleted todo is removed from the list.
    return clr_details()

@rt(&quot;/edit/{id}&quot;)
async def get(id:int):
    # The `hx_put` attribute tells HTMX to send a PUT request when the form is submitted.
    # `target_id` specifies which element will be updated with the server&#x27;s response.
    res = Form(Group(Input(id=&quot;title&quot;), Button(&quot;Save&quot;)),
        Hidden(id=&quot;id&quot;), CheckboxX(id=&quot;done&quot;, label=&#x27;Done&#x27;),
        Textarea(id=&quot;details&quot;, name=&quot;details&quot;, rows=10),
        hx_put=&quot;/&quot;, target_id=f&#x27;todo-{id}&#x27;, id=&quot;edit&quot;)
    # `fill_form` populates the form with existing todo data, and returns the result.
    # Indexing into a table (`todos`) queries by primary key, which is `id` here. It also includes
    # `xtra`, so this will only return the id if it belongs to the current user.
    return fill_form(res, todos[id])

@rt(&quot;/&quot;)
async def put(todo: Todo):
    # `update` is part of the MiniDataAPI spec.
    # Note that the updated todo is returned. By returning the updated todo, we can update the list directly.
    # Because we return a tuple with `clr_details()`, the details view is also cleared.
    return todos.update(todo), clr_details()

@rt(&quot;/&quot;)
async def post(todo:Todo):
    # `hx_swap_oob=&#x27;true&#x27;` tells HTMX to perform an out-of-band swap, updating this element wherever it appears.
    # This is used to clear the input field after adding the new todo.
    new_inp =  Input(id=&quot;new-title&quot;, name=&quot;title&quot;, placeholder=&quot;New Todo&quot;, hx_swap_oob=&#x27;true&#x27;)
    # `insert` returns the inserted todo, which is appended to the start of the list, because we used
    # `hx_swap=&#x27;afterbegin&#x27;` when creating the todo list form.
    return todos.insert(todo), new_inp

@rt(&quot;/todos/{id}&quot;)
async def get(id:int):
    todo = todos[id]
    # `hx_swap` determines how the update should occur. We use &quot;outerHTML&quot; to replace the entire todo `Li` element.
    btn = Button(&#x27;delete&#x27;, hx_delete=f&#x27;/todos/{todo.id}&#x27;,
                 target_id=f&#x27;todo-{todo.id}&#x27;, hx_swap=&quot;outerHTML&quot;)
    # The &quot;markdown&quot; class is used here because that&#x27;s the CSS selector we used in the JS earlier.
    # Therefore this will trigger the JS to parse the markdown in the details field.
    # Because `class` is a reserved keyword in Python, we use `cls` instead, which FastHTML auto-converts.
    return Div(H2(todo.title), Div(todo.details, cls=&quot;markdown&quot;), btn)

serve()</doc>
  </examples>
</project>
"""
