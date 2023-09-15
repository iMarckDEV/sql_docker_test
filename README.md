# iMarckDEV Blog Repository

Welcome to the iMarckDEV Blog Repository! This repository contains the source code for the [iMarckDEV blog site](https://www.imarck.dev), a platform dedicated to exploring cloud technologies, sharing tutorials, and providing valuable resources for developers.

# Description
So in this excercise i'll launch a server using Docker in a local environment, to load some tables and creating some tables and queries:

## 1. Launch the Docker server in local

Based in the  *Dockerfile* in the repo

```bash
docker image build -t flask-test .
docker run -p 5000:5000 -d flask-test
```

## 2. The ETL in python

So, basically the scripts in python just use flask, and sqlitle3 in *app.py*, 
with principals endpoits:

```python
@app.route('/') #the index.html, the principal, where just load the related files
@app.route('/load') #for the success loading files
@app.route('/employees') #justo to see a dataframe of employees
@app.route('/query1')
@app.route('/query2')
```

## 3. The local host endpoints
in localhost 127.0.0.1:5000

![LOAD](/images/principal_load.png)

in localhost 127.0.0.1:5000/query1

![QUERY1](/images/query1.png)

in localhost 127.0.0.1:5000/query2

![QUERY2](/images/query2.png)

## Join the Community
Join our vibrant developer community on the iMarckDEV blog site. Connect with fellow developers, ask questions, and share your insights. Together, we can learn, grow, and make a positive impact in the world of technology.

Thank you for your interest in the iMarckDEV Blog Repository. Happy coding!


