FROM python:3.10.6
COPY python_files/api /python_files/api
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn python_files.api.fast:app --host 0.0.0.0 --port $PORT
