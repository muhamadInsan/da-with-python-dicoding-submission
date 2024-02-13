FROM python:3.10-slim

ENV DB_HOST="host.docker.internal"
ENV DB_PORT="18123"
ENV DB_USER="admin"
ENV DB_PASSWORD="123123"

WORKDIR /etl

COPY . /etl

RUN python -m pip install -U pip &&\
    pip install pandas clickhouse-connect python-dotenv pytz 

ENTRYPOINT [ "python", "etl.py" ]
# CMD [ "python","etl.py" ]