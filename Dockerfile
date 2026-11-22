FROM python:3.12-slim
WORKDIR /bmeta
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV BMVC_HOST=0.0.0.0
EXPOSE 8080
CMD ["python3", "route.py"]

