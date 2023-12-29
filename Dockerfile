FROM python:3.8
WORKDIR /app
ADD app.py .
CMD python app.py
