#!/usr/bin/env python
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, MetaData
from sqlalchemy import text
from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import pandas as pd
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

class Departments(db.Model):
	pass

class Jobs(db.Model):
	pass

class HiredEmployees(db.Model):
	pass

@app.route('/')
def home():
	#awesome code
   pass


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
	"""
		This endpoint are going to handle post files in csv format and inert into mysql database 
	"""
	#some stuff with pandas 
	# data = pd.read_csv()
	# data.to_sql()
	pass


@app.route('/analytics/employees-hired', methods=['POST'])
def upload_csv():
	"""
		This endpoint are going to get the number of employees hired for each job and department in 2021 divided by quarter. The
		table must be ordered alphabetically by department and job.
	"""
	#some sql stuff 
	pass


@app.route('/analytics/list-id-employees', methods=['POST'])
def upload_csv():
	"""
		This endpoint are going to get the list of ids, name and number of employees hired of each department that hired more
		employees than the mean of employees hired in 2021 for all the departments, ordered
		by the number of employees hired (descending).

	"""
	#some sql stuff 
	pass


if __name__ == '__main__':
   app.run(debug=True)
