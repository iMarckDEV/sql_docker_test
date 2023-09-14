# Description
So in this excercise i'll launch a MySql server using Docker in my  local environment, to load some tables and creating some tables and queries:

1. Lauunch the MySql server in local

Based in the  *Dockerfile* in the path ** Docker_local_image/Dockerfile **

```bash
cd Docker_local_image
docker build -t imarckdev-mysql .
docker run --name mysql-server -p 3306:3306 -d imarckdev-mysql
```

2. The ETL in python

So, basically the scripts in python just load the csv files related in the path *pythonscripts_local*, all those
files will become a table over the running mySql server.


It's necesary have installed the package 

```bash
pip install mysql-connector-python
```
