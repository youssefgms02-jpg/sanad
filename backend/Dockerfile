FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_URL=sqlite:////var/data/sanad.db

WORKDIR /app/backend
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
RUN mkdir -p /var/data
RUN chmod +x /app/backend/entrypoint.sh

EXPOSE 8000
CMD ["./entrypoint.sh"]
