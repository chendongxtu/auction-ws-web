FROM cr.cheanjiait.com/library/python:3.6

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /auction-ws-web

EXPOSE 5000

COPY requirements.txt /auction-ws-web

RUN set -x \
      && apk add --update --virtual .build-deps \
              musl-dev \
              g++ \
              tzdata \
              git \
              curl \
              openssh-client \
      && apk add libstdc++ \
      && ONVAULT pip install --no-cache-dir -r requirements.txt \
      && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
      && apk del .build-deps \
      && rm -rf /var/cache/apk/*

COPY . /auction-ws-web

ARG GIT_COMMIT

ENV GIT_COMMIT ${GIT_COMMIT}

CMD ["gunicorn", "-b", ":5000", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "wsgi:application"]