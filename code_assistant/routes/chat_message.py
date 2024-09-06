from code_assistant.app import *

# Route that gets polled while streaming
async def page(request, msg_idx: int):
    if not hasattr(request.app.state, 'messages'):
        return Script("window.location.href = '/';")
    if msg_idx >= len(request.app.state.messages): return ""
    return ChatMessage(request.app.state.messages, msg_idx)