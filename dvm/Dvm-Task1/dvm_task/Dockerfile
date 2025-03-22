# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/dvm_task

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/dvm_task/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/dvm_task/entrypoint.sh
RUN chmod +x /usr/src/dvm_task/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/dvm_task/entrypoint.sh"]