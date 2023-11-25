FROM python:3.11-bookworm
COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY APIFlask.py /
COPY ./model /model/

ENTRYPOINT [ "python" ]
CMD [ "APIFlask.py" ]
