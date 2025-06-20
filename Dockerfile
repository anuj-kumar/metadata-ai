FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install uv
RUN uv pip install --system --no-cache-dir .

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
