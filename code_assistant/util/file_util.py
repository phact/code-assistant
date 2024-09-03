import html
import importlib
import inspect
import json
import traceback
from importlib import import_module

from ast_grep_py import SgRoot
from fasthtml import RouteX
from fasthtml.common import Script
from fasthtml.core import FastHTML
import starlette.middleware.errors as errors_module
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Mount
from tree_sitter import Language, Parser
import tree_sitter_python as tspython

from code_assistant.util.error_app import get_error_app

def format_line(
        self, index: int, line: str, frame_lineno: int, frame_index: int
) -> str:
    values = {
        # HTML escape - line could contain < or >
        "line": html.escape(line).replace(" ", "&nbsp"),
        "lineno": (frame_lineno - frame_index) + index,
    }

    if index != frame_index:
        return errors_module.LINE.format(**values)
    return errors_module.CENTER_LINE.format(**values)

def generate_frame_html(frame: inspect.FrameInfo, is_collapsed: bool) -> str:
    code_context = "".join(
        format_line(
            index,
            line,
            frame.lineno,
            frame.index,  # type: ignore[arg-type]
        )
        for index, line in enumerate(frame.code_context or [])
    )

    values = {
        # HTML escape - filename could contain < or >, especially if it's a virtual
        # file e.g. <stdin> in the REPL
        "frame_filename": html.escape(frame.filename),
        "frame_lineno": frame.lineno,
        # HTML escape - if you try very hard it's possible to name a function with <
        # or >
        "frame_name": html.escape(frame.function),
        "code_context": code_context,
        "collapsed": "collapsed" if is_collapsed else "",
        "collapse_button": "+" if is_collapsed else "&#8210;",
    }
    return errors_module.FRAME_TEMPLATE.format(**values)


def generate_html(exc: Exception, content: str, limit: int = 7) -> str:
    traceback_obj = traceback.TracebackException.from_exception(
        exc, capture_locals=True
    )

    exc_html = ""
    is_collapsed = False
    exc_traceback = exc.__traceback__
    if exc_traceback is not None:
        frames = inspect.getinnerframes(exc_traceback, limit)
        for frame in reversed(frames):
            exc_html += generate_frame_html(frame, is_collapsed)
            is_collapsed = True

    # escape error class and text
    error = (
        f"{html.escape(traceback_obj.exc_type.__name__)}: "
        f"{html.escape(str(traceback_obj))}"
    )

    return errors_module.TEMPLATE.format(styles=errors_module.STYLES, js=custom_js_script(content), error=error, exc_html=exc_html)

def script_with_path(path: str):
    prefix_id = path.replace('/', '').replace('.', '')
    script = Script(f"""
  let {prefix_id}_basePrefix = '{path}';

  function add_listener(){{
    // Listener for the HTMX config request event
    document.body.addEventListener("htmx:configRequest", function(event) {{
      const path = event.detail.path;

      // Ensure the path is correctly prefixed with the base URL
      if (!path.startsWith({prefix_id}_basePrefix)) {{
        event.detail.path = `${{{prefix_id}_basePrefix}}${{path}}`;
      }}
    }});

    // Modify all anchor hrefs that start with '/' to include the basePrefix
    document.querySelectorAll('a[href^="/"]').forEach(anchor => {{
      let href = anchor.getAttribute('href');
      if (!href.startsWith({prefix_id}_basePrefix)) {{
        anchor.setAttribute('href', `${{{prefix_id}_basePrefix}}${{href}}`);
      }}
    }});
    
    const originalFetch = window.fetch;
    window.fetch = function(input, init) {{
      if (typeof input === 'string') {{
        if (!input.startsWith({prefix_id}_basePrefix)) {{
          input = `${{{prefix_id}_basePrefix}}${{input}}`;
        }}
      }} else if (input instanceof Request) {{
        if (!input.url.startsWith({prefix_id}_basePrefix)) {{
          input = new Request(`${{{prefix_id}_basePrefix}}${{input.url}}`, input);
        }}
      }}
      return originalFetch(input, init);
    }}
  }};
  
  document.addEventListener("DOMContentLoaded", function() {{
    add_listener();
  }});
  
  function postMessageToParent(error_message){{
    // send postMessage to the parent
    var payload = {{
        type: 'showMessage',
        content: {{
            'error_message': error_message,
            'filename': '{prefix_id}.py', // TODO handle other filetypes
        }}
    }};
    window.parent.postMessage(payload, '*');
  }}
  
  
 
  
  // Handles javascript errors for self healing
  window.onerror = function(message, source, lineno, colno, error) {{
    console.error('Error message:', message);
    console.error('Source:', source);
    console.error('Line:', lineno);
    console.error('Column:', colno);
    console.error('Error object:', error);

    let error_message = 'Error message: ' + message + '\\nSource: ' + source + '\\nLine: ' + lineno + '\\nColumn: ' + colno + '\\nError object: ' + error;
    postMessageToParent(error_message);

  }};
  
  window.addEventListener('unhandledrejection', function(event) {{
    console.error('Unhandled Rejection: ', event.reason);
    debugger
    postMessageToParent('Error message: ' + event.reason);
  }});
  
 

""")

    return script

