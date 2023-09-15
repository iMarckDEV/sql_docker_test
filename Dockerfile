# init a base image (Alpine is small Linux distro)
FROM python:3-alpine3.15
# update pip to minimize dependency errors 
RUN pip install --upgrade pip
# define the present working directory
WORKDIR /flask-test
# copy the contents into the working dir
ADD . /flask-test
# run pip to install the dependencies of the flask app
RUN pip install flask pandas 
#RUN apk add --no-cache libsqlite3-dev sqlite3
RUN pip install sqlalchemy gunicorn
RUN pip install tabulate
#RUN pip install libsqlite3-dev sqlite3
#RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python","app.py"]