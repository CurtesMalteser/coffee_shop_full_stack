FROM python:3.12.5-slim

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /src

WORKDIR /src

ENV FLASK_APP=src/api.py
ENV FLASK_ENV=development

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
