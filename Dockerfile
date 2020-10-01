FROM python:3.7-alpine3.9

RUN apk update && apk add bash build-base python3-dev libffi-dev

WORKDIR /app

COPY . ./

#RUN pip install -r requirements.txt
RUN pip install .

RUN chmod +x ./run.sh

ENTRYPOINT ./run.sh
