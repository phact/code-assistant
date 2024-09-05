import os
import uvicorn


if __name__ == "__main__":
    port=int(os.getenv("PORT", default=5001))
    host="0.0.0.0"
    print(f'Link: http://{"localhost" if host=="0.0.0.0" else host}:{port}')
    uvicorn.run(f'code_assistant.main:app', host=host, port=port, reload=True, reload_excludes="./generated_apps/*")