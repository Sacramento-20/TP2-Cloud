FROM python:3.11-bookworm
COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY APIFlask.py /
COPY ./model /model/

EXPOSE 32194

ENTRYPOINT [ "python" ]
CMD [ "APIFlask.py", "--host=0.0.0.0", "--port 32194" ]
