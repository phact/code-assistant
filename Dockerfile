FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.cargo/bin/:$PATH"

# Set the working directory
WORKDIR /usr/src/app

# Copy only the files necessary for installing dependencies
COPY pyproject.toml uv.lock README.md ./


# Copy the rest of your application files into the container
COPY ./code_assistant ./code_assistant

# Install the dependencies specified in `pyproject.toml` and `uv.lock`.
RUN uv sync

# Specify the command to run your application
CMD ["uv", "run", "uvicorn", "code_assistant.main:app", "--host", "0.0.0.0", "--port", "5001", "--workers", "2", "--timeout-keep-alive", "600"]
