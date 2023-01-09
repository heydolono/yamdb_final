FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r /app/requirements.txt
WORKDIR /app/api_yamdb/
CMD python manage.py runserver 0:5000