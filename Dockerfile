FROM python:3.10.11

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# Copy the requirements and install it
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

RUN mkdir /app
COPY ./app /app
EXPOSE 8000
WORKDIR /app