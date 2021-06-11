ARG PYTHON_VERSION=3.7.2
FROM python:${PYTHON_VERSION}
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt