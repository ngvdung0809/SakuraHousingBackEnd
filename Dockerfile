FROM python:3
WORKDIR /webapp
COPY requirements.txt /webapp/
RUN pip install -r requirements.txt
COPY . /webapp/
EXPOSE 8000
RUN ["chmod", "+x", "entry-point.sh"]