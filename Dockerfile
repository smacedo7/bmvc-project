FROM python:3.12-slim
WORKDIR /bmeta
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BMVC_HOST=0.0.0.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd --system bmvc && useradd --system --gid bmvc --create-home bmvc
COPY --chown=bmvc:bmvc alembic.ini ./
COPY --chown=bmvc:bmvc migrations ./migrations
COPY --chown=bmvc:bmvc app ./app
COPY --chown=bmvc:bmvc route.py realtime.py ./
USER bmvc

EXPOSE 8080
CMD ["python3", "realtime.py"]
