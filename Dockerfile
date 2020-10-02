FROM python:3.7-alpine3.10

#RUN echo -e "https://nl.alpinelinux.org/alpine/v3.10/main\nhttps://nl.alpinelinux.org/alpine/v3.10/community" > /etc/apk/repositories

#RUN apk update && apk add bash build-base python3-dev libffi-dev
RUN apk add --no-cache bash 

WORKDIR /app

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install .

RUN chmod +x ./run.sh

ENTRYPOINT ./run.sh
