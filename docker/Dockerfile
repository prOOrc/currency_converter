FROM python:3.7

COPY /requirements/ /src/requirements/

RUN pip install -r /src/requirements/requirements-prod.txt
RUN pip install -r /src/requirements/requirements-dev.txt
RUN pip install -r /src/requirements/requirements-setup.txt
