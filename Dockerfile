FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt requirements.lock ./
RUN python -m pip install --no-cache-dir -c requirements.lock -r requirements.txt
COPY model.py ./
COPY data/sites.csv ./data/
USER 10001:10001
CMD ["python", "model.py", "--input", "data/sites.csv", "--output", "/tmp/scores.csv"]
