FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Create a non-root user and group
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

# Set ownership of the /app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

EXPOSE 8000

CMD ["python", "app.py"]