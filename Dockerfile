FROM python:3

WORKDIR /app

ADD . /app

RUN apt-get update && \
    # install sqlite3
    apt-get install -y sqlite3 libsqlite3-dev && \
    # run setup.py
    pip install --upgrade pip && \
    pip install --no-cache-dir . \

# run quesadiya to create projects folder
RUN quesadiya inspect all    
