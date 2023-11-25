FROM python:3.8-alpine
COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY APIFlask.py /

ENTRYPOINT [ "python" ]
CMD [ "APIFlask.py" ]
