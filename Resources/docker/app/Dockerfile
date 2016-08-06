FROM python:2.7

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.docker-compose'
ENV PYTHONHASHSEED 'random'

RUN mkdir /code
WORKDIR /code
VOLUME /code

ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code/

CMD gunicorn config.wsgi:application -c gunicorn.py.ini
EXPOSE 8000
