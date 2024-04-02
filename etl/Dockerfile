FROM python:3.10.0

WORKDIR /etl

COPY . /etl

RUN python -m pip install -U pip
RUN pip install pandas clickhouse-connect python-dotenv pytz

CMD [ "python","etl.py" ]