FROM python:3.8.10-slim-buster

WORKDIR /website

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN chmod +x /website/entrypoint.sh

CMD ["bash", "-c", "website/entrypoint.sh"]

COPY . .