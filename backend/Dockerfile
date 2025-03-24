FROM python:3.12-slim-bookworm AS base

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-cache


FROM base
RUN apt-get -y update --fix-missing && \
    apt-get -y install curl && \
    apt-get clean
ENV TZ="Europe/Ljubljana"
COPY --from=builder --chown=project:project /project /project
WORKDIR /project
ENV PATH="/project/.venv/bin:$PATH"
# Add user for security reasons
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    ada
RUN chown -R ada:ada /project/application
# USER ada
