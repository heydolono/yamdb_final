FROM python:3.7-slim
COPY ./ /app
WORKDIR /app/api_yamdb/
RUN pip install -r /app/requirements.txt
CMD python manage.py runserver 0:5000