FROM python:3.13-rc-bookworm
COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY ./dataset /
COPY training.py /

ENV URL_DATASET="https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_ds1.csv"

ENTRYPOINT [ "python" ]
CMD [ "training.py" ]
