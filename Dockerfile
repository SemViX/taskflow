FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["gunicorn", "-c", "gunicorn.conf.py", "config.wsgi:application"]