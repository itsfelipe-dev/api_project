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

class HiredEmployees(db.Model):
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
			data.to_sql(name=table, con=db.engine, if_exists='append', index=False)
			return jsonify ({'message': f"CSV data uploaded to {table} table"}), 200
		
	except Exception as err:
		return jsonify({'error': f'Error uploading data: {err}'}), 500


@app.route('/analytics/employees-hired', methods=['POST'])
def employees_hired():
	"""
		This endpoint are going to get the number of employees hired for each job and department in 2021 divided by quarter. The
		table must be ordered alphabetically by department and job.
	"""
	#some sql stuff 
	pass


@app.route('/analytics/list-id-employees', methods=['POST'])
def list_id_employees():
	"""
		This endpoint are going to get the list of ids, name and number of employees hired of each department that hired more
		employees than the mean of employees hired in 2021 for all the departments, ordered
		by the number of employees hired (descending).
	"""
	#some sql stuff 
	pass


if __name__ == '__main__':
   app.run(debug=True)
