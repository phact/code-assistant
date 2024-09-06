# code-assistant

A FastHTML app that makes FastHTML apps.

## Features and Roadmap:

### Guiding the LLM
 - [X] LSP support (code actions)
 - [X] LSP support (retrieve diagnostics)
 - [X] LSP Support (linter/formatter with `ruff server`)
 - [ ] LSP Support (type checker, use pyright or wait for ruff red-knot? https://github.com/astral-sh/ruff/issues/12701)
 - [ ] LSP support (use diagnostics in LLM context)
 - [X] Self-healing (backend runtime errors)
 - [X] Self-healing (frontend runtime errors)
 - [X] python indentation helper with tree sitter
 - [X] FastHTML specific validations using ast-grep
 - [X] FastHTML documentation llm context
 - [X] HTMX documentation llm context
 - [ ] fastlite documentation llm context
 - [ ] fastsql documentation llm context
 - [ ] fastastra documentation llm context
 - [ ] dynamic openapi spec llm context
 - [ ] dynamic sample apps llm context
 - [ ] astra-assistants documentation llm context
 - [ ] Multi-file support
 - [ ] Multi-turn generation

### UI/UX
 - [X] Live app preview
 - [X] Drive generated_apps dir with env var CA_GENERATED_APPS_DIR
 - [X] Add third party model support to frontend
 - [X] Improve third party auth
 - [ ] ollama integration guide / docs

 ### Multi-tenancy
 - [ ] Sessions
 - [ ] Sandboxing (probably with e2b)


code-assistant is built on OpenAI's Assistant API and uses astra-assistants to support other models including claude and local models.

## Install and run

Install with pip:

    pip install code-assistant

Run:

    code-assistant

this will start the web server on port 5001 and will create a generated_apps directory on your current working directory. You can override this directory by setting the CA_GENERATED_APPS_DIR environment variable.

    export CA_GENERATED_APPS_DIR="~/my_apps"
    code-assistant

## Run as an isolated program

use pipx or uvx if you're a uv user to run as an isolated program:

    pipx run code-assistant

or

    uvx code-assistant

## Third party LLM provider Authentication

If you have not provided credentials via env vars the UI will prompt you for credentials. Credentials inputed via the UI are not persisted.

To avoid manual entry, set up environment variables for [astradb](https://astra.datastax.com/) [required for any non OpenAI models] and your LLM provider of choice.:

```
#!/bin/bash

# AstraDB -> https://astra.datastax.com/ --> tokens --> administrator user --> generate
export ASTRA_DB_APPLICATION_TOKEN=""

# OpenAI Models - https://platform.openai.com/api-keys --> create new secret key
export OPENAI_API_KEY=""

# Groq Models - https://console.groq.com/keys
export GROQ_API_KEY=""

# Anthropic claude models - https://console.anthropic.com/settings/keys
export ANTHROPIC_API_KEY=""

# Gemini models -> https://makersuite.google.com/app/apikey
export GEMINI_API_KEY=""

# Perplexity models -> https://www.perplexity.ai/settings/api  --> generate
export PERPLEXITYAI_API_KEY=""

# Cohere models -> https://dashboard.cohere.com/api-keys
export COHERE_API_KEY=""

# Bedrock models -> https://docs.aws.amazon.com/bedrock/latest/userguide/setting-up.html
export AWS_REGION_NAME=""
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""

# vertexai models https://console.cloud.google.com/vertex-ai
export GOOGLE_JSON_PATH=""
export GOOGLE_PROJECT_ID=""

# ... for other models see https://github.com/datastax/astra-assistants-api/blob/main/.env.bkp
```
