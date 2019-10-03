FROM python:3.7
WORKDIR /usr/src/app
COPY . /usr/src/app
EXPOSE 8080
RUN pip install -r ./requirements.txt
CMD ["python", "OnionRingEngineHTTPServer.py"]