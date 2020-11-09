FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV CLIENT_TOKEN=${CLIENT_TOKEN}
ENTRYPOINT ["python"]
CMD ["main.py"]

