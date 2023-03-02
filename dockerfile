FROM --platform=linux/amd64  ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y install tesseract-ocr \
    && apt-get -y install wkhtmltopdf \
    && apt-get install -y python3 python3-distutils python3-pip \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 --no-cache-dir install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

RUN apt update \
    && apt-get install ffmpeg libsm6 libxext6 -y

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install Pillow
RUN pip3 install pytesseract

EXPOSE 8000

CMD ["python3", "app.py"]