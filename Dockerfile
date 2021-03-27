 FROM python:rc-alpine
 WORKDIR /app
 COPY . .
 RUN pip3  --no-cache-dir --use-feature=2020-resolver install -r requirements.txt  --no-deps
 CMD ["python3", "./manage.py", "runserver"]