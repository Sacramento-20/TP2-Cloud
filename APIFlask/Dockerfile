FROM python:3.8-alpine
COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY recommend.py /

ENTRYPOINT [ "python" ]
CMD [ "recommend.py" ]
