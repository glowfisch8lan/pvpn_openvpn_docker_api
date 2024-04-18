#!/usr/bin/python3

from flask import Flask
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from src.Routes import route

print('Start flask application...')
load_dotenv()
app = Flask(__name__)
route(app)

@app.errorhandler(HTTPException)
def handle_exception(e):
    print(e)
    try:
        msg = e.original_exception.msg
        code = e.original_exception.code
    except:
        msg = 'error'
        code = 500

    return msg, code
