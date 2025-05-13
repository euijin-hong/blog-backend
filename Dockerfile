FROM python:alpine

ENV PYTHONBUFFERED=1
ENV PYTHONPATH=/src
WORKDIR /src

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

