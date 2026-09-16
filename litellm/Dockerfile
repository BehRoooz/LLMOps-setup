FROM ghcr.io/berriai/litellm:latest

# Install MLflow for integration
#RUN pip install mlflow

# LiteLLM runs from /app/.venv which ships without pip.
# Bootstrap pip into that venv, then install MLflow for callbacks: ["mlflow"].
RUN /app/.venv/bin/python -m ensurepip --upgrade \
    && /app/.venv/bin/python -m pip install --no-cache-dir mlflow


WORKDIR /app
