FROM python:3.7-alpine3.10

RUN echo -e "https://nl.alpinelinux.org/alpine/v3.10/main\nhttps://nl.alpinelinux.org/alpine/v3.10/community" > /etc/apk/repositories

RUN apk update && apk add --no-cache bash build-base python3-dev libffi-dev

WORKDIR /app

COPY . ./

#RUN pip install -r requirements.txt
RUN pip install .

RUN chmod +x ./run.sh

ENTRYPOINT ./run.sh
