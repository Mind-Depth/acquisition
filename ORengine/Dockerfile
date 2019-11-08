FROM python:3.7
WORKDIR /usr/src/app
COPY . /usr/src/app
EXPOSE 8080
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt
CMD ["python3", "OnionRingEngineHTTPServer.py"]