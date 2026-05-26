FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

WORKDIR /app

ARG QUARTO_VERSION=1.9.38
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    wget \
    && wget -q "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb" \
    && apt-get install -y -f "./quarto-${QUARTO_VERSION}-linux-amd64.deb" \
    && rm "quarto-${QUARTO_VERSION}-linux-amd64.deb" \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .[dev] && \
    python -m ipykernel install --name python3

COPY . .

RUN mkdir -p output

CMD ["sh", "-c", "quarto render report.qmd && cp report.html output/"]
