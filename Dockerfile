FROM python:3.12
WORKDIR /app
COPY requirements.txt checker.py urls.txt /app
RUN pip install -r requirements.txt
CMD ["python3", "checker.py", "urls.txt"]
