FROM python:3.10.14-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 80

CMD ["python", "main.py"]

