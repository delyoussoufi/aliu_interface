from flask import Flask, jsonify, request
from sqlite3 import connect as sqlite_connect
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return sqlite_connect('artdatabase.db')