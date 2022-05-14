FROM python:3.7.9
LABEL Maintainer="peter.pogorelov@gmail.com"


WORKDIR /usr/app/src
ADD ./ /usr/app/src

RUN pip install -r requirements.txt

CMD [ "python", "./test.py"]