FROM python:3.8.12-buster

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY prediction_model prediction_model
COPY setup.py setup.py
RUN pip install .

CMD uvicorn prediction_model.api.fast:app --host 0.0.0.0 --port $PORT
