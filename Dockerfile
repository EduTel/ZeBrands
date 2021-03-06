 FROM python:3.9.1-alpine3.13
 WORKDIR /app
 COPY . .
 RUN pip3  --no-cache-dir --use-feature=2020-resolver install -r requirements.txt  --no-deps
 CMD ["python3", "./manage.py", "runserver"]