FROM python:3.11
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
CMD gunicorn bot:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --timeout 30