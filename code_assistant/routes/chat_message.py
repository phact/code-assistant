from code_assistant.app import *

# Route that gets polled while streaming
async def page(request, msg_idx: int):
    if msg_idx >= len(request.state.messages): return ""
    return ChatMessage(request.app.state.messages, msg_idx)