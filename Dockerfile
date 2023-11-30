FROM python:3.9-alpine3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers build-base postgresql-dev musl-dev zlib zlib-dev libffi-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
RUN chown -R user:user /usr/local/lib/python3.9/
RUN chmod -R 755 /usr/local/lib/python3.9/
USER user

CMD ["entrypoint.sh"]