FROM python:3.11-slim
WORKDIR /app
COPY lab7.py .
CMD ["python", "lab7.py"]