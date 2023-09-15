""""
from flask import Flask, render_template,request, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

"""
# app.py

from flask import Flask, request, jsonify, render_template  
import sqlite3
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)

# Function to get db connection
def get_db_connection():
    conn = sqlite3.connect('data.db')
    return conn

# Create tables
conn = get_db_connection()
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS departments  
             (id INTEGER PRIMARY KEY, department TEXT)''') 
             
c.execute('''CREATE TABLE IF NOT EXISTS jobs  
             (id INTEGER PRIMARY KEY, job TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS employees
             (id INTEGER PRIMARY KEY, name TEXT, hire_date TEXT, 
              department_id INTEGER, job_id INTEGER,
              FOREIGN KEY(department_id) REFERENCES departments(id),
              FOREIGN KEY(job_id) REFERENCES jobs(id))''')
              
# Index route            
@app.route('/')
def index():
    return render_template('index.html')

# Route to load data
@app.route('/load', methods=['POST']) 
def load_data():
  conn = get_db_connection()
  c = conn.cursor()
  # Load CSVs 
  departments_df = pd.read_csv(request.files['departments'],header=None)  
  jobs_df = pd.read_csv(request.files['jobs'],header=None)
  employees_df = pd.read_csv(request.files['employees'],header=None )

  # Clear and load data
  #c.execute('DELETE FROM departments')
  departments_df.columns=['id','department']
  departments_df.to_sql('departments', conn, if_exists='append', index=False)

  #c.execute('DELETE FROM jobs')
  jobs_df.columns=['id','job']
  jobs_df.to_sql('jobs', conn, if_exists='append', index=False)

  #c.execute('DELETE FROM employees')
  employees_df.columns=['id','name','hire_date', 'department_id', 'job_id']
  employees_df.to_sql('employees', conn, if_exists='append', index=False)
  
  conn.close()
  return jsonify({'message': 'Data loaded successfully'})

# Route to fetch all employees

@app.route('/employees')
def get_employees():
  conn = get_db_connection()
  c = conn.cursor()

  c.execute('SELECT * FROM employees')
  data = c.fetchall()
  conn.close()

  #return jsonify(data)
  return render_template('employees.html', employees=data)

"""
For the query1
Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.
"""
@app.route('/query1')
def employee_query():

  conn = get_db_connection()
  c = conn.cursor()

  c.execute('''SELECT d.department, j.job,  
               SUM(CASE WHEN strftime('%m', e.hire_date) IN ('01','02','03') THEN 1 ELSE 0 END) AS Q1,
               SUM(CASE WHEN strftime('%m', e.hire_date) IN ('04','05','06') THEN 1 ELSE 0 END) AS Q2, 
               SUM(CASE WHEN strftime('%m', e.hire_date) IN ('07','08','09') THEN 1 ELSE 0 END) AS Q3,
               SUM(CASE WHEN strftime('%m', e.hire_date) IN ('10','11','12') THEN 1 ELSE 0 END) AS Q4
             FROM employees e
             JOIN departments d ON e.department_id = d.id
             JOIN jobs j ON e.job_id = j.id
             WHERE strftime('%Y', e.hire_date) = '2021'
             GROUP BY d.department, j.job
             ORDER BY d.department, j.job''')

  results = c.fetchall()

  conn.close()            

  return render_template('query1.html', query_results=results)

"""
For query 2
List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).
"""
@app.route('/query2')
def departments_above_average():

  conn = get_db_connection()
  c = conn.cursor()  

  # Get mean hires in 2021
  c.execute('''SELECT avg(hired) 
              FROM (
                SELECT department_id, count(*) AS hired
                FROM employees
                WHERE strftime('%Y', hire_date) = '2021'
                GROUP BY department_id)''')
  
  mean = c.fetchone()[0]

  # Get departments above mean
  c.execute('''SELECT d.id, d.department, count(*) AS hired
              FROM employees e
              JOIN departments d ON e.department_id = d.id
              WHERE strftime('%Y', e.hire_date) = '2021'
              GROUP BY d.id
              HAVING count(*) > :mean
              ORDER BY hired DESC''', {'mean': mean})
              
  results = c.fetchall()

  conn.close()

  return render_template('query2.html', query2_results=results)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')