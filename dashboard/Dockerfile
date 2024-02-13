FROM python:3.10-slim

WORKDIR /dashboard

COPY . /dashboard/

RUN python -m pip install -U pip &&\ 
    pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]

# CMD [ "streamlit", "run", "dashboard.py" ]