FROM python:3.8-alpine
COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY ./dataset /
COPY training.py /

ENTRYPOINT [ "python" ]
CMD [ "training.py" ]
