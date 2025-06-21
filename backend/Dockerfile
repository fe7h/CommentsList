FROM python:3.11.2

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD python3 manage.py migrate && daphne -b 0.0.0.0 -p 8000 SPAComments.asgi:application