FROM python:alpine

ENV PYTHONBUFFERED=1
ENV PYTHONPATH=/src
WORKDIR /src

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY entrypoint.sh ./

RUN ls -l ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

