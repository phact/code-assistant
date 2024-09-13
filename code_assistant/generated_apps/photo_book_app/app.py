from fasthtml.common import *

app = FastHTML()
rt = app.route

photos = [
    {"description": "A beautiful sunrise over the mountains."},
    {"description": "A tranquil beach scene with crystal clear water."},
    {"description": "An urban skyline at dusk."}
]

current_photo_index = 0

def render_photo():
    global current_photo_index
    photo = photos[current_photo_index]
    photo_url = f"https://pollinations.ai/p/{photo['description'].replace(' ', '%20')}?model=flux"
    return Div(
        Img(src=photo_url, alt="Photo", style="display:block; margin:auto; max-width: 80%;"),
        P(photo["description"], style="text-align:center;"),
        id="photoSection",
        hx_swap="innerHTML"
    )

@rt('/')
def photo_book():
    return Div(
        H1('Photo Book', style="text-align:center; color: darkblue;"),
        render_photo(),
        Div(
            Button('Previous', hx_post='/prev', hx_trigger='click', hx_target="#photoSection", style="margin-right: 20px;"),
            Button('Next', hx_post='/next', hx_trigger='click', hx_target="#photoSection"),
            style="text-align:center;",
        ),
        style="max-width: 800px; margin: auto;"
    )

@rt('/next')
def next_photo():
    global current_photo_index
    current_photo_index = (current_photo_index + 1) % len(photos)
    return render_photo()

@rt('/prev')
def prev_photo():
    global current_photo_index
    current_photo_index = (current_photo_index - 1) % len(photos)
    return render_photo()

serve()