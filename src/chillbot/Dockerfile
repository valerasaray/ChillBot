FROM python:3.10-slim AS builder
WORKDIR /
COPY ./src/chillbot/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./src/chillbot /app
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
WORKDIR /app
ENTRYPOINT [ "python3", "main.py" ]
