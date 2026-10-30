## ------------------------------- Builder Stage ------------------------------ ## 
FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync

## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.12-slim-bookworm AS production

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY /common /app/common
COPY README.md /app/README.md
COPY /src /app/src
COPY /data /app/data
COPY /config /app/config

# The classic (non-BuildKit) docker builder always runs COPY as root regardless of
# the active USER, so /app ends up root-owned - fix that up explicitly.
USER root
RUN chown -R appuser:appuser /app
USER appuser

# Set up environment variables for production
ENV PATH="/app/.venv/bin:$PATH"

# Expose the specified port for FastAPI
EXPOSE $PORT

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]


