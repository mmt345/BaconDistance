FROM python:3.9-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY db db

RUN python db/generate_db.py

COPY . .

EXPOSE 5000

CMD ["python", "bacon_server.py"]