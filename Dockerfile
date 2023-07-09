FROM python:3.11
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
