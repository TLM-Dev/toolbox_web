FROM python:3.10

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -

RUN apt-get install -y nodejs

WORKDIR /backend

COPY req.txt req.txt

RUN pip install -r req.txt

COPY . .

RUN chmod +x entrypoint.sh