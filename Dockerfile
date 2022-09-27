FROM python:3.8-slim-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN pip install -e .

EXPOSE 8080

ENTRYPOINT [ "python" ]

CMD ["-m", "deepapi"]
