small_fasthtml_context = """
## Objective: 
Build a FastHTML app. 

## FastHTML Basics:

FastHTML is a NEW python web application framework, NOT TO BE CONFUSED WITH FASTAPI.

Here's a very basic, fully functional hello world which we'll break down:

```python
from fasthtml.common import *

app = FastHTML()
rt = app.route


@rt('/')
def get():
    return Div('Hello, World!')

serve()
```

### Application Setup:

Initialize a FastHTML app using app = FastHTML(hdrs=(picolink, css)).
Define routes using a shorthand 


```
rt = app.route

@rt('/')
def get():
    ...
```

### HTMX

FastHTML uses htmx for dynamic content updates. Aim to use HTMX for dynamic content updates and avoid using JS for DOM manipulation.

### Function Naming and Routes:

To crate routes always define HTTP method functions with the name of the HTTP method (get, post) and
Use @app.route('/') to apply routes, handling HTTP GET requests for rendering pages.

Always create a route for the root path ('/') to serve the main page of the app. 
If the app isn't loading properly check the route for the root path and  ensure it returns an FT with valid syntax.

```
rt = app.route

@rt('/')
def get():
    return Div('Hello, World!') # Note the div will automatically get converted to HTML and will be placed inside the body tag
    ...

@rt('/other-endpoint')
def post():
    ...
```
    
or alternatively using the app.get, app.post decorators:

```
@app.post('/vehicle/')
def select_vehicle(choice: str):
    ...
```
### HTML Structure:

FastHTML uses FastTags (known as FTs) these are python representations of HTML elements (e.g., Div, Button, Span). IMPORTANT, only the first letter is capitalized (i.e. use Hr, Tr, Th, etc not HR, TR, TH).

Here are all the available tags:

['Html', 'Safe', 'Head', 'Title', 'Meta' ,'Link', 'Style', 'Body', 'Pre', 'Code', 'Div', 'Span', 'P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Strong',
           'Em', 'B', 'I', 'U', 'S', 'Strike', 'Sub', 'Sup', 'Hr', 'Br', 'Img', 'A', 'Nav', 'Ul', 'Ol', 'Li', 'Dl',
           'Dt', 'Dd', 'Table', 'Thead', 'Tbody', 'Tfoot', 'Tr', 'Th', 'Td', 'Caption', 'Col', 'Colgroup', 'Form',
           'Input', 'Textarea', 'Button', 'Select', 'Option', 'Label', 'Fieldset', 'Legend', 'Details', 'Summary',
           'Main', 'Header', 'Footer', 'Section', 'Article', 'Aside', 'Figure', 'Figcaption', 'Mark', 'Small', 'Iframe',
           'Object', 'Embed', 'Param', 'Video', 'Audio', 'Source', 'Canvas', 'Svg', 'Math', 'Script', 'Noscript',
           'Template', 'Slot']

The various tags live in fasthtml.common and are imported using:

    from fasthtml.common import *

Always import * from fasthtml.common rather than doing individual imports

HTML attributes can be set using named python arguments. For example, to set the class attribute of a Div element:

Div(cls='my-class')

You can nest FastTags inside each other using positional python arguments in order to create complex HTML structures. 

Remember to include positional arguments (i.e. other FTs) before you include any keyword arguments (i.e. attrs).
 
The following example is incorrect:

    return Div(cls='my-class', Div('inner div')) 

It will return following runtime error: `positional argument follows keyword argument`


    return Div(Div('inner div'), cls='my-class')

Use semantic elements like Nav, Header, Form, Section to organize content.

Ensure that children elements are passed as positional arguments to parent tags:

Correct:

    Div(P('hello world'))

Incorrect:

    Div(children=['P('hello world')'])  # FT's do **not** take a children keyword argument


## Style and Script

You can include CSS and JS in your FastHTML app using the Style and Script FTs. This includes adding js libraries using a CDN.

for example:

```python
threejs = Script(src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"),
style = Style('body { background-color: lightblue; }')
script = Script('''
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
camera.position.z = 4;

var renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setClearColor("#000000");
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

var geometry = new THREE.BoxGeometry( 1, 1, 1 );
var material = new THREE.MeshBasicMaterial( { color: "#433F81" } );
var cube = new THREE.Mesh( geometry, material );
scene.add( cube );

var render = function () {
  requestAnimationFrame( render );

  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;

  renderer.render(scene, camera);
};

render();
''')

app = FastHTML(hdrs=(style, script))
```

IMPORANT Style and Script take a string as their first argument, which is the content of the style or script tag.
and the scripts need to go in hdrs=(...) in the FastHTML constructor.

## Request Parameters

When you specify arguments to a route, FastHTML will search the request for values with the same name, and convert them to the correct type. 
IMPORTANT you must use type hints for these arguments.

In order, it searches:
 - The path parameters
 - The query parameters
 - The cookies
 - The headers
 - The session
 - Form data
 
There are also a few special arguments:
 - request (or any prefix like req): gets the raw Starlette Request object
 - session (or any prefix like sess): gets the session object
 - auth
 - htmx
 - app
In this section let’s quickly look at some of these in action.

### Path Parameters:
When passing path parameters to a route, use the same name as the parameter in the path and always use type hints.

For example, this route:
```
@app.post('/thing/{id}')
def select_vehicle(id: str): # NOTICE the type hint for id, this is required or the variable will be set to None
    ...
```

Will accept the request made by the HTML generated by this FT:

```
Button(cls='btn', hx_post=f'/thing/my_thing_id', hx_swap="none")
```

### Query Parameters:
When passing query parameters to a route, make sure your parameter names match and always use type hints.

For example, this route:
```
@app.post('/thing')
def select_vehicle(id: str): # NOTICE the type hint for id, this is required or the variable will be set to None
    ...
```

Will accept the request made by the HTML generated by this FT:

```
Button(cls='btn', hx_post=f'/thing_id?id=my_thing_id', hx_swap="none")
```

### Body Parameters:

For POST routes you can also use body parameters but you must use a Form in the html.

You can use starlette request object to get the form data.

For example when submitting the following form (FT):

```
Form(Input(id='id', type='text'), Button('Submit'), hx_post='/thing_id')
```

Extract the values from the request object in the route function:

```
@app.post('/thing_id')
def select_vehicle(request): # NOTICE the type hint for id, this is required or the variable will be set to None
    form_obj = await request.form()
    id = form_obj['id']
    print(f'the id is {id}')
    ...
```


Alternatively (this shorthand is preffered), you can specify the variable name AND TYPE HINT in the route function arguments and FastHTML will automatically extract the values.

```
@app.post('/thing_id')
def select_vehicle(id: str): # NOTICE the type hint for id, this is required or the variable will be set to None
    print(f'the id is {id}')
    ...
```

Remember, the id attribute of the input tag(s) must match the parameter name(s) in the route.

### With inputs, checkboxes, or radio buttons

Note, to get the values of inputs you must put them in a Form with the Button that triggers the request and make sure the id of the input matches the parameter name in the route.


```
@rt("/context")
async def get(option_one: str = None, option_two: str = None, option_three: str = None): # NOTICE the type hints these are required or the variables will be set to None
    if option_one == 'on':
        ...
```


```
    Form(
        Div(
            Label(
                "Option One",
                Input(
                    id="option_one",
                    name="option_one",
                    type="checkbox",
                    checked=False
                ),
                for_="option_one"
            ),
            Label(
                "Option Two",
                Input(
                    id="option_two",
                    name="option_two",
                    type="checkbox",
                    checked=True
                ),
                for_="option_two"
            ),
            ...
            ),
        ),
        hx_trigger="change", hx_encoding='multipart/form-data', hx_get='/context', hx_swap="none",
    ),
```


### Static Files:

FastHTML uses starlette's path syntax, and adds a `static` type which matches standard static file extensions.
This means that FastHTML will by default serve static files from the directory from which the app is run.


### Serving the Application:

Use serve() with no arguments to start the application server directly, without conditionals or arguments. 
serve is a function that can be imported from FastHTML.common. It does not take any arguments. It is not a method of the FastHTML class.

## A Minimal Charting Application

The [`Script`](https://AnswerDotAI.github.io/fasthtml/api/xtend.html#script)
function allows you to include JavaScript. You can use Python to
generate parts of your JS or JSON like this:

``` python
import json
from fasthtml.common import * 

app, rt = fast_app(hdrs=(Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),))

data = json.dumps({
    "data": [{"x": [1, 2, 3, 4],"type": "scatter"},
            {"x": [1, 2, 3, 4],"y": [16, 5, 11, 9],"type": "scatter"}],
    "title": "Plotly chart in FastHTML ",
    "description": "This is a demo dashboard",
    "type": "scatter"
})


@rt("/")
def get():
  return Titled("Chart Demo", Div(id="myDiv"),
    Script(f"var data = {data}; Plotly.newPlot('myDiv', data);"))

serve()
```

### Common Errors to Avoid:

Ensure all parentheses are properly matched.
Use cls= instead of _class= for applying CSS classes. Multiple classes can be assigned in a single argument cls="class1 class2"

Import necessary modules correctly and avoid redundancy in code.

Make sure to properly use " and ' in fstrings i.e. f"{dict['puppies']}" is correct. f'{dict['puppies']}' is incorrect.

Example app:

###
# Walkthough of an idiomatic fasthtml app
###

# This fasthtml app includes functionality from fastcore, starlette, fastlite, and fasthtml itself.
# Run with: `python adv_app.py`
# Importing * from `fasthtml.common` brings the key parts of all of these together.
# For simplicity, you can just `from fasthtml.common import *`:
#Some useful functions and classes in fasthtml.common include:
# -  Most HTML components including: 
#A, AX, Button, Card, Checkbox, Container, Div, Form, Grid, Group, H1, H2, Hidden, Input, Li, Main, Script, Style, Textarea, Title, Titled, Ul,
# - Some are FastHTML symbols:
#    Beforeware, fast_app, SortableJS, fill_form, picolink, serve,
#Other useful simbols for Fast HTML Apps include things from Starlette, Fastlite, fastcore, and the Python stdlib:
#    FileResponse, NotFoundError, RedirectResponse, database, patch, dataclass
from fasthtml.common import *
from hmac import compare_digest

# You can use any database you want; it'll be easier if you pick a lib that supports the MiniDataAPI spec.
# Here we are using SQLite, with the FastLite library, which supports the MiniDataAPI spec.
db = database('data/utodos.db')
# The `t` attribute is the table collection. The `todos` and `users` tables are not created if they don't exist.
# Instead, you can use the `create` method to create them if needed.
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    # You can pass a dict, or kwargs, to most MiniDataAPI methods.
    users.create(dict(name=str, pwd=str), pk='name')
    todos.create(id=int, title=str, done=bool, name=str, details=str, priority=int, pk='id')
# Although you can just use dicts, it can be helpful to have types for your DB objects.
# The `dataclass` method creates that type, and stores it in the object, so it will use it for any returned items.
Todo,User = todos.dataclass(),users.dataclass()

# Any Starlette response class can be returned by a FastHTML route handler.
# In that case, FastHTML won't change it at all.
# Status code 303 is a redirect that can change POST to GET, so it's appropriate for a login page.
login_redir = RedirectResponse('/login', status_code=303)

# The `before` function is a *Beforeware* function. These are functions that run before a route handler is called.
def before(req, sess):
    # This sets the `auth` attribute in the request scope, and gets it from the session.
    # The session is a Starlette session, which is a dict-like object which is cryptographically signed,
    # so it can't be tampered with.
    # The `auth` key in the scope is automatically provided to any handler which requests it, and can not
    # be injected by the user using query params, cookies, etc, so it should be secure to use.
    auth = req.scope['auth'] = sess.get('auth', None)
    # If the session key is not there, it redirects to the login page.
    if not auth: return login_redir
    # `xtra` is part of the MiniDataAPI spec. It adds a filter to queries and DDL statements,
    # to ensure that the user can only see/edit their own todos.
    todos.xtra(name=auth)

markdown_js = \"\"\"
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import { proc_htmx} from "https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js/fasthtml.js";
proc_htmx('.markdown', e => e.innerHTML = marked.parse(e.textContent));
\"\"\"

# We will use this in our `exception_handlers` dict
def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :('))

# To create a Beforeware object, we pass the function itself, and optionally a list of regexes to skip.
bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])
# The `FastHTML` class is a subclass of `Starlette`, so you can use any parameters that `Starlette` accepts.
# In addition, you can add your Beforeware here, and any headers you want included in HTML responses.
# FastHTML includes the "HTMX" and "Surreal" libraries in headers, unless you pass `default_hdrs=False`.
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
                     Style(':root { --pico-font-size: 100%; }'),
                     # Have a look at fasthtml/js.py to see how these Javascript libraries are added to FastHTML.
                     # They are only 5-10 lines of code each, and you can add your own too.
                     SortableJS('.sortable'),
                     # MarkdownJS is actually provided as part of FastHTML, but we've included the js code here
                     # so that you can see how it works.
                     Script(markdown_js, type='module'))
                )
# We add `rt` as a shortcut for `app.route`, which is what we'll use to decorate our route handlers.
# When using `app.route` (or this shortcut), the only required argument is the path.
# The name of the decorated function (eg `get`, `post`, etc) is used as the HTTP verb for the handler.
rt = app.route

# For instance, this function handles GET requests to the `/login` path.
@rt("/login")
def get():
    # This creates a form with two input fields, and a submit button.
    # All of these components are `FT` objects. All HTML tags are provided in this form by FastHTML.
    # If you want other custom tags (e.g. `MyTag`), they can be auto-generated by e.g
    # `from fasthtml.common import MyTag`.
    # Alternatively, manually call e.g `ft(tag_name, *children, **attrs)`.
    frm = Form(
        # Tags with a `name` attr will have `name` auto-set to the same as `id` if not provided
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'),
        action='/login', method='post')
    # If a user visits the URL directly, FastHTML auto-generates a full HTML page.
    # However, if the URL is accessed by HTMX, then one HTML partial is created for each element of the tuple.
    # To avoid this auto-generation of a full page, return a `HTML` object, or a Starlette `Response`.
    # `Titled` returns a tuple of a `Title` with the first arg and a `Container` with the rest.
    # See the comments for `Title` later for details.
    return Titled("Login", frm)

# Handlers are passed whatever information they "request" in the URL, as keyword arguments.
# Dataclasses, dicts, namedtuples, TypedDicts, and custom classes are automatically instantiated
# from form data.
# In this case, the `Login` class is a dataclass, so the handler will be passed `name` and `pwd`.
@dataclass
class Login: name:str; pwd:str

# This handler is called when a POST request is made to the `/login` path.
# The `login` argument is an instance of the `Login` class, which has been auto-instantiated from the form data.
# There are a number of special parameter names, which will be passed useful information about the request:
# `session`: the Starlette session; `request`: the Starlette request; `auth`: the value of `scope['auth']`,
# `htmx`: the HTMX headers, if any; `app`: the FastHTML app object.
# You can also pass any string prefix of `request` or `session`.
@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    # Indexing into a MiniDataAPI table queries by primary key, which is `name` here.
    # It returns a dataclass object, if `dataclass()` has been called at some point, or a dict otherwise.
    try: u = users[login.name]
    # If the primary key does not exist, the method raises a `NotFoundError`.
    # Here we use this to just generate a user -- in practice you'd probably to redirect to a signup page.
    except NotFoundError: u = users.insert(login)
    # This compares the passwords using a constant time string comparison
    # https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    # Because the session is signed, we can securely add information to it. It's stored in the browser cookies.
    # If you don't pass a secret signing key to `FastHTML`, it will auto-generate one and store it in a file `./sesskey`.
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

# Instead of using `app.route` (or the `rt` shortcut), you can also use `app.get`, `app.post`, etc.
# In this case, the function name is not used to determine the HTTP verb.
@app.get("/logout")
def logout(sess):
    del sess['auth']
    return login_redir

# FastHTML uses Starlette's path syntax, and adds a `static` type which matches standard static file extensions.
# You can define your own regex path specifiers -- for instance this is how `static` is defined in FastHTML
# `reg_re_param("static", "ico|gif|jpg|jpeg|webm|css|js|woff|png|svg|mp4|webp|ttf|otf|eot|woff2|txt|xml|html")`
# In this app, we only actually have one static file, which is `favicon.ico`. But it would also be needed if
# we were referencing images, CSS/JS files, etc.
# Note, this function is unnecessary, as the `fast_app()` call already includes this functionality.
# However, it's included here to show how you can define your own static file handler.
@rt("/{fname:path}.{ext:static}")
async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# The `patch` decorator, which is defined in `fastcore`, adds a method to an existing class.
# Here we are adding a method to the `Todo` class, which is returned by the `todos` table.
# The `__ft__` method is a special method that FastHTML uses to convert the object into an `FT` object,
# so that it can be composed into an FT tree, and later rendered into HTML.
@patch
def __ft__(self:Todo):
    # Some FastHTML tags have an 'X' suffix, which means they're "extended" in some way.
    # For instance, here `AX` is an extended `A` tag, which takes 3 positional arguments:
    # `(text, hx_get, target_id)`.
    # All underscores in FT attrs are replaced with hyphens, so this will create an `hx-get` attr,
    # which HTMX uses to trigger a GET request.
    # Generally, most of your route handlers in practice (as in this demo app) are likely to be HTMX handlers.
    # For instance, for this demo, we only have two full-page handlers: the '/login' and '/' GET handlers.
    show = AX(self.title, f'/todos/{self.id}', 'current-todo')
    edit = AX('edit',     f'/edit/{self.id}' , 'current-todo')
    dt = '✅ ' if self.done else ''
    # FastHTML provides some shortcuts. For instance, `Hidden` is defined as simply:
    # `return Input(type="hidden", value=value, **kwargs)`
    cts = (dt, show, ' | ', edit, Hidden(id="id", value=self.id), Hidden(id="priority", value="0"))
    # Any FT object can take a list of children as positional args, and a dict of attrs as keyword args.
    return Li(*cts, id=f'todo-{self.id}')

# This is the handler for the main todo list application.
# By including the `auth` parameter, it gets passed the current username, for displaying in the title.
@rt("/")
def get(auth):
    title = f"{auth}'s Todo list"
    top = Grid(H1(title), Div(A('logout', href='/logout'), style='text-align: right'))
    # We don't normally need separate "screens" for adding or editing data. Here for instance,
    # we're using an `hx-post` to add a new todo, which is added to the start of the list (using 'afterbegin').
    new_inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(new_inp, Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="afterbegin")
    # In the MiniDataAPI spec, treating a table as a callable (i.e with `todos(...)` here) queries the table.
    # Because we called `xtra` in our Beforeware, this queries the todos for the current user only.
    # We can include the todo objects directly as children of the `Form`, because the `Todo` class has `__ft__` defined.
    # This is automatically called by FastHTML to convert the `Todo` objects into `FT` objects when needed.
    # The reason we put the todo list inside a form is so that we can use the 'sortable' js library to reorder them.
    # That library calls the js `end` event when dragging is complete, so our trigger here causes our `/reorder`
    # handler to be called.
    frm = Form(*todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post="/reorder", hx_trigger="end")
    # We create an empty 'current-todo' Div at the bottom of our page, as a target for the details and editing views.
    card = Card(Ul(frm), header=add, footer=Div(id='current-todo'))
    # PicoCSS uses `<Main class='container'>` page content; `Container` is a tiny function that generates that.
    # A handler can return either a single `FT` object or string, or a tuple of them.
    # In the case of a tuple, the stringified objects are concatenated and returned to the browser.
    # The `Title` tag has a special purpose: it sets the title of the page.
    return Title(title), Container(top, card)

# This is the handler for the reordering of todos.
# It's a POST request, which is used by the 'sortable' js library.
# Because the todo list form created earlier included hidden inputs with the todo IDs,
# they are passed as form data. By using a parameter called (e.g) "id", FastHTML will try to find
# something suitable in the request with this name. In order, it searches as follows:
# path; query; cookies; headers; session keys; form data.
# Although all these are provided in the request as strings, FastHTML will use your parameter's type
# annotation to try to cast the value to the requested type.
# In the case of form data, there can be multiple values with the same key. So in this case,
# the parameter is a list of ints.
@rt("/reorder")
def post(id:list[int]):
    for i,id_ in enumerate(id): todos.update({'priority':i}, id_)
    # HTMX by default replaces the inner HTML of the calling element, which in this case is the todo list form.
    # Therefore, we return the list of todos, now in the correct order, which will be auto-converted to FT for us.
    # In this case, it's not strictly necessary, because sortable.js has already reorder the DOM elements.
    # However, by returning the updated data, we can be assured that there aren't sync issues between the DOM
    # and the server.
    return tuple(todos(order_by='priority'))

# Refactoring components in FastHTML is as simple as creating Python functions.
# The `clr_details` function creates a Div with specific HTMX attributes.
# `hx_swap_oob='innerHTML'` tells HTMX to swap the inner HTML of the target element out-of-band,
# meaning it will update this element regardless of where the HTMX request originated from.
def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

# This route handler uses a path parameter `{id}` which is automatically parsed and passed as an int.
@rt("/todos/{id}")
def delete(id:int):
    # The `delete` method is part of the MiniDataAPI spec, removing the item with the given primary key.
    todos.delete(id)
    # Returning `clr_details()` ensures the details view is cleared after deletion,
    # leveraging HTMX's out-of-band swap feature.
    # Note that we are not returning *any* FT component that doesn't have an "OOB" swap, so the target element
    # inner HTML is simply deleted. That's why the deleted todo is removed from the list.
    return clr_details()

@rt("/edit/{id}")
async def get(id:int):
    # The `hx_put` attribute tells HTMX to send a PUT request when the form is submitted.
    # `target_id` specifies which element will be updated with the server's response.
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        Textarea(id="details", name="details", rows=10),
        hx_put="/", target_id=f'todo-{id}', id="edit")
    # `fill_form` populates the form with existing todo data, and returns the result.
    # Indexing into a table (`todos`) queries by primary key, which is `id` here. It also includes
    # `xtra`, so this will only return the id if it belongs to the current user.
    return fill_form(res, todos[id])

@rt("/")
async def put(todo: Todo):
    # `update` is part of the MiniDataAPI spec.
    # Note that the updated todo is returned. By returning the updated todo, we can update the list directly.
    # Because we return a tuple with `clr_details()`, the details view is also cleared.
    return todos.update(todo), clr_details()

@rt("/")
async def post(todo:Todo):
    # `hx_swap_oob='true'` tells HTMX to perform an out-of-band swap, updating this element wherever it appears.
    # This is used to clear the input field after adding the new todo.
    new_inp =  Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')
    # `insert` returns the inserted todo, which is appended to the start of the list, because we used
    # `hx_swap='afterbegin'` when creating the todo list form.
    return todos.insert(todo), new_inp

@rt("/todos/{id}")
async def get(id:int):
    todo = todos[id]
    # `hx_swap` determines how the update should occur. We use "outerHTML" to replace the entire todo `Li` element.
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=f'todo-{todo.id}', hx_swap="outerHTML")
    # The "markdown" class is used here because that's the CSS selector we used in the JS earlier.
    # Therefore this will trigger the JS to parse the markdown in the details field.
    # Because `class` is a reserved keyword in Python, we use `cls` instead, which FastHTML auto-converts.
    return Div(H2(todo.title), Div(todo.details, cls="markdown"), btn)

serve()
"""
