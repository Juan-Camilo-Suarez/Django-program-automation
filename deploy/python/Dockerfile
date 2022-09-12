FROM python:3.10.5
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python src/manage.py collectstatic --no-input

EXPOSE 8000

CMD python src/manage.py migrate && \
    gunicorn --chdir src --bind 0.0.0.0:8000  program_automation.wsgi
