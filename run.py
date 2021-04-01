import pyodbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#DBconnection
try:
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=ASHWANI;'
                        'Database=audiodb;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
except pyodbc.Error as ex:
    print ("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description))

from routes.runRoutes import *

# Required because run is imported in other modules
if __name__== '__main__':
    app.run(debug=True)