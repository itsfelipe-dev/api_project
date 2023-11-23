#!/usr/bin/env python
import os
from dotenv import load_dotenv

load_dotenv()


HOST_DB = os.getenv('HOST_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB =  os.getenv('PASSWORD_DB')
DATABASE = os.getenv('DATABASE')


print(HOST_DB, USER_DB , PASSWORD_DB, DATABASE)