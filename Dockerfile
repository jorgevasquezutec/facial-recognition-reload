FROM python:3.9-slim

RUN apt-get update && apt-get install -y build-essential cmake ffmpeg libsm6 libxext6

WORKDIR /app

COPY /requirements/prod.txt ./

RUN pip install -U pip wheel cmake
RUN pip install --no-cache-dir -r prod.txt

COPY . .

EXPOSE 5000

CMD ["python", "."]