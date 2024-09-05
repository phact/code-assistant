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
 - [ ] Multi-turn generation

### UI/UX
 - [X] Live app preview
 - [X] Drive generated_apps dir with env var CA_GENERATED_APPS_DIR
 - [ ] Add third party model support to frontend
 - [ ] ollama integration guide / docs

 ### Multi-tenancy
 - [ ] Sessions
 - [ ] Sandboxing (probably with e2b)


code-assistant is built on OpenAI's Assistant API and uses astra-assistants to run non openAI models including local models.

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

