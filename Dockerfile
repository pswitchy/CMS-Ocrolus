FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]