def get_post_message_script(content):
    post_message_script = f"""
        // send postMessage to the parent
        var payload = {{
            type: 'showMessage',
            content: {content}
        }};
        window.parent.postMessage(payload, '*');
    """
    return post_message_script


def custom_js_script(content: str = '\'\''):
    post_message_script = get_post_message_script(content)
    CUSTOM_JS = f"""
    <script type="text/javascript">
        function collapse(element){{
            const frameId = element.getAttribute("data-frame-id");
            const frame = document.getElementById(frameId);

            if (frame.classList.contains("collapsed")){{
                element.innerHTML = "&#8210;";
                frame.classList.remove("collapsed");
            }} else {{
                element.innerHTML = "+";
                frame.classList.add("collapsed");
            }}
        }}
        
        {post_message_script}
    </script>
    """
    return CUSTOM_JS


class CustomServerErrorMiddleware(errors_module.ServerErrorMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        try:
            response = await self.app(scope, receive, send)
            await response(scope, receive, send)
        except Exception as exc:
            filename = str(request.url).split(str(request.base_url))[1].split("/")[0] + ".py"
            content = json.dumps({"error_message": str(exc), "filename": filename})
            errors_module.JS = custom_js_script(content)
            response = super().debug_response(request, exc)

            response.headers["HX-Trigger"] = "showMessage"

            # We always continue to raise the exception.
            # This allows servers to log the error, or allows test clients
            # to optionally raise the error within the test case.
            raise exc


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            if hasattr(response, "status_code") and response.status_code >= 400 and response.status_code < 600:
                filename = str(request.url).split(str(request.base_url))[1].split("/")[0] + ".py"
                # TODO figure out how to get the actual error
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk

                # Optionally decode or process the body
                body_text = body.decode('utf-8')
                content = json.dumps({"error_message": f"Error code {response.status_code}, {body_text}", "filename": filename})
                errors_module.JS = custom_js_script(content)
                path = str(request.url).split(str(request.base_url)+filename.split(".py")[0])[1]
                html_content = generate_html(Exception(f"Error code {response.status_code}, {body_text}, for path: '{path}'"), content)
                response.headers["HX-Trigger"] = "showMessage"
                return HTMLResponse(html_content, status_code=response.status_code)
            return response
        except Exception as exc:
            trace = traceback.format_exc()
            print(trace)
            raise exc


def get_mount_from_file(filename, program_id=None):
    if program_id is None:
        program_id = filename
    filename = filename.split('.')[0]
    print(f"loading filename: {filename}")
    app = None
    try:
        with open(f'code_assistant/generated_apps/{filename}.py') as f:
            code = f.read()
            # TODO: required libraries will be configurable
            assert is_library_used(code, 'fasthtml'), "The app does not use fasthtml library."
            assert serve_attr_check(code), "serve() function should not have any attributes."
            assert (code), "serve() function should not have any attributes."

        module = import_module(f'code_assistant.generated_apps.{filename}')
        importlib.reload(module)
        app = module.app
        app.debug = True
        app.add_middleware(CustomServerErrorMiddleware)
        app.add_middleware(ErrorHandlingMiddleware)

        mount = Mount(
            f"/{filename}",
            app,
        )
        assert isinstance(mount.app,
                          FastHTML), "The app is not a FastHTML app. Always use `from fasthtml.common import *`"
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        content = json.dumps({"error_message": str(e), "filename": filename, "program_id": program_id})
        app = get_error_app(filename, str(e), trace, program_id, get_post_message_script(content))
        mount = Mount(
            path=f"/{filename}",
            app=app
        )
    script = None
    for route in mount.routes:
        # route.hdrs.insert(0, script_with_path(f'/{filename}'))
        script = script_with_path(f'/{filename}')
        #if not isinstance(route, RouteX):
        #    route = RouteX(
        #        path=route.path,
        #        endpoint=route.endpoint,
        #        methods=route.methods,
        #        name=route.name,
        #        include_in_schema=route.include_in_schema,
        #        hdrs=[script, ],
        #    )
        #else:
        #    route.hdrs.append(script)
        break
    if app is not None and script is not None:
        app.hdrs.append(script)
        print(f"loaded filename: {filename}")
        return mount
    else:
        raise Exception("This is a bug, should not happen")


ts_language = Language(tspython.language())
parser = Parser(ts_language)


def serve_attr_check(code):
    root = SgRoot(code, "python")
    node = root.root()
    #serve_calls = node.find_all(pattern="serve($$$ARGS)")
    serve_calls = node.find_all({
        "rule": {
            "pattern": "serve($$$A)",
        },
        "constraints": {
            "A": { "regex": "no match" }
        }
    })
    non_empty_calls = []
    for call in serve_calls:
        if call.text() != "serve()":
            non_empty_calls.append(call)

    if len(non_empty_calls) == 0:
        return True
    else:
        return False

def is_library_used(code, library_name):
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node

    for child in root_node.children:
        if child.type == "import_statement":
            for grandchild in child.named_children:
                if grandchild.text.decode("utf8") == library_name:
                    return True
        elif child.type == "import_from_statement":
            for grandchild in child.children:
                if grandchild.type == "dotted_name":
                    module_name = grandchild.text.decode("utf8")
                    if library_name in module_name:
                        return True
    return False
