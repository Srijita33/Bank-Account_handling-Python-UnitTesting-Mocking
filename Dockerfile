FROM python:3.11-slim

WORKDIR /app

COPY . .

CMD ["python", "-m", "unittest", "test_main.py", "-v"]