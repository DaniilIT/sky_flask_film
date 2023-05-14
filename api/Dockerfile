FROM python:3.11-alpine

ENV HOME /src
WORKDIR ${HOME}
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .

ENV FLASK_APP run
ENV FLASK_ENV production
CMD python -m flask run -h 0.0.0.0 -p 5000
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
# CMD gunicorn -w 4 -b 0.0.0.0:5000 run:app
