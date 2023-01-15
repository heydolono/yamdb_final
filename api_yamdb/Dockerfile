FROM python:3.7-slim
WORKDIR /app
RUN pip install -r /app/requirements.txt
COPY ./ ./
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ] 