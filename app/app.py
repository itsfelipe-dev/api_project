#!/usr/bin/env python
from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, MetaData
from sqlalchemy import text
from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import pandas as pd
import io
import os

app = Flask(__name__)

load_dotenv()
HOST_DB = os.getenv('HOST_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB =  os.getenv('PASSWORD_DB')
DATABASE = os.getenv('DATABASE')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}/{DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

table_info = {'departments', 'jobs' ,'hiredemployees'}

class Departments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	kind = db.Column(db.String(255))

class Jobs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))

class Hiredemployees(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	datetime = db.Column(db.String(255))
	department_id = db.Column(db.Integer)
	job_id = db.Column(db.Integer)

with app.app_context():
	db.create_all()


@app.route('/', methods=['GET'])
def home():
	return render_template('home.html') 


def set_columns_table(table, data):
		table_class = globals()[table.title()]
		data.columns = table_class.__table__.columns.keys() 
		return data

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
	"""
		This endpoint are going to handle post files in csv format and inert into mysql database 
	"""
	try:
		try:
			table = request.headers.get('table').lower()
		except Exception as err:
			return jsonify({'error': 'Must include table header table:<table>'}), 400
		
		if table in table_info:
			file_data = request.get_data()
			data = pd.read_csv(io.BytesIO(file_data))
			data = set_columns_table(table, data)
			data.to_sql(name=table, con=db.engine, if_exists='append', index=False)
			return jsonify ({'message': f"CSV data uploaded to {table} table"}), 200
		
	except Exception as err:
		return jsonify({'error': f'Error uploading data: {err}'}), 500


@app.route('/analytics/employees-hired', methods=['GET'])
def employees_hired():
	"""
		This endpoint are going to get the number of employees hired for each job and department in 2021 divided by quarter. The
		table must be ordered alphabetically by department and job.
	"""
	with db.engine.connect() as connection:
		query= """
			select departments.kind as department, '' as empty_column, jobs.name as job, 
			SUM(CASE WHEN date_format(cast(hired_employees.datetime as date),'%m') BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1, 
			SUM(CASE WHEN date_format(cast(hired_employees.datetime as date),'%m') BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2, 
			SUM(CASE WHEN date_format(cast(hired_employees.datetime as date),'%m') BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
			SUM(CASE WHEN date_format(cast(hired_employees.datetime as date),'%m') BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
			from hired_employees inner join jobs on hired_employees.job_id = jobs.id 
			inner join departments on hired_employees.department_id = departments.id
			where date_format(cast(hired_employees.datetime as date),'%Y') = '2021'
			group by departments.id , jobs.id  
			order by `department`ASC, `job`;
			"""
		result_df = pd.read_sql(text(query),connection)
		print(result_df)
		return render_template("base.html", column_names=result_df.columns.values, row_data=list(result_df.values.tolist()),
                           title="Section 2: SQL", zip=zip, description="Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.")



@app.route('/analytics/list-id-employees', methods=['GET'])
def list_id_employees():
	"""
		This endpoint are going to get the list of ids, name and number of employees hired of each department that hired more
		employees than the mean of employees hired in 2021 for all the departments, ordered
		by the number of employees hired (descending).
	"""
	with db.engine.connect() as connection:
		query= """
			select
				hired_employees.id,
				hired_employees.name,
				count(1) as hired,
				hired_employees.datetime
			from
				hired_employees
			inner join departments on departments.id = hired_employees.department_id
			where
				date_format(cast(hired_employees.datetime as date), '%Y') = '2021'
			group by departments.id
			order by hired desc;
			"""
		result_df = pd.read_sql(text(query),connection)
		print(result_df)
		return render_template("base.html", column_names=result_df.columns.values, row_data=list(result_df.values.tolist()),
                           title="Section 2: SQL", zip=zip, description="Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.")


if __name__ == '__main__':
   app.run(debug=True)
