FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and the README
COPY src/ ./src/
COPY README.md .

EXPOSE 80

# Use gunicorn with gevent worker to support WebSockets
# Run from src directory
CMD ["gunicorn", "-k", "gevent", "-w", "1", "src.app:app", "--bind", "0.0.0.0:80"]
