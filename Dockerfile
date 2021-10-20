FROM python:3
ENV PYTHONUNBUFFERED 1

# Install locales
RUN apt-get update
RUN apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# de_CH.UTF-8 UTF-8/de_CH.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

# Setup project
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
