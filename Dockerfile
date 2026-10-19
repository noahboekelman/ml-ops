FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app

# Disable development dependencies
ENV UV_NO_DEV=1

RUN uv sync --locked

RUN uv run python -m app.model   # bakes the model into the image

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "--port", "80"]

# Run with:
#    docker build -t ml-ops .
#    docker run -p 80:80 ml-ops