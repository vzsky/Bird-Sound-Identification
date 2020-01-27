FROM python:3.7-buster

COPY req /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY app.py /app/webapp.py
COPY Birdmodel.h5 /app/Birdmodel.h5
COPY template/result.html /app/template/result.html
COPY template/uploadfile.html /app/template/uploadfile.html

WORKDIR /app
EXPOSE 80
CMD ["python", "webapp.py"]